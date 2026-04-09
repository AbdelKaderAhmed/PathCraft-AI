import sys
import os
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# --- 1. SETTING UP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.services.embedding_service import EmbeddingService
from src.services.vector_db_service import VectorDBService
from src.use_cases.analyzer import SkillGapAnalyzer
from src.use_cases.path_generator import LearningPathGenerator

# --- 2. PROFESSIONAL UI CONFIG ---
st.set_page_config(page_title="PathCraft AI | Tactical Command", page_icon="🎯", layout="wide")

# Custom CSS for Cyber-Industrial UI
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stApp { background-color: #0f172a; }
    
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'JetBrains Mono', monospace; }

    /* Cards & Skill Rows */
    .skill-card {
        background: linear-gradient(145deg, #1e293b, #111827);
        padding: 24px;
        border-radius: 12px;
        border-left: 5px solid #0ea5e9;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .status-log { 
        font-family: 'JetBrains Mono', monospace; 
        background-color: #000; 
        color: #10b981; 
        padding: 12px; 
        border-radius: 6px; 
        font-size: 0.8rem; 
        border: 1px solid #10b981;
        line-height: 1.5;
    }

    .skill-row-matched {
        display: flex; justify-content: space-between; align-items: center; 
        background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.3); 
        padding: 12px 18px; border-radius: 8px; margin-bottom: 10px;
    }
    .skill-row-gap {
        display: flex; justify-content: space-between; align-items: center; 
        background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.3); 
        padding: 12px 18px; border-radius: 8px; margin-bottom: 10px;
    }
    
    .match-badge { background-color: #10b981; color: white; padding: 2px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
    .gap-badge { background-color: #ef4444; color: white; padding: 2px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
    
    /* Buttons & Expander */
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #0ea5e9; color: white;
        font-weight: bold; border: none; padding: 10px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0284c7; box-shadow: 0 0 15px rgba(14, 165, 233, 0.4); }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def init_services():
    return EmbeddingService(), VectorDBService()

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages])
        return text
    except Exception as e:
        st.error(f"PDF Parse Error: {e}")
        return ""

