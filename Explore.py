from collections import Counter

import Data
import Utils
from Unicode import print_char_set, print_char_counts

data = Data.OSCAR()

def show_chars():
    char_set = set()
    for d in data:
        char_set.update(d)
    print_char_set(char_set)

def count_chars():
    char_counts = Counter()
    for d in data:
        char_counts.update(d)
    print_char_counts(char_counts)
    Utils.save_counter_json(char_counts, "char_counts.json")
    Utils.save_counter_csv(char_counts, "char_counts.csv")
