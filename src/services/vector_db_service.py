import chromadb
from chromadb.config import Settings


class VectorDBService:
    """
    Service to manage ChromaDB operations: Creating collections, 
    adding data, and performing semantic searches.
    """

    def __init__(self, path="./chromadb_storage"):
        # Connect to ChromaDB and ensure data is saved permanently in the path folder
        self.client = chromadb.PersistentClient(path=path)
        print(f"--- ChromaDB initialized at: {path} ---")

    def get_or_create_collection(self, name: str):
        # Collections are like tables in a database
        return self.client.get_or_create_collection(name=name)

    def add_data(self, collection_name, ids, documents, embeddings, metadatas=None):
        # Add text, its vector, and additional info (metadata) to the DB
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"--- Added {len(ids)} items to collection: {collection_name} ---")

    def query_similar(self, collection_name, query_embeddings, n_results=3, where_filter=None):
        # Perform a semantic search using the vector
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where_filter
        )