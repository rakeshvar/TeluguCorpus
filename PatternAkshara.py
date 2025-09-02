import re

#---------------------------------------------------------------------
A = '[అ-ఔౠౡ]'                 # acculu
H = '[క-హ]'                      # hallulu
U = '[ఁంః]'                    # ubhayamulu
M = '[ా-ౌౢౣ]'                   #  maatralu
V = '[్]'                       # viramam
MV ='[ా-ౌౢౣ్]'                   # matralu, viramam
N = '[౦-౯]'                     # Numbers
O = '[ॐ।॥₹\u200C]'                # Others
P = '[!()+,./0-9:;=?]'           # Common Punctuation
Q = r'[#$%&*<>@[\\\]^_`{|}~]'    # Uncommon Punctuation
X = '["\'`-\t\r]'                # Should be replaced with Unicode equivalent
R = '[–—‘’“”]'                   # Unicode Punctuation
S = r'[ \n]'                     # Space
E = '[a-zA-Z]'                   # English

akshara = (f"{U}|{A}|{N}|{P}|{O}|{S}|{E}|{Q}|"        # Individuals
           f"{H}(?:{V}{H})*{M}|"                      # Compounds with matra
           f"(?:{H}{V})+(?!{H})|"                     # Compounds with virama
           f"{H}(?:{V}{H})*(?!{MV})")                 # Compounds without matra

print("Pattern: ", akshara)
akshara_pattern = re.compile(akshara)

#-------------------------------------------------------------
