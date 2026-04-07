from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """
    Service to convert text into numerical vectors using a free, 
    local model from Sentence-Transformers.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initialize the model. It will download to your PC only once.
        print(f"--- Initializing Free Model: {model_name} ---")
        self.model = SentenceTransformer(model_name)

    def generate_vector(self, text: str):
        # Convert a single string into a list of numbers (Vector)
        # We use .tolist() because ChromaDB expects a standard Python list
        return self.model.encode(text).tolist()

    def generate_vectors_batch(self, texts: list[str]):
        # Convert a list of strings into a list of vectors efficiently
        return self.model.encode(texts).tolist()