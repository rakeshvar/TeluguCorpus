from pathlib import Path

from Parse_Build import match_pattern, parse_allowed_unallowed, build_akshara_grams
from PatternAkshara import akshara_pattern
from PatternCharacter import allowed_pattern


def test_parse(patt, *, text=None, file=None):
    if text is None:
        text = Path(file).read_text(encoding='utf-8', errors="ignore")

    tt, ot = match_pattern(text, patt)
    print("Allowed  Telugu Text: ", tt)
    print("Unallowed Other Text: ", ot)


parse_allowed_unallowed(
    [akshara_pattern, allowed_pattern],
    ["akshara", "character"],
    max_docs=100
)

build_akshara_grams(allowed_pattern, "chargram100", num_docs=100)
build_akshara_grams(akshara_pattern, "akshargram100", num_docs=100)
build_akshara_grams(allowed_pattern, "chargram")
build_akshara_grams(akshara_pattern, "akshargram")