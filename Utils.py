import csv
import json
from collections import Counter, OrderedDict
from pathlib import Path


def ensure_ext(name, ext):
    file_path = Path(name)
    if not ext.startswith('.'):
        ext = '.' + ext
    return file_path.with_suffix(ext)

#----------------------------------
# Save Counter to JSON file
#----------------------------------
def save_counter_json(counter, filename):
    filename = ensure_ext(filename, 'json')
    with open(filename, 'w') as f:
        json.dump(OrderedDict(counter.most_common()), f, indent=4)
    print("Saved ", filename)

#----------------------------------
# Load Counter from JSON file
#----------------------------------
def load_counter_json(filename):
    with open(filename, 'r') as f:
        return Counter(json.load(f))


#----------------------------------
# Save Counter to CSV file
#----------------------------------
def save_counter_csv(counter, filename, header=('Character', 'Count')):
    filename = ensure_ext(filename, 'csv')
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for char, count in counter.most_common():
            writer.writerow([char, count])
    print("Saved ", filename)

#----------------------------------
# Load Counter from CSV file
#----------------------------------
def load_counter_csv(filename):
    counter = Counter()
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row:  # Check if row is not empty
                counter[row[0]] = int(row[1])
    return counter
