# Lead Qualifier Dashboard
**Marksman Technologies Pvt. Ltd. | AI Internship | Team 4**
1 May 2026 – 15 July 2026

**Team Members**
- Rishabh Jain — Amity University Noida | CSE 2023–2027
- Chetna Verma — Amity University Noida | CSE 2023–2027
- Aniruddha Singh — Amity University Noida | CSE 2023–2027

## What it does
An AI-powered Sales Intelligence and Lead Prioritization System that automatically
scores and prioritizes sales leads as Hot, Warm, or Cold using a 3-layer hybrid
architecture — deterministic weighted scoring, NLP intelligence, and selective
GenAI via Groq's Llama 3.3 through LangChain.

## Features
- Deterministic weighted scoring with explainable score breakdown
- Hot / Warm / Cold classification with confidence scores and priority ranking
- Professional dark-theme dashboard with sidebar navigation
- Filter leads by status in real time
- Detail panel with AI analysis and recommended action per lead
- Live stats — total, hot, warm, cold lead counts
- Add single lead via modal or bulk upload via CSV
- Delete leads directly from the dashboard
- Sales Assistant page — discovery questions, pitch suggestions, meeting summary generator
- Email draft generator, follow-up sequence generator, objection handler
- Call script generator, sentiment analysis, CSV export
- Conversational chatbot on Dashboard and Sales Assistant pages
- Analytics tab with Chart.js visualizations
- Airtable as live database backend

## Tech Stack
Python 3.11, FastAPI, Uvicorn, LangChain, Groq API (Llama 3.3 70B),
HuggingFace, Airtable, HTML, CSS, JavaScript, Chart.js

## Setup
source env/bin/activate
pip install fastapi uvicorn langchain-groq langchain-core python-dotenv
uvicorn main:app --reload
Then open localhost:8000 in your browser.

## Architecture
3-Layer Hybrid System:
- Layer 1: Deterministic weighted scoring
- Layer 2: NLP intelligence
- Layer 3: Selective GenAI (Groq Llama 3.3 70B via LangChain)

Airtable DB → FastAPI Backend → LangChain + Groq → Dashboard UI

## Scoring Criteria
- Role seniority (CEO/CTO/Founder scores higher than Manager)
- Company size (larger = higher score)
- Industry relevance (EdTech, Pharma, Retail, Real Estate, Media)
- Target geography (USA, Canada, Singapore, Middle East)
- Engagement level (requested call > replied > opened email > no engagement)

## Repository
Branch: dev
GitHub: github.com/RJ1899157/lead-qualifier-dashboard