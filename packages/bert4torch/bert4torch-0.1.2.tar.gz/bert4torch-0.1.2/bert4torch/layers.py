from audioop import bias
from turtle import forward
from sympy import im
import torch
import torch.nn as nn
from torch.nn import functional as F
import math
from bert4torch.snippets import get_sinusoid_encoding_table
from bert4torch.activations import get_activation


class LayerNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-12, conditional_size=False, bias=True, mode='normal', **kwargs):
        """layernorm 层，这里自行实现，目的是为了兼容 conditianal layernorm，使得可以做条件文本生成、条件分类等任务
           条件layernorm来自于苏剑林的想法，详情：https://spaces.ac.cn/archives/7124
        """
        super(LayerNorm, self).__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        # 兼容t5不包含bias项, 和t5使用的RMSnorm
        if bias:
            self.bias = nn.Parameter(torch.zeros(hidden_size))
        self.mode = mode

        self.eps = eps
        self.conditional_size = conditional_size
        if conditional_size:
            # 条件layernorm, 用于条件文本生成,
            # 这里采用全零初始化, 目的是在初始状态不干扰原来的预训练权重
            self.dense1 = nn.Linear(conditional_size, hidden_size, bias=False)
            self.dense1.weight.data.uniform_(0, 0)
            self.dense2 = nn.Linear(conditional_size, hidden_size, bias=False)
            self.dense2.weight.data.uniform_(0, 0)

    def forward(self, x):
        inputs = x[0]

        if self.mode == 'rmsnorm':
            # t5使用的是RMSnorm
            variance = inputs.to(torch.float32).pow(2).mean(-1, keepdim=True)
            o = inputs * torch.rsqrt(variance + self.eps)
        else:
            u = inputs.mean(-1, keepdim=True)
            s = (inputs - u).pow(2).mean(-1, keepdim=True)
            o = (inputs - u) / torch.sqrt(s + self.eps)

        if not hasattr(self, 'bias'):
            self.bias = 0

        if self.conditional_size:
            cond = x[1]
            for _ in range(len(inputs.shape) - len(cond.shape)):
                cond = cond.unsqueeze(dim=1)
            return (self.weight + self.dense1(cond)) * o + (self.bias + self.dense2(cond))
        else:
            return self.weight * o + self.bias


