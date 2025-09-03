
from Parse_Build import parse_allowed_unallowed, build_akshara_grams
from PatternAkshara import akshara_pattern
from PatternCharacter import allowed_pattern

outdir = "models"

#-------------------
# Test Run
#-------------------
M, Mt = 10000, "10K"

parse_allowed_unallowed(
    [akshara_pattern, allowed_pattern],
    [f"{outdir}/akshara_{Mt}", f"{outdir}/character_{Mt}"],
    max_docs=M
)
build_akshara_grams(allowed_pattern, f"{outdir}/chargram_{Mt}", max_docs=M)
build_akshara_grams(akshara_pattern, f"{outdir}/akshargram_{Mt}", max_docs=M)

#-------------------
# Main Run
#-------------------
parse_allowed_unallowed(
    [allowed_pattern, akshara_pattern],
    [f"{outdir}/character", f"{outdir}/akshara"],
)

build_akshara_grams(allowed_pattern, f"{outdir}/chargram")
build_akshara_grams(akshara_pattern, f"{outdir}/akshargram")