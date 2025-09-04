import os
from collections import OrderedDict

from bs4 import BeautifulSoup
from tqdm import tqdm

input_dir = "../articles"
output_file = "eemaata_articles_sections.csv"

with open(output_file, "w", encoding="utf-8") as out:
    for filename in tqdm(sorted(os.listdir(input_dir))):
        if not filename.endswith(".html"):
            continue

        input_path = os.path.join(input_dir, filename)
        with open(input_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Find all divs (or other relevant tags)
        elements = soup.find_all(["div", "article", "section", "main"])

        # Extract text and compute sizes
        element_sizes = {}
        for elem in elements:
            text = elem.get_text(separator=" ", strip=True)
            size = len(text)
            if size > 0:  # Ignore empty elements
                # Try to get an identifier (class, id, or tag)
                identifier = (
                        elem.get("id", "") or
                        elem.get("class", [""])[0] or
                        elem.name
                )
                element_sizes[identifier] = size

        # Sort by size (descending)
        element_sizes = OrderedDict(sorted(element_sizes.items(), key=lambda x: x[1], reverse=True))

        # Total size of all text
        total_size = sum(element_sizes.values())

        # Write to out.info
        line = f"{filename},{total_size}"
        for identifier, size in element_sizes.items():
            line += f",{identifier},{size}"
        out.write(line + "\n")

        if 'entry-content' not in element_sizes:
            print(f"{filename} does not have entry-content")

print(f"Analysis complete. Results saved to {output_file}.")