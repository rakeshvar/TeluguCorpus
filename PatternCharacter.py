import re

T = '\u0C00-\u0C7f'            # Telugu
O = 'ॐ।॥₹\u200C'                # Others
P = '!()+,./0-9:;=?'           # Common Punctuation
Q = r'#$%&*<>@[\\\]^_`{|}~'    # Uncommon Punctuation
R = '–—‘’“”'                   # Unicode Punctuation
S = r' \n'                     # Space
E = '[a-zA-Z]'                   # English

X = r'"\'`\-\t\r'                # Should be replaced with Unicode equivalent

allowed = rf'{T}{O}{P}{Q}{R}{S}{E}'
allowed_pattern = re.compile(rf'[{allowed}]')
not_allowed_pattern = re.compile(rf'[^{allowed}]')