class MultiHeadAttentionLayer(nn.Module):
    def __init__(self, hidden_size, num_attention_heads, attention_probs_dropout_prob, attention_scale=True,
                 return_attention_scores=False, **kwargs):
        super(MultiHeadAttentionLayer, self).__init__()

        assert hidden_size % num_attention_heads == 0

        self.hidden_size = hidden_size
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = int(hidden_size / num_attention_heads)
        self.attention_scale = attention_scale
        self.return_attention_scores = return_attention_scores

        self.q = nn.Linear(hidden_size, hidden_size)
        self.k = nn.Linear(hidden_size, hidden_size)
        self.v = nn.Linear(hidden_size, hidden_size)
        self.o = nn.Linear(hidden_size, hidden_size)
        self.dropout = nn.Dropout(attention_probs_dropout_prob)

        self.a_bias, self.p_bias = kwargs.get('a_bias'), kwargs.get('p_bias')

        if self.p_bias == 'typical_relative':  # nezha
            self.relative_positions_encoding = RelativePositionsEncoding(qlen=kwargs.get('max_position'),
                                                                         klen=kwargs.get('max_position'),
                                                                         embedding_size=self.attention_head_size,
                                                                         max_relative_position=kwargs.get('max_relative_position'))
        elif self.p_bias == 'rotary':  # roformer
            self.relative_positions_encoding = RoPEPositionEncoding(max_position=kwargs.get('max_position'), embedding_size=self.attention_head_size)
        elif self.p_bias == 't5_relative':  # t5
            self.relative_positions = RelativePositionsEncodingT5(qlen=kwargs.get('max_position'), 
                                                                  klen=kwargs.get('max_position'), 
                                                                  relative_attention_num_buckets=kwargs.get('relative_attention_num_buckets'), 
                                                                  is_decoder=kwargs.get('is_decoder'))
            self.relative_positions_encoding = nn.Embedding(kwargs.get('relative_attention_num_buckets'), self.num_attention_heads)

    def transpose_for_scores(self, x):
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        x = x.view(*new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(self, hidden_states, attention_mask=None, encoder_hidden_states=None, encoder_attention_mask=None):
        # hidden_states shape: [batch_size, seq_q, hidden_size]
        # attention_mask shape: [batch_size, 1, 1, seq_q] 或者 [batch_size, 1, seq_q, seq_q]
        # encoder_hidden_states shape: [batch_size, seq_k, hidden_size]
        # encoder_attention_mask shape: [batch_size, 1, 1, seq_k]

        mixed_query_layer = self.q(hidden_states)
        if encoder_hidden_states is not None:
            mixed_key_layer = self.k(encoder_hidden_states)
            mixed_value_layer = self.v(encoder_hidden_states)
            attention_mask = encoder_attention_mask
        else:
            mixed_key_layer = self.k(hidden_states)
            mixed_value_layer = self.v(hidden_states)
        # mixed_query_layer shape: [batch_size, query_len, hidden_size]
        # mixed_query_layer shape: [batch_size, key_len, hidden_size]
        # mixed_query_layer shape: [batch_size, value_len, hidden_size]

        query_layer = self.transpose_for_scores(mixed_query_layer)
        key_layer = self.transpose_for_scores(mixed_key_layer)
        value_layer = self.transpose_for_scores(mixed_value_layer)
        # query_layer shape: [batch_size, num_attention_heads, query_len, attention_head_size]
        # key_layer shape: [batch_size, num_attention_heads, key_len, attention_head_size]
        # value_layer shape: [batch_size, num_attention_heads, value_len, attention_head_size]

        if self.p_bias == 'rotary':
            query_layer = self.relative_positions_encoding(query_layer)
            key_layer = self.relative_positions_encoding(key_layer)

        # 交换k的最后两个维度，然后q和k执行点积, 获得attention score
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))

        # attention_scores shape: [batch_size, num_attention_heads, query_len, key_len]
        if (self.p_bias == 'typical_relative') and hasattr(self, 'relative_positions_encoding'):
            relations_keys = self.relative_positions_encoding(attention_scores.shape[-1], attention_scores.shape[-1])  # [to_seq_len, to_seq_len, d_hid]
            # 旧实现，方便读者理解维度转换
            # query_layer_t = query_layer.permute(2, 0, 1, 3)
            # query_layer_r = query_layer_t.contiguous().view(from_seq_length, batch_size * num_attention_heads, self.attention_head_size)
            # key_position_scores = torch.matmul(query_layer_r, relations_keys.permute(0, 2, 1))
            # key_position_scores_r = key_position_scores.view(from_seq_length, batch_size, num_attention_heads, from_seq_length)
            # key_position_scores_r_t = key_position_scores_r.permute(1, 2, 0, 3)
            # 新实现
            key_position_scores_r_t = torch.einsum('bnih,ijh->bnij', query_layer, relations_keys)
            attention_scores = attention_scores + key_position_scores_r_t
        elif (self.p_bias == 't5_relative') and hasattr(self, 'relative_positions_encoding'):
            relations_keys = self.relative_positions(attention_scores.shape[-1], attention_scores.shape[-1])
            key_position_scores_r_t = self.relative_positions_encoding(relations_keys).permute([2, 0, 1]).unsqueeze(0)
            attention_scores = attention_scores + key_position_scores_r_t

        # 是否进行attention scale
        if self.attention_scale:
            attention_scores = attention_scores / math.sqrt(self.attention_head_size)
        # 执行attention mask，对于mask为0部分的attention mask，
        # 值为-1e10，经过softmax后，attention_probs几乎为0，所以不会attention到mask为0的部分
        if attention_mask is not None:
            # attention_scores = attention_scores.masked_fill(attention_mask == 0, -1e10)
            attention_mask = (1.0 - attention_mask) * -10000.0  # 所以传入的mask的非padding部分为1, padding部分为0
            attention_scores = attention_scores + attention_mask

        # 将attention score 归一化到0-1
        attention_probs = nn.Softmax(dim=-1)(attention_scores)
        attention_probs = self.dropout(attention_probs)
        context_layer = torch.matmul(attention_probs, value_layer)  # [batch_size, num_attention_heads, query_len, attention_head_size]

        if (self.p_bias == 'typical_relative') and hasattr(self, 'relative_positions_encoding'):
            relations_values = self.relative_positions_encoding(attention_scores.shape[-1], attention_scores.shape[-1])
            # 旧实现，方便读者理解维度转换
            # attention_probs_t = attention_probs.permute(2, 0, 1, 3)
            # attentions_probs_r = attention_probs_t.contiguous().view(from_seq_length, batch_size * num_attention_heads, to_seq_length)
            # value_position_scores = torch.matmul(attentions_probs_r, relations_values)
            # value_position_scores_r = value_position_scores.view(from_seq_length, batch_size, num_attention_heads, self.attention_head_size)
            # value_position_scores_r_t = value_position_scores_r.permute(1, 2, 0, 3)
            # 新实现
            value_position_scores_r_t = torch.einsum('bnij,ijh->bnih', attention_probs, relations_values)
            context_layer = context_layer + value_position_scores_r_t

        # context_layer shape: [batch_size, query_len, num_attention_heads, attention_head_size]
        # transpose、permute等维度变换操作后，tensor在内存中不再是连续存储的，而view操作要求tensor的内存连续存储，
        # 所以在调用view之前，需要contiguous来返回一个contiguous copy；
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()

        new_context_layer_shape = context_layer.size()[:-2] + (self.hidden_size,)
        context_layer = context_layer.view(*new_context_layer_shape)

        # 是否返回attention scores
        if self.return_attention_scores:
            # 这里返回的attention_scores没有经过softmax, 可在外部进行归一化操作
            return self.o(context_layer), attention_scores
        else:
            return self.o(context_layer)


