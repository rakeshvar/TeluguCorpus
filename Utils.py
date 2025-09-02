import csv
import json
from collections import Counter

#----------------------------------
# Save Counter to JSON file
#----------------------------------
def save_counter_json(counter, filename):
    with open(filename, 'w') as f:
        json.dump(dict(counter), f, indent=4)

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
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for char, count in counter.most_common():
            writer.writerow([char, count])

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
