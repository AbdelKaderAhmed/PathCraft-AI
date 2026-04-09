import pandas as pd
import os
import re
from src.core.entities import Course

class LearningPathGenerator:
    """
    Generates educational paths by matching identified skill gaps 
    with available courses from CSV and Vector Database.
    """
    def __init__(self, vector_db_service):
        self.vector_db_service = vector_db_service
        self.data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../data/courses.csv"))
        
        self.real_courses = None
        if os.path.exists(self.data_path):
            try:
                self.real_courses = pd.read_csv(self.data_path)
                self.real_courses.columns = self.real_courses.columns.str.strip()
            except Exception as e:
                print(f"CRITICAL ERROR: Could not load courses.csv: {e}")
        else:
            print(f"SYSTEM WARNING: CSV file missing at {self.data_path}")

    def generate_recommendations(self, gap_vector, gap_skills=None, *args, **kwargs):
        recommendations = []
        seen_titles = set()

        # --- STEP 1: SMART CSV MATCHING ---
        if gap_skills and self.real_courses is not None:
            for skill in gap_skills:
                clean_skill = str(skill).strip().lower()
                if not clean_skill: continue

                # تحسين البحث: نبحث عما إذا كانت المهارة موجودة كجزء من نص المهارة في الكورس
                # أو العكس (لضمان أقصى تغطية)
                mask = self.real_courses['skill'].str.lower().apply(
                    lambda x: clean_skill in str(x) or str(x) in clean_skill
                )
                matches = self.real_courses[mask]
                
                for _, row in matches.iterrows():
                    title = row['course_title']
                    if title not in seen_titles:
                        course_entity = Course(
                            id=f"csv-{clean_skill}",
                            title=title,
                            url=row['url'],
                            provider=row['provider'],
                            skill_covered=row['skill'],
                            relevance_score=100.0
                        )
                        recommendations.append(course_entity.__dict__)
                        seen_titles.add(title)

        # --- STEP 2: SEMANTIC VECTOR SEARCH ---
        try:
            # نطلب عدد أكبر قليلاً لضمان التنوع (10 بدلاً من 5)
            vector_results = self.vector_db_service.query_similar(
                collection_name="courses",
                query_embeddings=[gap_vector],
                n_results=10 
            )
            
            if vector_results and 'ids' in vector_results and len(vector_results['ids'][0]) > 0:
                for i in range(len(vector_results['ids'][0])):
                    meta = vector_results['metadatas'][0][i]
                    title = meta.get("title", "Advanced Training")
                    
                    if title not in seen_titles:
                        distance = vector_results['distances'][0][i]
                        # تصحيح الحسبة: ضمان أن السكور دائماً بين 0 و 100
                        score = max(5.0, round(abs(1 - float(distance)) * 100, 1))
                        if score > 100: score = 95.0 # تصحيح في حال كانت الـ distance سالبة
                        
                        course_entity = Course(
                            id=vector_results['ids'][0][i],
                            title=title,
                            url=meta.get("url", "#"),
                            provider=meta.get("provider", "AI Technical Institute"),
                            skill_covered=meta.get("skill", "Vector Match"),
                            relevance_score=score
                        )
                        recommendations.append(course_entity.__dict__)
                        seen_titles.add(title)
        except Exception as e:
            print(f"VECTOR SEARCH FAILED: {e}")

        # ترتيب النتائج النهائية حسب الأهمية
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # إرجاع أفضل 6 توصيات
        return recommendations[:6]