class PositionWiseFeedForward(nn.Module):
    def __init__(self, hidden_size, intermediate_size, dropout_rate=0.5, hidden_act='gelu', is_dropout=False, **kwargs):
        # 原生的tf版本的bert在激活函数后，没有添加dropout层，但是在google AI的bert-pytorch开源项目中，多了一层dropout；
        # 并且在pytorch官方的TransformerEncoderLayer的实现中，也有一层dropout层，就像这样：self.linear2(self.dropout(self.activation(self.linear1(src))))；
        # 这样不统一做法的原因不得而知，不过有没有这一层，差别可能不会很大；

        # 为了适配是否dropout，用is_dropout，dropout_rate两个参数控制；如果是实现原始的transformer，直接使用默认参数即可；如果是实现bert，则is_dropout为False，此时的dropout_rate参数并不会使用.
        super(PositionWiseFeedForward, self).__init__()

        self.is_dropout = is_dropout
        self.intermediate_act_fn = get_activation(hidden_act)
        self.intermediateDense = nn.Linear(hidden_size, intermediate_size)
        self.outputDense = nn.Linear(intermediate_size, hidden_size)
        if self.is_dropout:
            self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        # x shape: (batch size, seq len, hidden_size)
        if self.is_dropout:
            x = self.dropout(self.intermediate_act_fn(self.intermediateDense(x)))
        else:
            x = self.intermediate_act_fn(self.intermediateDense(x))

        # x shape: (batch size, seq len, intermediate_size)
        x = self.outputDense(x)

        # x shape: (batch size, seq len, hidden_size)
        return x


