from datasets import load_dataset

leipzig_txt = "Corpus_Leipzig/leipzig.txt"
eemaata_txt = "Corpus_Eemaata/eemaata.txt"
files = [
    leipzig_txt,
    eemaata_txt
]

# TODO: Make it take the list of files as args along with max_docs
class DataLoader:
    def __init__(self, max_docs=None):
        self.max_docs = max_docs
        self.contents = []
        for file in files:
            with open(file, "r", encoding='utf-8') as fp:
                self.contents.extend(fp.readlines())

    def __iter__(self):
        for i, line in enumerate(self.contents):
            if self.max_docs is not None and i >= self.max_docs:
                break
            yield line

    def __getitem__(self, idx):
        if self.max_docs is not None and idx >= self.max_docs:
            raise IndexError("Index out of range")
        return self.contents[idx]

    def __len__(self):
        if self.max_docs is not None:
            return min(self.max_docs, len(self.contents))
        else:
            return len(self.contents)


class OSCAR:
    def __init__(self, max_docs=None, seed=42, streaming=True):
        print(f"Loading OSCAR Telugu dataset...")
        self.dataset = load_dataset("oscar-corpus/OSCAR-2301",
                                    use_auth_token=True,
                                    language="te",  # Fixed to Telugu
                                    streaming=streaming)
        self.dataset = self.dataset.shuffle(seed=seed)
        if not streaming and max_docs is not None:
            self.dataset = self.dataset.select(range(max_docs))

        self.max_docs = max_docs
        self.streaming = streaming
        self.current_count = 0

    def __iter__(self):
        self.current_count = 0
        for example in self.dataset:
            if self.max_docs is not None and self.current_count >= self.max_docs:
                break
            yield example['text']
            self.current_count += 1

    def __getitem__(self, idx):
        return self.dataset[idx]['text']

    def __len__(self):
        """Return the number of documents"""
        if self.streaming:
            if self.max_docs is not None:
                return self.max_docs
            else:
                raise TypeError("Length not available for streaming mode without max_docs")
        else:
            return len(self.dataset)


#OSCAR(max_docs=100, seed=42, streaming=True)
#OSCAR(streaming=False)
