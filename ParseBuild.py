from collections import Counter, namedtuple
from tqdm import tqdm

import Data
import Utils
from Cleaner import clean_text
from Sampler import SamplerMat, SamplerDict
from TriGram import TriGram
from Unicode import print_char_counts

#--------------------------------------
# Pattern Matching and finding hits and misses
#--------------------------------------
def match_pattern_simple(text, pattern):
    matches = []
    for match in pattern.finditer(text):
        matches.append(match.group())
    matches.append('\n')                # Standardize single \n at EOL
    return matches

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
        last_end = end
        matched.append(match_text)

    if last_end < len(text):
        missed_text = text[last_end:len(text)]
        missed.append(missed_text)

    return matched, missed


def count_allowed_unallowed(patterns, out_heads, max_docs=None, clean=False, save_csv=False):
    Result = namedtuple('Result', ['allowed', 'unallowed', 'unallowedchar'])
    results = [Result(allowed=Counter(),
                      unallowed=Counter(),
                      unallowedchar=Counter()) for _ in patterns]

    for i, d in enumerate(tqdm(Data.DataLoader(max_docs), desc="Parsing Patterns of Data")):
        if clean:
            d = clean_text(d)
        for patt, result in zip(patterns, results):
            tt, ot = match_pattern(d, patt)
            result.allowed.update(tt)
            result.unallowed.update(ot)
            result.unallowedchar.update("".join(ot))

    for result, out_head in zip(results, out_heads):
        if save_csv:
            Utils.save_counter_csv(result.allowed, out_head + '_allowed', ['AllowedChar', 'Count'])
            Utils.save_counter_csv(result.unallowed, out_head + '_unallowed', ['UnallowedChar', 'Count'])
            Utils.save_counter_csv(result.unallowedchar, out_head + '_unallowedchar', ['UnallowedChar', 'Count'])
        Utils.save_counter_json(result.allowed, out_head + '_allowed')
        Utils.save_counter_json(result.unallowed, out_head + '_unallowed')
        Utils.save_counter_json(result.unallowedchar, out_head + '_unallowedchar')

#--------------------------------------
# Counts
#--------------------------------------
def count_chars(max_docs):
    char_counts = Counter()
    for d in Data.DataLoader(max_docs):
        char_counts.update(d)
    print_char_counts(char_counts)
    Utils.save_counter_json(char_counts, "char_counts.json")
    Utils.save_counter_csv(char_counts, "char_counts.csv")

#--------------------------------------
# Make the TriGram
#--------------------------------------
def build_akshara_grams(patt, outhead, max_docs=None):
    print("\nBuilding trigram using pattern: ", patt)
    model = TriGram()
    data = Data.DataLoader(max_docs)

    for d in tqdm(data, desc="Feeding text to Trigram"):
        d = clean_text(d)
        tel = match_pattern_simple(d, patt)
        if len(tel) > 1:
            model.process_text(tel)

    model.save_dicts(outhead)
    model.convert_to_mat()
    model.save_mats_to_npz(outhead)