class BertEmbeddings(nn.Module):
    """
        embeddings层
        构造word, position and token_type embeddings.
    """
    def __init__(self, vocab_size, embedding_size, hidden_size, max_position, segment_vocab_size, shared_segment_embeddings, drop_rate, conditional_size=False, **kwargs):
        super(BertEmbeddings, self).__init__()
        self.shared_segment_embeddings = shared_segment_embeddings
        self.word_embeddings = nn.Embedding(vocab_size, embedding_size, padding_idx=0)
        if (kwargs.get('p_bias') not in {'rotary', 'typical_relative', 't5_relative'}) and max_position > 0: # Embeddings时候包含位置编码
            self.position_embeddings = nn.Embedding(max_position, embedding_size)
        if (segment_vocab_size > 0) and (not shared_segment_embeddings):
            self.segment_embeddings = nn.Embedding(segment_vocab_size, embedding_size)

        self.layerNorm = LayerNorm(embedding_size, eps=1e-12, conditional_size=conditional_size)
        self.dropout = nn.Dropout(drop_rate)
        # 如果embedding_size != hidden_size，则再有一个linear(适用于albert矩阵分解)
        if embedding_size != hidden_size:
            self.embedding_hidden_mapping_in = nn.Linear(embedding_size, hidden_size)

    def forward(self, token_ids, segment_ids=None, conditional_emb=None):
        words_embeddings = self.word_embeddings(token_ids)

        if hasattr(self, 'segment_embeddings'):
            segment_ids = torch.zeros_like(token_ids) if segment_ids is None else segment_ids
            segment_embeddings = self.segment_embeddings(segment_ids)  
            embeddings = words_embeddings + segment_embeddings
        elif self.shared_segment_embeddings:  # segment和word_embedding共享权重
            segment_ids = torch.zeros_like(token_ids) if segment_ids is None else segment_ids
            segment_embeddings = self.word_embeddings(segment_ids)  
            embeddings = words_embeddings + segment_embeddings
        else:
            embeddings = words_embeddings
        
        if hasattr(self, 'position_embeddings'):
            seq_length = token_ids.size(1)
            position_ids = torch.arange(seq_length, dtype=torch.long, device=token_ids.device)
            position_ids = position_ids.unsqueeze(0).expand_as(token_ids)
            position_embeddings = self.position_embeddings(position_ids)
            embeddings += position_embeddings

        if hasattr(self, 'layerNorm'):
            embeddings = self.layerNorm((embeddings, conditional_emb))
        embeddings = self.dropout(embeddings)

        if hasattr(self, 'embedding_hidden_mapping_in'):
            embeddings = self.embedding_hidden_mapping_in(embeddings)
        return embeddings


