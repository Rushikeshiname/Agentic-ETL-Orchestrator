import faiss
import numpy as np

class TransformMemory:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.transforms = []

    def add_transform(self, embedding, transform_code):
        vec = np.array([embedding]).astype("float32")
        self.index.add(vec)
        self.transforms.append(transform_code)

    def search(self, embedding, k=1):
        vec = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(vec, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.transforms):
                results.append(self.transforms[idx])

        return results

memory = TransformMemory()