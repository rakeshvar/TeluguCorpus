import re

#---------------------------------------------------------------------
A = '[అ-ఔౠౡ]'                 # acculu
H = '[క-ళవ-హ]'                   # hallulu (Avoid ఴ, ౚ)
U = '[ఁంః]'                    # ubhayamulu
M = '[ా-ౌౢౣ]'                   #  maatralu
V = '[్]'                       # viramam
MV ='[ా-ౌౢౣ్]'                   # matralu, viramam
N = '[౦-౯]'                     # Numbers
O = '[ॐ।॥₹\u200C]'                # Others
P = '[!()+,./0-9:;=?]'           # Common Punctuation
Q = r'[#$%&*<>@[\\\]^_`{|}~]'    # Uncommon Punctuation
X = '["\'`-\t\r]'                # Should be replaced with Unicode equivalent
R = '[-—‘’“”]'                   # Unicode Punctuation
S = r'[ \n]'                     # Space
E = '[a-zA-Z]'                   # English
Z = '[ౘౙఽ]'

akshara = (f"{U}|{A}|{N}|{O}|{P}|{Q}|{R}|{S}|{E}|{Z}|" # Individuals
           f"{H}(?:{V}{H})*{M}|"                       # Compounds with matra
           f"(?:{H}{V})+(?!{H})|"                      # Compounds with virama
           f"{H}(?:{V}{H})*(?!{MV})")                  # Compounds without matra
akshara_pattern = re.compile(akshara)
