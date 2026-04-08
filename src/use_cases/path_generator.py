class LearningPathGenerator:
    """
    This use case takes the 'Gap Vector' and searches the 
    Course Collection in ChromaDB to find the best learning materials.
    """

    def __init__(self, vector_db_service):
        self.vector_db_service = vector_db_service

    def generate_recommendations(self, gap_vector, collection_name="courses", top_n=3):
        """
        Search for courses that are semantically closest to the gap_vector.
        """
        # We query ChromaDB using the gap_vector itself as the 'search term'
        results = self.vector_db_service.query_similar(
            collection_name=collection_name,
            query_embeddings=[gap_vector],
            n_results=top_n
        )

        # Structure the results for the user
        recommendations = []
        
        # results contains lists, we take the first element (index 0)
        for i in range(len(results['ids'][0])):
            recommendations.append({
                "id": results['ids'][0][i],
                "title": results['metadatas'][0][i].get("title", "Unknown Course"),
                "url": results['metadatas'][0][i].get("url", "#"),
                "provider": results['metadatas'][0][i].get("provider", "Open Source"),
                "relevance_score": f"{max(0, round((1 - results['distances'][0][i]) * 100, 1))}%" # Converting distance to similarity
            })

        return recommendations