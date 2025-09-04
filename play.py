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

def to_remove(ch, count):
    return count < 5 or len(ch) > 5

samplerd = SamplerDict("models/aksharagram.pkl.gz")
trim_low_counts(samplerd.uni, samplerd.bi, samplerd.tri, to_remove)
textd = samplerd.generate_text(["\n"], 10000)
print(textd)