class BertLayer(nn.Module):
    """
        Transformer层:
        顺序为: Attention --> Add --> LayerNorm --> Feed Forward --> Add --> LayerNorm

        注意: 1、以上都不计dropout层，并不代表没有dropout，每一层的dropout使用略有不同，注意区分
              2、原始的Transformer的encoder中的Feed Forward层一共有两层linear，
              config.intermediate_size的大小不仅是第一层linear的输出尺寸，也是第二层linear的输入尺寸
    """
    def __init__(self, hidden_size, num_attention_heads, dropout_rate, attention_probs_dropout_prob, intermediate_size, hidden_act, 
                 is_dropout=False, conditional_size=False, **kwargs):
        super(BertLayer, self).__init__()
        self.multiHeadAttention = MultiHeadAttentionLayer(hidden_size, num_attention_heads, attention_probs_dropout_prob, **kwargs)
        self.dropout1 = nn.Dropout(dropout_rate)
        self.layerNorm1 = LayerNorm(hidden_size, eps=1e-12, conditional_size=conditional_size)
        self.feedForward = PositionWiseFeedForward(hidden_size, intermediate_size, dropout_rate, hidden_act, is_dropout=is_dropout)
        self.dropout2 = nn.Dropout(dropout_rate)
        self.layerNorm2 = LayerNorm(hidden_size, eps=1e-12, conditional_size=conditional_size)
        self.is_decoder = kwargs.get('is_decoder')
        if self.is_decoder:
            self.crossAttention = MultiHeadAttentionLayer(hidden_size, num_attention_heads, attention_probs_dropout_prob, **kwargs)
            self.dropout3 = nn.Dropout(dropout_rate)
            self.layerNorm3 = LayerNorm(hidden_size, eps=1e-12, conditional_size=conditional_size)

    def forward(self, hidden_states, attention_mask, conditional_emb=None, encoder_hidden_states=None, encoder_attention_mask=None):
        self_attn_output = self.multiHeadAttention(hidden_states, attention_mask)  # self.decoder为true时候，这里的attention_mask是三角的
        hidden_states = hidden_states + self.dropout1(self_attn_output)
        hidden_states = self.layerNorm1((hidden_states, conditional_emb))
        
        # cross attention
        if self.is_decoder and encoder_hidden_states is not None:
            cross_attn_output = self.crossAttention(hidden_states, None, encoder_hidden_states, encoder_attention_mask)
            hidden_states = hidden_states + self.dropout3(cross_attn_output)
            hidden_states = self.layerNorm3((hidden_states, conditional_emb))
            
        self_attn_output2 = self.feedForward(hidden_states)
        hidden_states = hidden_states + self.dropout2(self_attn_output2)
        hidden_states = self.layerNorm2((hidden_states, conditional_emb))
        return hidden_states


class T5Layer(BertLayer):
    """T5的Encoder的主体是基于Self-Attention的模块
    顺序：LN --> Att --> Add --> LN --> FFN --> Add
    """
    def __init__(self, *args, version='t5.1.0', **kwargs):
        super().__init__(*args, **kwargs)
        # 定义RMSnorm层
        self.layerNorm1 = LayerNorm(hidden_size=args[0], eps=1e-12, bias=False, mode='rmsnorm', **kwargs)
        self.layerNorm2 = LayerNorm(hidden_size=args[0], eps=1e-12, bias=False, mode='rmsnorm', **kwargs)

        # 删除对应的bias项
        self.multiHeadAttention.q.register_parameter('bias', None)
        self.multiHeadAttention.k.register_parameter('bias', None)
        self.multiHeadAttention.v.register_parameter('bias', None)
        self.multiHeadAttention.o.register_parameter('bias', None)

        # 如果是t5.1.1结构，则FFN层需要变更
        if version.endswith('t5.1.0'):
            self.feedForward.outputDense.register_parameter('bias', None)
            self.feedForward.intermediateDense.register_parameter('bias', None)
        elif version.endswith('t5.1.1'):
            kwargs['dropout_rate'] = args[2]
            kwargs['hidden_act'] = args[5]
            self.feedForward = self.T5PositionWiseFeedForward(hidden_size=args[0], intermediate_size=args[4], **kwargs)
        else:
            raise ValueError('T5 model only support t5.1.0 and t5.1.1')

        # decoder中间有crossAttention
        if self.is_decoder:
            self.layerNorm3 = LayerNorm(hidden_size=args[0], eps=1e-12, bias=False, mode='rmsnorm', **kwargs)
            self.crossAttention.q.register_parameter('bias', None)
            self.crossAttention.k.register_parameter('bias', None)
            self.crossAttention.v.register_parameter('bias', None)
            self.crossAttention.o.register_parameter('bias', None)
            if hasattr(self.crossAttention, 'relative_positions_encoding'):
                del self.crossAttention.relative_positions_encoding
                del self.crossAttention.relative_positions

    def forward(self, hidden_states, attention_mask, conditional_emb=None, encoder_hidden_states=None, encoder_attention_mask=None):
        # bert的layernorm是在attn/ffc之后，Openai-gpt2是在之前
        x = self.layerNorm1((hidden_states, conditional_emb))
        self_attn_output = self.multiHeadAttention(x, attention_mask)
        hidden_states = hidden_states + self.dropout1(self_attn_output)

        # cross attention
        if self.is_decoder and encoder_hidden_states is not None:
            x = self.layerNorm3((hidden_states, conditional_emb))
            cross_attn_output = self.crossAttention(x, None, encoder_hidden_states, encoder_attention_mask)
            hidden_states = hidden_states + self.dropout3(cross_attn_output)

        x = self.layerNorm2((hidden_states, conditional_emb))
        ffn_output = self.feedForward(x)
        hidden_states = hidden_states + self.dropout2(ffn_output)
        return hidden_states

    class T5PositionWiseFeedForward(PositionWiseFeedForward):
        def __init__(self, hidden_size, intermediate_size, **kwargs):
            super().__init__(hidden_size, intermediate_size, **kwargs)
            self.intermediateDense = nn.Linear(hidden_size, intermediate_size, bias=False)
            self.intermediateDense1 = nn.Linear(hidden_size, intermediate_size, bias=False)
            self.outputDense = nn.Linear(intermediate_size, hidden_size, bias=False)

        def forward(self, x):
            # x shape: (batch size, seq len, hidden_size)
            x_gelu = self.intermediate_act_fn(self.intermediateDense(x))
            x_linear = self.intermediateDense1(x)
            x = x_gelu * x_linear
            if self.is_dropout:
                x = self.dropout(x)

            # x shape: (batch size, seq len, intermediate_size)
            x = self.outputDense(x)

            # x shape: (batch size, seq len, hidden_size)
            return x


