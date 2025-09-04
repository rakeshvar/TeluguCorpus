from ParseBuild import build_akshara_grams
from PatternAkshara import akshara_pattern
from PatternCharacter import character_pattern

outdir = "models"


#-------------------
# Test Run
#-------------------
if False:
    M, Mt = 10000, "10K"
    build_akshara_grams(character_pattern, f"{outdir}/chargram_{Mt}", max_docs=M)
    build_akshara_grams(akshara_pattern, f"{outdir}/akshargram_{Mt}", max_docs=M)

#-------------------
# Main Run
#-------------------
build_akshara_grams(character_pattern, f"{outdir}/chargram")
build_akshara_grams(akshara_pattern, f"{outdir}/akshargram")