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
    if 'ౚ' in ch:   # U+0C5A RRRA
        return True

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


samplerd = SamplerDict("models/akshara_gram.pkl.gz")
trim_low_counts(samplerd.uni, samplerd.bi, samplerd.tri, to_remove)
textd = samplerd.generate_text(["\n"], 10)
print(textd)