class Identity(nn.Module):
    def __init__(self, *args, **kwargs):
        super(Identity, self).__init__()

    def forward(self, *args):
        return args[0]


class RelativePositionsEncoding(nn.Module):
    """nezha用的google相对位置编码
    来自论文：https://arxiv.org/abs/1803.02155
    """
    def __init__(self, qlen, klen, embedding_size, max_relative_position=127):
        super(RelativePositionsEncoding, self).__init__()
        # 生成相对位置矩阵
        vocab_size = max_relative_position * 2 + 1
        distance_mat = torch.arange(klen)[None, :] - torch.arange(qlen)[:, None]  # 列数-行数, [query_len, key_len]
        distance_mat_clipped = torch.clamp(distance_mat, -max_relative_position, max_relative_position)
        final_mat = distance_mat_clipped + max_relative_position

        # sinusoid_encoding编码的位置矩阵
        embeddings_table = get_sinusoid_encoding_table(vocab_size, embedding_size)

        # 实现方式1
        # flat_relative_positions_matrix = final_mat.view(-1)
        # one_hot_relative_positions_matrix = torch.nn.functional.one_hot(flat_relative_positions_matrix, num_classes=vocab_size).float()
        # position_embeddings = torch.matmul(one_hot_relative_positions_matrix, embeddings_table)
        # my_shape = list(final_mat.size())
        # my_shape.append(embedding_size)
        # position_embeddings = position_embeddings.view(my_shape)

        # 实现方式2
        # position_embeddings = torch.take_along_dim(embeddings_table, final_mat.flatten().unsqueeze(1), dim=0)
        # position_embeddings = position_embeddings.reshape(*final_mat.shape, embeddings_table.shape[-1])  # [seq_len, seq_len, hdsz]
        # self.register_buffer('position_embeddings', position_embeddings)
        
        # 实现方式3
        position_embeddings = nn.Embedding.from_pretrained(embeddings_table, freeze=True)(final_mat)
        self.register_buffer('position_embeddings', position_embeddings)

    def forward(self, qlen, klen):
        return self.position_embeddings[:qlen, :klen, :]


