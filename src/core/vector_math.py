import numpy as np

class VectorMath:
    @staticmethod
    def calculate_similarity(v1: list, v2: list):
        np_v1 = np.array(v1)
        np_v2 = np.array(v2)
        
        norm_v1 = np.linalg.norm(np_v1)
        norm_v2 = np.linalg.norm(np_v2)
        
        # صمام أمان: إذا كان أحد المتجهات صفرياً (لا توجد بيانات)، نرجع 0.0 بدلاً من حدوث خطأ Crash
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
            
        dot_product = np.dot(np_v1, np_v2)
        return float(dot_product / (norm_v1 * norm_v2))

    @staticmethod
    def calculate_skill_gap(job_vector: list, user_vector: list):
        # التأكد من أن المتجهات بنفس الطول قبل الطرح
        if len(job_vector) != len(user_vector):
            raise ValueError("Vectors must have the same dimensionality")
        
        np_job = np.array(job_vector)
        np_user = np.array(user_vector)
        
        gap_vector = np_job - np_user
        return gap_vector.tolist()
    @staticmethod
    def calculate_skill_gap(job_vector: list, user_vector: list):
        """
        Calculate the difference between the Job requirements 
        and the User skills.
        Math: Gap = Job_Vector - User_Vector
        """
        np_job = np.array(job_vector)
        np_user = np.array(user_vector)
        
        # The result is a vector pointing to the missing skills
        gap_vector = np_job - np_user
        return gap_vector.tolist()

    @staticmethod
    def calculate_similarity(v1: list, v2: list):
        """
        Calculate how close two vectors are (Cosine Similarity).
        1.0 means identical, 0.0 means completely different.
        """
        np_v1 = np.array(v1)
        np_v2 = np.array(v2)
        
        # Dot product divided by the product of magnitudes
        dot_product = np.dot(np_v1, np_v2)
        norm_v1 = np.linalg.norm(np_v1)
        norm_v2 = np.linalg.norm(np_v2)
        
        return dot_product / (norm_v1 * norm_v2)