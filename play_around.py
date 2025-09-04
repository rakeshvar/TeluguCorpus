from Sampler import SamplerDict, SamplerMat
from Trim import trim_low_counts


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

#--------------------------------------

def to_remove(ch:str, count:int) -> bool:
    if count > 108:  # Too frequent
        return False

    if '్' not in ch:  # Remove only conjuncts
        return False

    if count < 5:
        return True

    if len(ch) > 4:
        print(f"Removing {ch} of len {len(ch)} with count {count}.")
        return True
    
    return False

#--------------------------------------
import argparse
parser = argparse.ArgumentParser(description="Create a sample text from a tri-gram model.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-G", "--gram", type=str, default="models/akshara_gram.pkl.gz", help="Path to the saved trigram model")
parser.add_argument("-N", "--len", type=int, default=100, help="Length of string to be generated.")
args = parser.parse_args()

samplerd = SamplerDict(args.gram)
trim_low_counts(samplerd.uni, samplerd.bi, samplerd.tri, to_remove)
textd = samplerd.generate_text(["\n"], args.len)
print(textd)
