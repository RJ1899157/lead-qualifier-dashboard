# Lead Qualifier Dashboard
by Rishabh Jain | Amity University Noida

## What it does
An AI-powered lead qualification system that automatically scores and prioritizes sales leads as Hot, Warm, or Cold using a Groq LLM (Llama 3.3).

## Features
- AI scoring of leads based on role, company size, industry, country and engagement
- Color-coded dashboard with sidebar filters
- Detail panel with AI analysis and recommended action per lead
- Real-time stats — total, hot, warm, cold lead counts

## Tech Stack
Python, FastAPI, LangChain, Groq (Llama 3.3), HTML/CSS/JS

## How to run
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Then open localhost:8000 in your browser.

## Architecture
Sample Leads → Lead Qualifier (LangChain + Groq) → FastAPI Backend → Dashboard UI