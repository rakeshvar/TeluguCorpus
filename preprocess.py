from pathlib import Path

from ParseBuild import count_allowed_unallowed
from PatternAkshara import akshara_pattern
from PatternCharacter import character_pattern

outdir = "counts"
Path(outdir).mkdir(exist_ok=True)

#-------------------
# Test Run
#-------------------
if False:
    M, Mt = 100000, "1L"

    count_allowed_unallowed(
        [akshara_pattern, character_pattern],
        [f"{outdir}/akshara_{Mt}", f"{outdir}/character_{Mt}"],
        max_docs=M
    )


#-------------------
# Main Run
#-------------------
count_allowed_unallowed(
    [character_pattern, akshara_pattern],
    [f"{outdir}/character", f"{outdir}/akshara"],
)
