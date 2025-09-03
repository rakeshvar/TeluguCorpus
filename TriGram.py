import gzip
import pickle
from collections import defaultdict, Counter
import numpy as np

from Utils import ensure_ext


class TriGram():
    def __init__(self):
        self.uni = Counter()
        self.bi = defaultdict(Counter)
        self.tri = dict()

    def addtotri(self, s, t, u, v=1):   # This way self.tri can be pickled
        if s not in self.tri:
            self.tri[s] = defaultdict(Counter)
        self.tri[s][t][u] += v

    def process_text(self, text):
        for i in range(len(text)-2):
            s, t, u = text[i:(i+3)]
            self.uni[s] += 1
            self.bi[s][t] += 1
            self.addtotri(s, t, u)

        try:
            s, t = text[-2:]
            self.uni[s] += 1
            self.uni[t] += 1
            self.bi[s][t] += 1
        except:
            print("Bad text: ", text)

    def convert_to_mat(self):
        v = len(self.uni)
        stoi = dict((k, i) for i, k in enumerate(sorted(self.uni.keys())))

        self.vocab_size = v
        self.stoi = stoi

        self.unimat = np.zeros(v, dtype=np.int32)
        for s, count in self.uni.items():
            self.unimat[stoi[s]] = count

        self.bimat =  np.zeros((v, v), dtype=np.int32)
        for s, counts in self.bi.items():
            for t, count in counts.items():
                self.bimat[stoi[s], stoi[t]] = count

        try:
          self.trimat = np.zeros((v, v, v), dtype=np.int32)
          for s, dfc in self.tri.items():
            for t, counts in dfc.items():
                for u, count in counts.items():
                    self.trimat[stoi[s], stoi[t], stoi[u]] = count
        except Exception as e:
            print("Could not save Trigram. Got Error:\n", e)

    def save_dicts(self, filename):
        filename = ensure_ext(filename, "pkl.gz")
        with gzip.open(filename, 'wb') as f:
            pickle.dump({
                'uni': self.uni,
                'bi': self.bi,
                'tri': self.tri
            }, f)
        print("Saved ", filename)

    def save_mats_to_npz(self, out_path):
        out_path = ensure_ext(out_path, "npz")
        chars, indices = zip(*self.stoi.items())
        try:
            trimat = self.trimat
        except:
            trimat = None
        np.savez_compressed(
            out_path,
            uni=self.unimat,
            bi=self.bimat,
            tri=trimat,
            chars=np.array(chars),
            indices=np.array(indices)
        )
        print("Saved ", out_path)

    @classmethod
    def load_dicts(cls, filename):
        with gzip.open(filename, 'rb') as f:
            data = pickle.load(f)
            return data['uni'], data['bi'], data['tri']

    @classmethod
    def load_mats_from_npz(cls, filename):
        data = np.load(filename, allow_pickle=True)
        return data['uni'], data['bi'], data['tri'], data['chars'], data['indices']