class RelativePositionsEncodingT5(nn.Module):
    """Google T5的相对位置编码
    来自论文：https://arxiv.org/abs/1910.10683
    """
    def __init__(self, qlen, klen, relative_attention_num_buckets, is_decoder=False):
        super(RelativePositionsEncodingT5, self).__init__()
        # 生成相对位置矩阵
        context_position = torch.arange(qlen, dtype=torch.long)[:, None]
        memory_position = torch.arange(klen, dtype=torch.long)[None, :]
        relative_position = memory_position - context_position  # shape (qlen, klen)
        relative_position = self._relative_position_bucket(
            relative_position,  # shape (qlen, klen)
            bidirectional=not is_decoder,
            num_buckets=relative_attention_num_buckets,
        )
        self.register_buffer('relative_position', relative_position)

    def forward(self, qlen, klen):
        return self.relative_position[:qlen, :klen]

    @staticmethod
    def _relative_position_bucket(relative_position, bidirectional=True, num_buckets=32, max_distance=128):
        '''直接来源于transformer
        '''
        ret = 0
        n = -relative_position
        if bidirectional:
            num_buckets //= 2
            ret += (n < 0).to(torch.long) * num_buckets  # mtf.to_int32(mtf.less(n, 0)) * num_buckets
            n = torch.abs(n)
        else:
            n = torch.max(n, torch.zeros_like(n))
        # now n is in the range [0, inf)

        # half of the buckets are for exact increments in positions
        max_exact = num_buckets // 2
        is_small = n < max_exact

        # The other half of the buckets are for logarithmically bigger bins in positions up to max_distance
        val_if_large = max_exact + (
            torch.log(n.float() / max_exact) / math.log(max_distance / max_exact) * (num_buckets - max_exact)
        ).to(torch.long)
        val_if_large = torch.min(val_if_large, torch.full_like(val_if_large, num_buckets - 1))

        ret += torch.where(is_small, n, val_if_large)
        return ret

class SinusoidalPositionEncoding(nn.Module):
    """定义Sin-Cos位置Embedding
    """
    def __init__(self, max_position, embedding_size):
        super(SinusoidalPositionEncoding, self).__init__()
        position_embeddings = nn.Embedding.from_pretrained(get_sinusoid_encoding_table(max_position, embedding_size), freeze=True)
        self.register_buffer('position_embeddings', position_embeddings)

    def forward(self, position_ids):
        return self.position_embeddings(position_ids)


class RoPEPositionEncoding(nn.Module):
    """旋转式位置编码: https://kexue.fm/archives/8265
    """
    def __init__(self, max_position, embedding_size):
        super(RoPEPositionEncoding, self).__init__()
        position_embeddings = get_sinusoid_encoding_table(max_position, embedding_size)  # [seq_len, hdsz]
        cos_position = position_embeddings[:, 1::2].repeat(1, 2)
        sin_position = position_embeddings[:, ::2].repeat(1, 2)
        self.register_buffer('cos_position', cos_position)
        self.register_buffer('sin_position', sin_position)
    
    def forward(self, qw, seq_len_dim=1):
        dim = len(qw.shape)
        assert (dim >= 2) and (dim <= 4), 'Input units should >= 2 dims(seq_len and hdsz) and usually <= 4 dims'
        seq_len = qw.shape[seq_len_dim]

        if dim == 2:
            qw2 = torch.cat([-qw[:, 1::2], qw[:, ::2]], dim=-1)
            return qw * self.cos_position[:seq_len] + qw2 * self.sin_position[:seq_len]
        if dim == 3:
            qw2 = torch.cat([-qw[:, :, 1::2], qw[:, :, ::2]], dim=-1)
            return qw * self.cos_position[:seq_len].unsqueeze(0) + qw2 * self.sin_position[:seq_len].unsqueeze(0)
        else:
            qw2 = torch.cat([-qw[:, :, :, 1::2], qw[:, :, :, ::2]], dim=-1)
            return qw * self.cos_position[:seq_len].unsqueeze(0).unsqueeze(2) + qw2 * self.sin_position[:seq_len].unsqueeze(0).unsqueeze(2)