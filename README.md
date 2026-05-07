# Lead Qualifier Dashboard
by Rishabh Jain | Amity University Noida | CSE 2023-2027

## What it does
An AI-powered lead qualification system that automatically scores and prioritizes 
sales leads as Hot, Warm, or Cold using Groq's Llama 3.3 via LangChain.

Built as part of Marksman Technologies internship prep — directly relevant to 
Team 4: Lead Qualification + Sales Assistant.

## Features
- AI scoring of leads based on role seniority, company size, industry, country and engagement
- Hot / Warm / Cold classification with confidence scores
- Professional dark-theme dashboard with sidebar navigation
- Filter leads by status in real time
- Detail panel with AI analysis and recommended action per lead
- Live stats — total, hot, warm, cold lead counts
- Add new leads via form — AI qualifies them instantly
- Delete leads directly from the dashboard

## Tech Stack
Python, FastAPI, LangChain, Groq (Llama 3.3), HTML, CSS, JavaScript

## Setup
source env/bin/activate
pip install fastapi uvicorn langchain-groq langchain-core python-dotenv
uvicorn main:app --reload

Then open localhost:8000 in your browser.

## Architecture
Sample Leads → LangChain + Groq LLM → Lead Scorer → FastAPI Backend → Dashboard UI

## Scoring Criteria
- Role seniority (CEO/CTO/Founder scores higher than Manager)
- Company size (larger = higher score)
- Industry relevance (EdTech, Pharma, Retail, Real Estate, Media)
- Target geography (USA, Canada, Singapore, Middle East)
- Engagement level (requested call > replied > opened email > no engagement)