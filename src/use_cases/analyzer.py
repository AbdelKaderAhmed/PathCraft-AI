from src.core.vector_math import VectorMath

class SkillGapAnalyzer:
    """
    This use case orchestrates the entire analysis process:
    1. Embeds User CV and Job Description.
    2. Calculates the gap vector.
    3. Finds the matching percentage.
    """

    def __init__(self, embedding_service, vector_db_service):
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.math = VectorMath()

    def analyze_user_vs_job(self, user_cv_text, job_id, collection_name="jobs"):
        """
        Main logic to compare a user's CV against a specific job stored in DB.
        """
        # 1. Convert User CV to Vector
        user_vector = self.embedding_service.generate_vector(user_cv_text)

        # 2. Get Job Vector from ChromaDB
        job_data = self.vector_db_service.get_or_create_collection(collection_name).get(
            ids=[job_id], 
            include=["embeddings", "documents", "metadatas"]
        )
        
       
        if job_data["embeddings"] is None or len(job_data["embeddings"]) == 0:
            return "Job not found in database."

        job_vector = job_data["embeddings"][0]
        job_text = job_data["documents"][0]

        # 3. Calculate Similarity (Percentage)
        similarity_score = self.math.calculate_similarity(job_vector, user_vector)
        match_percentage = round(similarity_score * 100, 2)

        # 4. Calculate the 'Gap Vector'
        # This vector points to what is missing in the user's profile
        gap_vector = self.math.calculate_skill_gap(job_vector, user_vector)

        return {
            "match_percentage": match_percentage,
            "gap_vector": gap_vector,
            "job_title": job_data["metadatas"][0].get("role", "Unknown"),
            "original_job_text": job_text
        }