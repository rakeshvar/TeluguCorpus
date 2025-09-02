from collections import Counter

import Data
from Sampler import SamplerMat, SamplerDict
from TriGram import TriGram
from Cleaner import clean
from Unicode import print_char_set, print_char_counts

data = Data.OSCAR()
model = TriGram()

def show_chars():
    char_set = set()
    for d in data:
        char_set.update(d)
    print_char_set(char_set)

def count_chars():
    char_counts = Counter()
    for d in data:
        char_counts.update(d)
    print_char_counts(char_counts)


for d in data:
    d = clean(d)
    model.process_text(d)

model.convert_to_mat()
model.save_dicts("grams.pkl.gz")
model.save_mats_to_npz("grams.npz")

samplermat = SamplerMat("grams.npz")
samplerdict = SamplerDict("grams.pkl.gz")

textmat = samplermat.generate_text([0], 100)
textdict = samplerdict.generate_text([0], 100)

perpmat = samplermat.perplexity(textmat)
perpdict = samplermat.perplexity(textdict)
