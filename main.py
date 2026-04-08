from src.services.embedding_service import EmbeddingService
from src.services.vector_db_service import VectorDBService
from src.use_cases.analyzer import SkillGapAnalyzer
from src.use_cases.path_generator import LearningPathGenerator

def main():
    # 1. Initialize Services
    # Creating the engines
    embed_service = EmbeddingService()
    db_service = VectorDBService()
    
    # 2. Setup Analyzers
    analyzer = SkillGapAnalyzer(embed_service, db_service)
    path_gen = LearningPathGenerator(db_service)

    # 3. Seed Data (Simulating a real database)
    # Adding a sample Job
    job_text = "Senior Python Developer: Expert in FastAPI, PostgreSQL, and AWS Cloud."
    job_vector = embed_service.generate_vector(job_text)
    db_service.add_data(
        collection_name="jobs",
        ids=["job_001"],
        documents=[job_text],
        embeddings=[job_vector],
        metadatas=[{"role": "Senior Python Developer", "company": "TechCorp"}]
    )

    # Adding sample Courses
    course_data = [
        {"id": "c1", "text": "Mastering AWS Cloud Infrastructure", "meta": {"title": "AWS Course", "url": "https://aws.com"}},
        {"id": "c2", "text": "Deep Dive into FastAPI and Async Python", "meta": {"title": "FastAPI Mastery", "url": "https://fastapi.tiangolo.com"}},
        {"id": "c3", "text": "Basic Python for Beginners", "meta": {"title": "Intro to Python", "url": "https://python.org"}}
    ]
    
    db_service.add_data(
        collection_name="courses",
        ids=[c["id"] for c in course_data],
        documents=[c["text"] for c in course_data],
        embeddings=embed_service.generate_vectors_batch([c["text"] for c in course_data]),
        metadatas=[c["meta"] for c in course_data]
    )

    # 4. User Simulation (The CV)
    # Let's say the user knows Python and SQL but lacks AWS and FastAPI
    user_cv = "I am a developer with experience in Python and SQL databases. Looking for new challenges."
    
    print("\n--- Starting Analysis ---")
    results = analyzer.analyze_user_vs_job(user_cv, job_id="job_001")

    print(f"Target Job: {results['job_title']}")
    print(f"Match Percentage: {results['match_percentage']}%")

    # 5. Generate Learning Path
    print("\n--- Recommended Learning Path to Close the Gap ---")
    recommendations = path_gen.generate_recommendations(results['gap_vector'])

    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - Relevance: {rec['relevance_score']} | Link: {rec['url']}")

if __name__ == "__main__":
    main()