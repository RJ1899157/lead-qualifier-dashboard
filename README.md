# Lead Qualifier — AI Sales Lead Dashboard

**Marksman Technologies Pvt. Ltd. | AI Internship | Team 4**
**Team Members**
- Rishabh Jain — Amity University Noida | CSE 2023–2027
- Chetna Verma — Amity University Noida | CSE 2023–2027
- Aniruddha Singh — Amity University Noida | CSE 2023–2027

## What is this?
 
Lead Qualifier is a small internal tool that helps a sales team figure out **which leads are worth chasing first**, and then helps them actually work those leads — questions to ask, a pitch angle to use, and a summary after the call.
 
Instead of a rep manually reading through a spreadsheet and guessing who's "hot," the tool scores every lead automatically and explains *why* it gave that score.
 
## Who it's for
 
Anyone on a sales team who receives inbound leads (from a form, an event, a CSV export, etc.) and needs to decide who to call first and what to say.
 
## The problem it solves
 
When leads come in one by one or in bulk, it's hard to consistently judge:
- Is this person senior enough to make a buying decision?
- Is their industry/company/country a good fit?
- Have they actually engaged with us, or did they just fill a form?
This tool answers those questions with a consistent, explainable score instead of gut feeling.
 
## How it works (workflow)
 
1. **Add a lead**
   - One at a time via the "Add Lead" form (name, role, company, industry, country, company size, engagement notes, contact details), or
   - In bulk by uploading a CSV of leads.
2. **Automatic scoring**
   - Each lead is scored out of 100 based on five factors: **role/seniority, industry, country, company size, and engagement level**.
   - Based on the total score, the lead is labeled:
     - 🔴 **Hot** (score ≥ 80) — strong fit, follow up immediately
     - 🟠 **Warm** (score 50–79) — decent fit, worth pursuing
     - 🔵 **Cold** (score < 50) — low priority for now
3. **AI explanation**
   - For every lead, an AI model writes a short, human-readable explanation of *why* it received that score, plus a recommended next action (e.g. "schedule a demo call").
4. **Dashboard**
   - All leads show up in a sortable, filterable, searchable table with their score, status, and details.
   - Click a lead to see its full profile — contact info, engagement history, and the AI's reasoning.
   - Leads can be edited or deleted at any time (which re-scores them if edited).
5. **Sales Assistant**
   - Pick any lead and the assistant generates:
     - **5 discovery questions** tailored to that lead's role, industry, and engagement.
     - **A personalized pitch angle** for that specific lead.
   - After a call, paste in your raw meeting notes and the assistant turns them into a structured summary (Summary / Key Points / Next Steps) you can drop straight into a CRM.
6. **Chatbot**
   - A chat assistant with visibility into the entire lead database, for quick questions like "who are my top 3 hottest leads in Pharma?" or "draft me a follow-up email to [lead]."
## Scoring criteria
 
Every lead is scored out of 100 by adding up points from five factors:
 
**1. Role / seniority — up to 30 points**
| Role | Points |
|---|---|
| CEO / Founder | 30 |
| CTO / VP Marketing | 25 |
| Director | 20 |
| Manager | 10 |
| Junior Manager | 5 |
| Any other role | 5 |
 
**2. Industry — up to 25 points**
| Industry | Points |
|---|---|
| EdTech / Pharma | 25 |
| Retail | 20 |
| Media | 18 |
| Real Estate | 15 |
| Any other industry | 10 |
 
**3. Country — up to 15 points**
| Country | Points |
|---|---|
| USA | 15 |
| Canada | 12 |
| Singapore / UAE | 10 |
| India | 5 |
| Any other country | 5 |
 
**4. Company size — up to 20 points**
| Employees | Points |
|---|---|
| 500+ | 20 |
| 100–499 | 15 |
| 20–99 | 10 |
| Under 20 | 5 |
 
**5. Engagement level — up to 10 points**
Based on keywords found in the engagement notes:
| Engagement mentions... | Points |
|---|---|
| "requested", "demo", or "call" | 10 |
| "replied" | 8 |
| "opened" or "clicked" | 5 |
| None of the above | 0 |
 
**Final status** is then assigned from the total (out of 100):
- 🔴 **Hot** — 80 and above
- 🟠 **Warm** — 50 to 79
- 🔵 **Cold** — below 50
This is why two leads with the same job title can end up with very different scores — it's the *combination* of role, industry, country, company size, and how engaged they've actually been that determines the final number.
 
## Why this approach
 
- **Scoring is deterministic, explanations are AI-generated.** The score itself is calculated by fixed rules (not the AI), so it's consistent and repeatable. The AI is only used to *explain* the score and to help with the sales-facing writing tasks (questions, pitches, summaries) — the parts that genuinely benefit from natural language generation.
- This keeps the ranking trustworthy while still getting the benefit of AI for the parts of the job that are naturally conversational.