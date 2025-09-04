import re

T = '\u0c00-\u0c7f'            # Telugu
O = 'ॐ।॥₹\u200c'                # Others
P = '!()+,./0-9:;=?'           # Common Punctuation
Q = r'#$%&*<>@[\\\]^_{|}~'      # Uncommon Punctuation (raw string, no extra escapes)
R = '—‘’“”'                   # Unicode Punctuation
S = r' \n\-'                     # Space
E = 'a-zA-Z'                   # English

X = '"' + r"'`–\t\r"                # Should be replaced with Unicode equivalent

allowed = f'{T}{O}{P}{Q}{R}{S}{E}'
character_pattern = re.compile(f'[{allowed}]')

print("Allowed Character Pattern: ", allowed)
print("\t Compiled: ", character_pattern)