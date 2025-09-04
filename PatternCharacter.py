import re

T = 'ఁ-ఃఅ-ళవ-హఽ-్ౘౙౠ-౯'            # Telugu Avoid rare ones: ౚ ఀఄఴ఼౼౷
O = 'ॐ।॥₹\u200c'                # Others
P = '!()+,./0-9:;=?'           # Common Punctuation
Q = r'#$%&*<>@[\\\]^_{|}~'      # Uncommon Punctuation (raw string, no extra escapes)
R = '—‘’“”'                   # Unicode Punctuation
S = r' \n\-\x1E'               # Space
E = 'a-zA-Z'                   # English

X = '"' + r"'`–\t\r"                # Should be replaced with Unicode equivalent

allowed = f'{T}{O}{P}{Q}{R}{S}{E}'
character_pattern = re.compile(f'[{allowed}]')
