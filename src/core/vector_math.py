import numpy as np

class VectorMath:
    """
    Core mathematical operations for analyzing skills using vectors.
    This class handles the logic of finding the 'Gap' between 
    a user and a job.
    """

    @staticmethod
    def calculate_mean_vector(vectors: list):
        """
        Calculate the average (mean) of multiple vectors.
        This represents the 'Average Professional Identity' of a user.
        """
        # Convert list to a numpy array for mathematical operations
        np_vectors = np.array(vectors)
        # Calculate the mean across the first axis
        mean_vector = np.mean(np_vectors, axis=0)
        return mean_vector.tolist()

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