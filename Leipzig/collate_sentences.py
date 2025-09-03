from pathlib import Path

sens = Path(".").rglob('*sentences.txt')
for s in sens:
    print(s, " ", s.stat().st_size/10**6)

output_file = '/tmp/all.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
  for input_file in Path(".").rglob("*sentences.txt"):
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
          try:
            cleaned_line = line.split(' ', 1)[1].strip()
            outfile.write(cleaned_line + '\n')
          except e:
            print(f"Error {e} in {input_file} at...")
            print(cleaned_line)

Path(output_file).stat().st_size/10**6
