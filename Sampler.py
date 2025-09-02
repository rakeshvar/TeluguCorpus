import random
import numpy as np

from TriGram import TriGram

class SamplerMat():
    def __init__(self, npzfile:str):
        assert npzfile.endswith('.npz'), "Should give an npz file"
        self.unimat, self.bimat, self.trimat, self.chars, self.indices = TriGram.load_mats_from_npz(npzfile)
        self.stoi = dict(zip(self.chars, self.indices))
        self.itos = dict(zip(self.indices, self.chars))

        self.uniprobs = self.unimat.astype(np.float32) / self.unimat.sum()
        self.biprobs = self.bimat.astype(np.float32) / self.bimat.sum(axis=(0, 1), keepdims=True)  # +1 ?
        self.triprobs = self.trimat.astype(np.float32) / self.trimat.sum(axis=2, keepdims=True)
        self.vocab_size = self.uniprobs.shape[0]

    def next_char_bi(self, a):
        return np.random.choice(self.vocab_size, size=1, p=self.biprobs[a])

    def next_char_tri(self, a, b):
        return np.random.choice(self.vocab_size, size=1, p=self.triprobs[a, b])

    def generate_text(self, init, length):
        len1 = len(init)

        if len(init) == 0:
            init = [0]  # Todo: self.begin
            length -= 1

        if len(init) == 1:
            init = [init[0], self.next_char_bi(init[0])]
            length -= 1

        ret = np.zeros((len1 + length,), dtype=np.int8)
        ret[:length(init)] = init

        j = length(init)
        for j in range(len(init), len(init)+length):
            ret[j] = self.next_char_tri(*ret[-2:])

        return ret

    def perplexity(self, text: str) -> float:
        if len(text) < 3:
            return float('inf')

        total_log_prob = 0.0
        tokens = self.tokenize(text)
        len2 = len(tokens) - 2

        for i in range(len2):
            s, t, u = tokens[i:(i+3)]
            prob = self.triprobs[s, t, u]
            if prob > 0:
                total_log_prob += np.log(prob)
            else:
                total_log_prob += -np.inf
                print(f"Warning: Probability should be positive. Check tri[{s}, {t}, {u}] = {prob}")

        return np.exp(-total_log_prob/len2)

    def tokenize(self, text:str) -> list:
        return [self.stoi[s] for s in text]


class SamplerDict():
    def __init__(self, gzfile):
        assert gzfile.endswith('.pkl.gz'), "Should given a gz file"
        self.uni, self.bi, self.tri = TriGram.load_dicts(gzfile)

    def next_char_uni(self):
        k, v = zip(*self.uni)
        return random.choices(k, weights=v, k=1)

    def next_char_bi(self, a):
        k, v = zip(*self.bi[a].items())
        return random.choices(k, weights=v, k=1)

    def next_char_tri(self, a, b):
        k, v = zip(*self.tri[a][b].items())
        return random.choices(k, weights=v, k=1)

    def generate_text(self, init, length):
        if len(init) == 0:
            init = [0]  # Todo: [self.begtoken]

        if len(init) == 1:
            init.append(self.next_char_bi(init[0]))

        for i in range(length):
            init.append(self.next_char_tri(*init[-2:]))

        return init
