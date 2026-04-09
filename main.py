import sys
import os

# Ensure the project root is in the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.services.embedding_service import EmbeddingService
from src.services.vector_db_service import VectorDBService
from src.use_cases.analyzer import SkillGapAnalyzer
from src.use_cases.path_generator import LearningPathGenerator

def main():
    # 1. Initialize core AI and Database services
    embed_service = EmbeddingService()
    db_service = VectorDBService()
    
    # 2. Setup the Business Logic Layer
    analyzer = SkillGapAnalyzer(embed_service, db_service)
    path_gen = LearningPathGenerator(db_service)

    # 3. Seed Data: Injecting sample Job into the Vector DB
    # We use a piped string format to simulate our production data structure
    job_title = "Senior Python Developer"
    job_skills_text = "Python | FastAPI | PostgreSQL | AWS Cloud"
    job_full_text = f"{job_title}: Expert in {job_skills_text}"
    
    job_vector = embed_service.generate_vector(job_full_text)
    
    # Clear old data if needed or just add new
    db_service.add_data(
        collection_name="jobs",
        ids=["job_001"],
        documents=[job_full_text],
        embeddings=[job_vector],
        metadatas=[{"title": job_title, "location": "Remote", "content": job_skills_text}]
    )

    # 4. User Simulation: A CV that lacks specific keywords
    user_cv = "I am a developer with experience in Python and SQL. Looking for new challenges."
    
    print("\n--- [PHASE 1: STRATEGIC ANALYSIS] ---")
    results = analyzer.analyze_user_vs_job(user_cv, job_id="job_001")

    print(f"Target Job: {results.get('job_title', job_title)}")
    print(f"Match Readiness: {results['match_percentage']}%")

    # 5. Skill Extraction & Cleaning (Logic Sync with app.py)
    # We manually extract gaps to pass them as text for high-accuracy CSV matching
    raw_skills = job_skills_text.split('|')
    gap_skills = []
    
    for s in raw_skills:
        skill_name = s.strip()
        # Case-insensitive check to find missing keywords in CV
        if skill_name.lower() not in user_cv.lower():
            gap_skills.append(skill_name)

    print(f"Detected Gaps: {', '.join(gap_skills)}")

    # 6. Generate Recommendations using both Vector and Textual Gaps
    print("\n--- [PHASE 2: RECOMMENDED TRAINING] ---")
    recommendations = path_gen.generate_recommendations(
        gap_vector=results['gap_vector'],
        gap_skills=gap_skills
    )

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. [{rec.get('provider', 'Expert')}] {rec['title']}")
            print(f"   Relevance: {rec['relevance_score']} | Link: {rec['url']}\n")
    else:
        print("No immediate matches found in local repository.")

if __name__ == "__main__":
    main()