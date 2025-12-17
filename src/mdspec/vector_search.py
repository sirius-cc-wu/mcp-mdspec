import chromadb
from sentence_transformers import SentenceTransformer

class VectorSearch:
    def __init__(self):
        self.client = chromadb.Client()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("specs")

    def index_specs(self, specs: list):
        """
        Indexes a list of specs.
        Each spec is a dictionary with 'path' and 'content' keys.
        """
        for spec in specs:
            self.collection.add(
                documents=[spec['content']],
                metadatas=[{"path": spec['path']}],
                ids=[spec['path']]
            )

    def search(self, query: str, n_results: int = 5) -> list:
        """
        Searches for a query in the indexed specs.
        """
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

