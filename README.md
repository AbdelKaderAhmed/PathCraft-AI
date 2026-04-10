🎯 PathCraft AI | Strategic Skill-Gap Analysis Engine
PathCraft AI is a local-first intelligence platform engineered to analyze technical alignment within the 2026 AI job market. By leveraging high-dimensional vector embeddings and deterministic matching logic, the system provides precise gap analysis and career deployment roadmaps without relying on external cloud APIs.

🛠 Technical Architecture
The system is built with a modular "Local-First" stack, prioritizing data privacy, low latency, and mathematical accuracy.

Neural Inference (Local): Sentence-Transformers utilizing BERT-based architectures for high-precision semantic vector generation.

Vector Orchestration: ChromaDB for high-dimensional indexing and similarity-based retrieval.

Compute Logic: Pure Python 3.10+ featuring custom VectorMath modules for deterministic similarity scoring.

Tactical Interface: Streamlit with a customized Cyber-Industrial CSS framework for high-density data visualization.

Data Pipeline: Pandas for structured market intelligence and PyPDF2 for secure, localized document parsing.

🚀 Key Capabilities
📡 Offline Vector Intelligence
Execute deep semantic analysis of professional experience against complex job requirements. The system maps CV data to a high-dimensional vector space stored in ChromaDB, enabling instantaneous alignment scoring without external API dependencies.

🛡️ Tactical Token Extraction
A robust regex-based extraction engine designed to parse unstructured job descriptions. It identifies critical technical tokens (e.g., Vector Databases, RAG, PyTorch) to generate a clean, validated "Required Stack" list.

🧬 Automated Gap Synthesis
The engine cross-references identified technical deficiencies with a localized courses.csv repository. This generates a direct bridge between detected gaps and verified educational modules from elite providers.

📟 Cyber-Industrial Command Center
An engineering-centric dashboard designed for professional clarity:

Match Readiness Index: Real-time percentage reflecting semantic and technical alignment.

Deployment Status: Visual "MATCHED" (✔) and "GAP" (✖) status indicators.


📂 Project Structure

├── data/                   # Verified Course Intelligence (courses.csv)
├── src/
│   ├── api/                # Tactical Command Dashboard (app.py)
│   ├── core/               # Mathematical logic & analysis entities
│   ├── services/           # VectorDB (ChromaDB) & Embedding orchestration
│   └── use_cases/          # SkillGapAnalyzer & PathGenerator modules
├── ai_jobs_market_25_26.csv# 2026 AI Market Intelligence Dataset
├── ingest_jobs.py          # Data Ingestion & Vectorization Pipeline
└── requirements.txt        # System Dependency Manifest

⚡ Deployment Guide
1.Environment Setup:
pip install -r requirements.txt

2.Initialize Vector Database (Local Processing):
  python ingest_jobs.py

3.Launch Tactical Interface:
 streamlit run src/api/app.py

 
