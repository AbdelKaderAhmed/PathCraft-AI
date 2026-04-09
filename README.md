# PathCraft-AI
🎯 PathCraft AI | Tactical Skill Analysis Engine
PathCraft AI is a professional-grade strategic intelligence system built to analyze skill gaps in the 2026 AI job market. It operates as a Fully Local AI System, ensuring data privacy and high performance without reliance on external APIs.

🛠 Project Tech Stack
Intelligence (Local Embeddings): Sentence-Transformers (Local BERT-based models for high-precision vector generation).

Memory (Vector Layer): ChromaDB (Open-source vector database for high-dimensional storage).

Logic & Math: Pure Python 3.10+ (Custom VectorMath for similarity scoring).

Control Panel (UI): Streamlit with a custom Cyber-Industrial CSS dashboard.

Data Engine: Pandas for structured market and course data management.

Document Parser: PyPDF2 for secure, local CV parsing.

🚀 Key Features
1. Offline Vector Intelligence
By using local embeddings, the system performs instantaneous analysis without network latency or API costs. It maps your CV against a high-dimensional vector space of job requirements stored in ChromaDB.

2. Tactical Skill Extraction
A robust extraction engine that uses pattern matching to scan job descriptions for technical tokens (e.g., Python, Vector DBs, RAG). This ensures a clean "Required Stack" even from unstructured text.

3. Verified Learning Path Synthesis
Identified gaps are cross-referenced with a local courses.csv database. The system provides a direct bridge between a missing skill and a verified course (e.g., DeepLearning.AI).

4. Cyber-Industrial Tactical UI
A high-density dashboard designed for engineering clarity:

Match Readiness Score: Real-time vector similarity percentage.

Technical Stack: Visual "MATCHED" (✔) vs "GAP" (✖) status.

Diagnostic Console: Real-time JSON logs showing system health and data integrity.

📂 Project Structure

├── data/                   # courses.csv (Verified training data)
├── src/
│   ├── api/                # Streamlit Dashboard (app.py)
│   ├── core/               # VectorMath & Analysis logic
│   ├── services/           # Local Embedding & ChromaDB services
│   └── use_cases/          # SkillGapAnalyzer & PathGenerator
├── ai_jobs_market_...csv   # Market Dataset (2025-2026)
├── ingest_jobs.py          # Local Data Ingestion Pipeline
└── requirements.txt        # System Dependencies

⚡ Quick Start
1.Install Dependencies:
  pip install -r requirements.txt

2.Run Ingestion (Local Processing):
  python ingest_jobs.py

3.Launch Tactical Command Center:
  streamlit run src/api/app.py

 