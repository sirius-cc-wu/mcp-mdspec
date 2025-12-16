import chromadb
from sentence_transformers import SentenceTransformer

class VectorSearch:
    def __init__(self):
        self.client = chromadb.Client()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("notes")

    def index_notes(self, notes: list):
        """
        Indexes a list of notes.
        Each note is a dictionary with 'path' and 'content' keys.
        """
        for note in notes:
            self.collection.add(
                documents=[note['content']],
                metadatas=[{"path": note['path']}],
                ids=[note['path']]
            )

    def search(self, query: str, n_results: int = 5) -> list:
        """
        Searches for a query in the indexed notes.
        """
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

