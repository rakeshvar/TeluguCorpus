import re

T = '\u0C00-\u0C7f'            # Telugu
O = 'ॐ।॥₹\u200C'                # Others
P = '!()+,./0-9:;=?'           # Common Punctuation
Q = r'#$%&*<>@[\\\]^_`{|}~'      # Uncommon Punctuation (raw string, no extra escapes)
R = '–—‘’“”'                   # Unicode Punctuation
S = r' \n'                     # Space
E = 'a-zA-Z'                   # English

X = r"""'"`\-\t\r"""                # Should be replaced with Unicode equivalent

allowed = f'{T}{O}{P}{Q}{R}{S}{E}'
allowed_pattern = re.compile(f'[{allowed}]')
not_allowed_pattern = re.compile(f'[^{allowed}]')

print("Allowed Char Pattern: ", allowed)
print("Allowed re Pattern:", allowed_pattern)