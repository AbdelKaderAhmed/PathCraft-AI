import pandas as pd
import uuid
import os
from src.services.embedding_service import EmbeddingService
from src.services.vector_db_service import VectorDBService

def ingest_all():
    embed_service = EmbeddingService()
    db_service = VectorDBService()

    # --- 1. شحن بيانات الوظائف (JOBS) ---
    jobs_file = "ai_jobs_market_2025_2026.csv"
    if os.path.exists(jobs_file):
        print(f"--- Processing Jobs: {jobs_file} ---")
        df_jobs = pd.read_csv(jobs_file).dropna(subset=['required_skills']).head(200)
        
        job_docs = [f"Job: {r['job_title']}. Skills: {r['required_skills']}" for _, r in df_jobs.iterrows()]
        job_metas = [{
            "title": str(r.get('job_title', 'Unknown')),
            "location": f"{r.get('city', 'Remote')}, {r.get('country', '')}",
            "salary": f"${r.get('annual_salary_usd', 'N/A')}",
            "content": str(r['required_skills']) # مهم للتحليل النصي لاحقاً
        } for _, r in df_jobs.iterrows()]
        
        job_vectors = embed_service.generate_vectors_batch(job_docs)
        job_ids = [str(uuid.uuid4()) for _ in range(len(job_docs))]
        
        db_service.add_data("jobs", job_ids, job_docs, job_vectors, job_metas)
        print(f"✅ Success: {len(job_ids)} Jobs Ingested.")

    # --- 2. شحن بيانات الكورسات (COURSES) - هذا الجزء المفقود ---
    courses_file = "data/courses.csv"
    if os.path.exists(courses_file):
        print(f"--- Processing Courses: {courses_file} ---")
        df_courses = pd.read_csv(courses_file)
        
        # نستخدم اسم الكورس والمهارة التي يغطيها لإنشاء المتجه
        course_docs = [f"Course: {r['course_title']}. Covers: {r['skill']}" for _, r in df_courses.iterrows()]
        course_metas = df_courses.to_dict(orient='records') # تخزين كل البيانات كـ metadata
        
        course_vectors = embed_service.generate_vectors_batch(course_docs)
        course_ids = [f"course-{i}" for i in range(len(course_docs))]
        
        db_service.add_data("courses", course_ids, course_docs, course_vectors, course_metas)
        print(f"✅ Success: {len(course_ids)} Courses Ingested.")
    else:
        print(f"❌ Error: {courses_file} not found. Cannot recommend training!")

if __name__ == "__main__":
    ingest_all()