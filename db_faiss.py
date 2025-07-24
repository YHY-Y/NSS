import faiss
import numpy as np
import json
from .embedding import get_embedding

class NovelDB:
    def __init__(self, data_path):
        self.data = []
        self.embeddings = []
        self.ids = []
        with open(data_path, encoding='utf-8') as f:
            self.data = json.load(f)
        for item in self.data:
            emb = get_embedding(item['intro'])
            self.embeddings.append(emb)
            self.ids.append(item['id'])
        self.embeddings = np.vstack(self.embeddings).astype('float32')
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query, top_k=5):
        q_emb = get_embedding(query).astype('float32')
        D, I = self.index.search(np.expand_dims(q_emb, 0), top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            item = self.data[idx]
            results.append({
                'id': item['id'],
                'title': item['title'],
                'intro': item['intro'],
                'url': item['url'],
                'score': float(-dist) # L2 거리이므로 음수로 변환
            })
        return results 