import re
from src.core.vector_math import VectorMath
from src.core.entities import AnalysisResult

class SkillGapAnalyzer:
    def __init__(self, embedding_service, vector_db_service):
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.math = VectorMath()

    def analyze_user_vs_job(self, user_cv_text, job_id, collection_name="jobs") -> AnalysisResult:
        # 1. جلب البيانات من Vector DB
        job_data = self.vector_db_service.get_or_create_collection(collection_name).get(
            ids=[job_id], 
            include=["embeddings", "documents", "metadatas"]
        )
        
        if not job_data.get("ids"):
           raise ValueError(f"Job ID {job_id} not found.")

        # 2. الحسابات الرياضية
        user_vector = self.embedding_service.generate_vector(user_cv_text)
        job_vector = job_data["embeddings"][0]
        similarity_score = self.math.calculate_similarity(job_vector, user_vector)
        match_percentage = round(float(similarity_score) * 100, 2)
        gap_vector = self.math.calculate_skill_gap(job_vector, user_vector)

        # 3. --- [إصلاح استخراج المهارات] ---
        # نجمع كل النصوص المتاحة عن الوظيفة في متغير واحد
        full_job_text = ""
        if job_data.get("documents"):
            full_job_text += str(job_data["documents"][0])
        if job_data.get("metadatas"):
            full_job_text += " " + str(job_data["metadatas"][0].get("content", ""))
            full_job_text += " " + str(job_data["metadatas"][0].get("title", ""))

        # مكتبة ذكية للمهارات المطلوبة في مجال AI/SaaS
        tech_library = [
            "Python", "PyTorch", "TensorFlow", "LLM", "LangChain", "NLP", 
            "Generative AI", "AWS", "Azure", "Docker", "Kubernetes", "SQL", 
            "PostgreSQL", "Vector DB", "FastAPI", "React", "AI Agent", "API"
        ]

        extracted_skills = []

        # محاولة الاستخراج عن طريق البحث عن الكلمات المفتاحية (Keyword Matching)
        for tech in tech_library:
            if re.search(rf'\b{re.escape(tech)}\b', full_job_text, re.IGNORECASE):
                extracted_skills.append(tech)

        # محاولة الاستخراج عن طريق الفواصل (Regex Split) إذا كان النص منظماً
        raw_split = re.split(r'[|,\n•\-]', full_job_text)
        for s in raw_split:
            clean_s = s.strip()
            if 1 < len(clean_s) < 30 and clean_s not in extracted_skills:
                # نتحقق أنها ليست جملة طويلة بل مهارة
                extracted_skills.append(clean_s)

        # 4. التصنيف النهائي
        user_cv_lower = user_cv_text.lower()
        matched_skills = [s for s in extracted_skills if s.lower() in user_cv_lower]
        gap_skills = [s for s in extracted_skills if s.lower() not in user_cv_lower]

        return AnalysisResult(
            job_id=job_id,
            match_percentage=match_percentage,
            gap_skills=gap_skills,
            matched_skills=matched_skills,
            gap_vector=gap_vector
        )