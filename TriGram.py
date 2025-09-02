import gzip
import pickle
from collections import defaultdict, Counter
import numpy as np

from Utils import ensure_ext


class TriGram():
    def __init__(self):
        self.uni = Counter()
        self.bi = defaultdict(Counter)
        self.tri = defaultdict(lambda : defaultdict(Counter))

    def process_text(self, text):
        for i in range(len(text)-2):
            s, t, u = text[i:(i+3)]
            self.uni[s] += 1
            self.bi[s][t] += 1
            self.tri[s][t][u] += 1

        s, t = text[-2:]
        self.uni[s] += 1
        self.uni[t] += 1
        self.bi[s][t] += 1

    def convert_to_mat(self):
        v = len(self.uni)
        stoi = dict((k, i) for i, k in enumerate(sorted(self.uni.keys())))

        self.vocab_size = v
        self.stoi = stoi
        self.unimat = np.zeros(v, dtype=np.int32)
        self.bimat =  np.zeros((v, v), dtype=np.int32)
        self.trimat = np.zeros((v, v, v), dtype=np.int32)

        for s, count in self.uni.items():
            self.unimat[stoi[s]] = count

        for s, counts in self.bi.items():
            for t, count in counts.items():
                self.bimat[stoi[s], stoi[t]] = count

        for s, dfc in self.tri.items():
            for t, counts in dfc.items():
                for u, count in counts.items():
                    self.trimat[stoi[s], stoi[t], stoi[u]] = count

    def save_dicts(self, filename):
        filename = ensure_ext(filename, "pkl.gz")
        with gzip.open(filename, 'wb') as f:
            pickle.dump({
                'uni': self.uni,
                'bi': self.bi,
                'tri': self.tri
            }, f)

    def save_mats_to_npz(self, out_path):
        out_path = ensure_ext(out_path, "npz")
        chars, indices = zip(*self.stoi.items())
        np.savez_compressed(
            out_path,
            uni=self.unimat,
            bi=self.bimat,
            tri=self.trimat,
            chars=np.array(chars),
            indices=np.array(indices)
        )

    @classmethod
    def load_dicts(cls, filename):
        with gzip.open(filename, 'rb') as f:
            data = pickle.load(f)
            return data['uni'], data['bi'], data['tri']

    @classmethod
    def load_mats_from_npz(cls, filename):
        data = np.load(filename, allow_pickle=True)
        return data['uni'], data['bi'], data['tri'], data['chars'], data['indices']