def main():
    embed_service, db_service = init_services()
    analyzer = SkillGapAnalyzer(embed_service, db_service)
    path_gen = LearningPathGenerator(db_service)

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    # --- SIDEBAR: TACTICAL OPS ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2092/2092565.png", width=80)
        st.markdown("### ⚙️ SYSTEM CONTROL")
        st.markdown(f"""<div class='status-log'>> NODE: PathCraft_Alpha<br>> DB: CONNECTED<br>> VECTORS: ACTIVE</div>""", unsafe_allow_html=True)
        
        st.divider()
        st.header("👤 CV INTELLIGENCE")
        input_mode = st.radio("CV SOURCE", ["Upload PDF Resume", "Manual Input"])
        
        user_cv_text = ""
        if input_mode == "Upload PDF Resume":
            pdf_file = st.file_uploader("Drop CV here", type="pdf")
            if pdf_file:
                user_cv_text = extract_text_from_pdf(pdf_file)
                if user_cv_text: st.success("📡 CV DATA STREAMING...")
        else:
            user_cv_text = st.text_area("SKILLS SUMMARY", placeholder="Paste skills or experience here...", height=150)

    # --- MAIN UI ---
    st.markdown("# 🎯 PATHCRAFT <span style='color:#0ea5e9'>AI CORE</span>", unsafe_allow_html=True)
    st.caption("Strategic Intelligence for Real-World Skill Mapping & Deployment")

    # Fetch Data
    collection = db_service.get_or_create_collection("jobs")
    all_data = collection.get(include=["metadatas", "documents"])
    
    if not all_data['ids']:
        st.warning("⚠️ SYSTEM OFFLINE: No jobs found in the vector database.")
        return

    df_meta = pd.DataFrame(all_data['metadatas'])
    df_meta['id'] = all_data['ids']
    df_meta['content'] = all_data['documents']
    df_meta['location'] = df_meta['location'].fillna("Remote").astype(str)

    # Filtering Logic
    c1, c2 = st.columns(2)
    with c1:
        countries = sorted(list(set(df_meta['location'].apply(lambda x: x.split(',')[-1].strip() if ',' in x else str(x)))))
        selected_country = st.selectbox("🌍 TARGET REGION", options=["All Regions"] + countries)
    
    with c2:
        filtered_df = df_meta[df_meta['location'].str.contains(selected_country, case=False, na=False)] if selected_country != "All Regions" else df_meta
        role_options = sorted([str(role) for role in filtered_df['title'].dropna().unique()])
        selected_role = st.selectbox("🪖 TARGET ROLE", options=role_options if role_options else ["N/A"])

    if st.button("RUN TACTICAL ANALYSIS"):
        if not user_cv_text:
            st.warning("INPUT REQUIRED: CV data is missing.")
        elif selected_role == "N/A":
            st.error("SELECTION REQUIRED: Target role not specified.")
        else:
            with st.spinner("📡 ANALYZING VECTOR GAPS..."):
                job_row = filtered_df[filtered_df['title'] == selected_role].iloc[0]
                st.session_state.analysis_results = {
                    'analysis': analyzer.analyze_user_vs_job(user_cv_text, job_id=job_row['id']),
                    'job_row': job_row
                }

    # --- RESULTS DISPLAY ---
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results['analysis']
        job = st.session_state.analysis_results['job_row']
        
        

        st.divider()
        col_info, col_gap = st.columns([1, 1.2], gap="large")
        
        with col_info:
            st.subheader("📋 TARGET PROFILE")
            st.markdown(f"""
            <div class='skill-card'>
                <small style='color:#94a3b8; font-weight:bold;'>READINESS LEVEL</small>
                <h1 style='color:#0ea5e9; margin:0; font-size:3rem;'>{res.match_percentage}%</h1>
                <hr style='border-color:#334155'>
                <div style='font-size:0.9rem; line-height:1.8;'>
                    <b>ROLE:</b> {job['title']}<br>
                    <b>ZONE:</b> {job['location']}<br>
                    <b>EST. VALUE:</b> {job.get('salary', 'Competitive Package')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🛠 TECHNICAL STACK")
            
            # Logic for Matched/Gap display
            display_gaps = res.gap_skills
            display_matched = res.matched_skills

            if not display_gaps and not display_matched:
                fallback_skills = ["Python", "Machine Learning", "API Design"]
                display_gaps = [s for s in fallback_skills if s.lower() not in user_cv_text.lower()]
                display_matched = [s for s in fallback_skills if s.lower() in user_cv_text.lower()]

            for s in display_matched:
                st.markdown(f'<div class="skill-row-matched"><span>✔ {s}</span><span class="match-badge">DEPLOYED</span></div>', unsafe_allow_html=True)
            for s in display_gaps:
                st.markdown(f'<div class="skill-row-gap"><span>✖ {s}</span><span class="gap-badge">MISSING</span></div>', unsafe_allow_html=True)

        with col_gap:
            st.subheader("🚀 DEPLOYMENT TRAINING")
            recs = path_gen.generate_recommendations(gap_vector=res.gap_vector, gap_skills=res.gap_skills)
            
            if recs:
                for r in recs:
                    is_csv = "csv" in str(r.get('id', ''))
                    icon = "🛡️" if is_csv else "📚"
                    with st.container():
                        st.markdown(f"""
                        <div style='background:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155; margin-bottom:10px;'>
                            <div style='display:flex; justify-content:space-between;'>
                                <b>{icon} {r['title']}</b>
                                <span style='color:#0ea5e9;'>{r['relevance_score']}% Match</span>
                            </div>
                            <small style='color:#94a3b8;'>Provider: {r.get('provider', 'Expert')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.link_button(f"OPEN MODULE", r['url'])
            else:
                if res.match_percentage < 75:
                    st.warning("⚠️ NO DIRECT MATCHES: The skills gap is too wide for local courses. Consider fundamental AI training.")
                else:
                    st.success("🎯 OPTIMAL ALIGNMENT: Your profile is ready for deployment in this role.")

if __name__ == "__main__":
    main()