from sentence_transformers import SentenceTransformer
import logging

class EmbeddingService:
    """
    Service to convert text into numerical vectors (embeddings) 
    using a local Transformer model. 
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # 1. تهيئة المتغير بـ None لضمان وجوده في الذاكرة ومنع AttributeError
        self.model = None
        
        print(f"--- [AI MODEL] Loading Transformer: {model_name} ---")
        try:
            # 2. تحميل النموذج وتخزينه في self.model
            self.model = SentenceTransformer(model_name)
            print(f"--- [AI MODEL] Ready for Vectorization ---")
        except Exception as e:
            # 3. تسجيل الخطأ ورفعه لمنع النظام من العمل بحالة غير مستقرة
            print(f"--- [ERROR] Failed to load model: {e} ---")
            raise RuntimeError(f"Critical Error: AI Model could not be loaded. {e}")

    def generate_vector(self, text: str):
        """
        Converts a single text input into a high-dimensional vector.
        """
        # 4. تحقق أمان إضافي قبل استخدام النموذج
        if self.model is None:
            raise AttributeError("EmbeddingService.model is not initialized. Check logs for loading errors.")

        if not text or not text.strip():
            # إرجاع متجه صفري بالأبعاد الصحيحة (عادة 384 للنموذج المستخدم)
            dim = self.model.get_sentence_embedding_dimension()
            return [0.0] * dim
            
        return self.model.encode(text).tolist()

    def generate_vectors_batch(self, texts: list[str]):
        """
        Processes multiple documents efficiently.
        """
        if self.model is None:
            raise AttributeError("EmbeddingService.model is not initialized.")

        if not texts:
            return []
            
        safe_texts = [t if (t and t.strip()) else "" for t in texts]
        return self.model.encode(safe_texts).tolist()