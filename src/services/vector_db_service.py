import chromadb
from chromadb.config import Settings

class VectorDBService:
    """
    Manages the Vector Database (ChromaDB) for permanent storage 
    and high-performance semantic retrieval of jobs and courses.
    """

    def __init__(self, path="./chromadb_storage"):
        # Initialize a persistent client so data survives application restarts
        self.client = chromadb.PersistentClient(path=path)
        print(f"--- [DATABASE] Persistent Store Ready at: {path} ---")

    def get_or_create_collection(self, name: str):
        """
        Retrieves an existing collection or creates a new one. 
        Acts like 'Table' initialization in SQL.
        """
        return self.client.get_or_create_collection(name=name)

    def add_data(self, collection_name, ids, documents, embeddings, metadatas=None):
        """
        Inserts vectorized data into the specified collection.
        Automatically handles metadata for filtering during queries.
        """
        collection = self.get_or_create_collection(collection_name)
        
        # Upsert: Update if ID exists, otherwise Insert
        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"--- [STORAGE] Synchronized {len(ids)} records in '{collection_name}' ---")

    def query_similar(self, collection_name, query_embeddings, n_results=3, where_filter=None):
        """
        Executes a K-Nearest Neighbors (KNN) search to find the 
        most semantically relevant documents.
        """
        collection = self.get_or_create_collection(collection_name)
        
        # Validation: Check if collection has data before querying
        if collection.count() == 0:
            print(f"--- [WARNING] Collection '{collection_name}' is empty ---")
            return {"ids": [[]], "distances": [[]], "metadatas": [[]]}

        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where_filter
        )

    def delete_collection(self, name: str):
        """Removes a collection and all its data (Useful for system resets)."""
        try:
            self.client.delete_collection(name=name)
            print(f"--- [CLEANUP] Collection '{name}' deleted ---")
        except Exception as e:
            print(f"--- [ERROR] Delete failed: {e} ---")