from datasets import load_dataset

class OSCAR:
    def __init__(self):
        print(f"Loading OSCAR Telugu dataset...")
        self.dataset = load_dataset("oscar-corpus/OSCAR-2301",
                               use_auth_token=True,  # required
                               language="te",
                               streaming=True,  # optional
                               split="train")  # optional

    def __iter__(self):
        for d in self.dataset:
            yield d['text']

    def get_some(self, num_samples):
        texts = []
        for i, example in enumerate(self.dataset):
            if i >= num_samples:
                break
            texts.append(example['text'])
        return texts

