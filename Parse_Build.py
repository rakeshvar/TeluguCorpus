from collections import Counter, namedtuple

import Data
import Utils
from Cleaner import clean
from Sampler import SamplerMat, SamplerDict
from TriGram import TriGram
from Unicode import print_char_counts

#--------------------------------------
# Pattern Matching and finding hits and misses
#--------------------------------------
def match_pattern(text, pattern):
    matched, missed = [], []
    i, last_end = 0, 0

    for match in pattern.finditer(text):
        i += 1
        match_text = match.group()
        start, end = match.start(), match.end()
        if start > last_end:
            missed_text = text[last_end:start]
            missed.append(missed_text)
            print("Missed: ", missed_text)
        last_end = end
        matched.append(match_text)

    if last_end < len(text):
        missed_text = text[last_end:len(text)]
        missed.append(missed_text)

    return matched, missed


def parse_allowed_unallowed(patterns, out_heads, num_docs=9**9):
    Result = namedtuple('Result', ['allowed', 'unallowed'])
    results = [Result(allowed=Counter(), unallowed=Counter()) for _ in patterns]

    for i, d in enumerate(Data.OSCAR(num_docs)):
        for patt, result in zip(patterns, results):
            tt, ot = match_pattern(d, patt)
            result.allowed.update(tt)
            result.unallowed.update(ot)

    for result, out_head in zip(results, out_heads):
        Utils.save_counter_csv(result.allowed, out_head + '_allowed', ['AllowedChar', 'Count'])
        Utils.save_counter_json(result.allowed, out_head + '_allowed')
        Utils.save_counter_csv(result.unallowed, out_head + '_unallowed', ['UnallowedChar', 'Count'])
        Utils.save_counter_json(result.unallowed, out_head + '_unallowed')

#--------------------------------------
# Counts
#--------------------------------------
def count_chars(num_docs):
    char_counts = Counter()
    for d in Data.OSCAR(num_docs):
        char_counts.update(d)
    print_char_counts(char_counts)
    Utils.save_counter_json(char_counts, "char_counts.json")
    Utils.save_counter_csv(char_counts, "char_counts.csv")

#--------------------------------------
# Make the TriGram
#--------------------------------------
def build_akshara_grams(patt, outhead, num_docs=9**9):
    model = TriGram()
    data = Data.OSCAR(num_docs)
    spurious = Counter()

    for d in data:
        d = clean(d)
        tel, oth = match_pattern(d, patt)
        model.process_text(tel)
        spurious.update(oth)

    model.convert_to_mat()
    model.save_dicts(outhead)
    model.save_mats_to_npz(outhead)
    Utils.save_counter_csv(spurious, "spurious_" + outhead)


#--------------------------------------
# Generate from TriGram
#--------------------------------------
def test_gen(gz_in, npz_in, nchars=200):
    samplerd = SamplerDict(gz_in)
    samplerm = SamplerMat(npz_in)

    textd = samplerd.generate_text(["\n"], nchars)
    textm = samplerm.generate_text([samplerm.stoi("\n")], nchars)

    perpd = samplerm.perplexity(textd)
    perpm = samplerm.perplexity(textm)

    print(f"Text: {textd}\nPerplexity: {perpd:6.4f}")
    print(f"Text: {textm}\nPerplexity: {perpm:6.4f}")
