from pathlib import Path

from ParseBuild import build_akshara_grams
from PatternAkshara import akshara_pattern
from PatternCharacter import character_pattern

outdir = "models"
Path(outdir).mkdir(exist_ok=True)

#-------------------
# Test Run
#-------------------
if False:
    M, Mt = 10000, "10K"
    build_akshara_grams(character_pattern, f"{outdir}/char_gram_{Mt}", max_docs=M)
    build_akshara_grams(akshara_pattern, f"{outdir}/akshara_gram_{Mt}", max_docs=M)

#-------------------
# Main Run
#-------------------
build_akshara_grams(character_pattern, f"{outdir}/char_gram")
build_akshara_grams(akshara_pattern, f"{outdir}/akshara_gram")