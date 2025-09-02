import re
from collections import Counter

import Data
import Utils
from Cleaner import clean
from Sampler import SamplerMat, SamplerDict
from TriGram import TriGram

def parse(text, pattern):
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

def test_parse(patt, text = "ఉఁకగఃరిలుంక్రత్తంమత్స్యంకృత్స్న సాఫ్ట్‌వేర్ గ్ం (abc123) #x $99.9 [?] ఽ।॥ ₹౩౨,౫"):
    tt, ot = parse(text, patt)
    print("Allowed  Telugu Text: ", tt)
    print("Unallowed Other Text: ", ot)


def build_akshara_grams(patt,
                        gz_out = "akshara_grams.pkl.gz",
                        npz_out = "akshara_grams.npz"):
    model = TriGram()
    data = Data.OSCAR()
    spurious = Counter()

    for d in data:
        d = clean(d)
        tel, oth = parse(d, patt)
        model.process_text(tel)
        spurious.update(oth)

    model.convert_to_mat()
    model.save_dicts(gz_out)
    model.save_mats_to_npz(npz_out)
    Utils.save_counter_csv(spurious, "spurious_aksharas.csv")


def test_gen(gz_in = "akshara_grams.pkl.gz",
             npz_in = "akshara_grams.npz",
             nchars=200):
    samplerd = SamplerDict(gz_in)
    samplerm = SamplerMat(npz_in)

    textd = samplerd.generate_text(["\n"], nchars)
    textm = samplerm.generate_text([samplerm.stoi("\n")], nchars)

    perpd = samplerm.perplexity(textd)
    perpm = samplerm.perplexity(textm)

    print(f"Text: {textd}\nPerplexity: {perpd:6.4f}")
    print(f"Text: {textm}\nPerplexity: {perpm:6.4f}")
