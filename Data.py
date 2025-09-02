import random
from datasets import load_dataset
from datasets import load_dataset


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
