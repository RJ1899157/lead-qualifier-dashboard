# Developer Setup & Architecture Notes

> For a description of what this project does and its workflow, see `README.md`. This file covers setup, configuration, and technical/architectural notes only.

## Tech stack

- **Backend:** FastAPI (Python)
- **LLM:** Groq (`llama-3.3-70b-versatile`) via `langchain-groq`
- **Data store:** Airtable (via `pyairtable`)
- **CSV parsing:** pandas
- **Frontend:** static HTML/CSS/vanilla JS (no build step), served directly by FastAPI

## Prerequisites

- Python 3.10+
- A Groq API key ([console.groq.com](https://console.groq.com))
- An Airtable base with a table named **`Leads`**

## Airtable schema

The `Leads` table is expected to have (at minimum) these fields, matching what `lead_repository.py` reads/writes:

| Field | Type |
|---|---|
| `lead_id` | Single line text |
| `full_name` | Single line text |
| `designation` | Single line text |
| `company_name` | Single line text |
| `industry` | Single line text |
| `country` | Single line text |
| `linkedin_profile` | URL / text |
| `work_email` | Email / text |
| `phone_number` | Phone / text |
| `website` | URL / text |
| `company_size` | Number |
| `engagement` | Long text |
| `score` | Number |
| `status` | Single line text |
| `score_explanation` | Long text |
| `recommended_action` | Long text |
| `ai_summary` | Long text |
| `interaction_count` | Number |
| `knowledge_base` | Long text |
| `priority_rank` | Number |

## Environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
AIRTABLE_TOKEN=your_airtable_personal_access_token
AIRTABLE_BASE_ID=your_airtable_base_id
```

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running locally

```bash
uvicorn main:app --reload
```

The app will be available at `http://localhost:8000`.

Routes served:
| Route | Serves |
|---|---|
| `/` | `index.html` — main dashboard |
| `/sales-assistant` | `sales_assistant.html` — sales assistant page |
| `/analytics` | `analytics.html` — analytics page (not included in this doc set) |
| `/components.js` | shared JS (sidebar, chatbot components) |

## Project structure

```
.
├── main.py                # FastAPI app & all routes
├── lead_qualifier.py       # Orchestrates scoring + AI explanation generation
├── scoring.py              # Deterministic scoring rules (role/industry/country/size/engagement)
├── data_loader.py          # CSV parsing, header aliasing/normalization
├── lead_repository.py      # Airtable CRUD wrapper
├── airtable_client.py      # Airtable API client init
├── utils.py                # Misc helpers (lead ID generation)
├── index.html              # Dashboard UI
├── sales_assistant.html    # Sales assistant UI
├── components.js           # Shared frontend components (not included in this doc set)
└── .env                    # Local secrets (not committed)
```

## API reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/leads` | List all leads |
| `POST` | `/api/leads` | Create + score a single lead |
| `PUT` | `/api/leads/{record_id}` | Update + re-score a lead |
| `DELETE` | `/api/leads/{record_id}` | Delete a lead |
| `POST` | `/api/leads/upload-csv` | Bulk-import leads from CSV (upserts on name+company match) |
| `GET` | `/api/sales-assistant/{index}` | Get discovery questions + pitch suggestion for a lead |
| `POST` | `/api/meeting-summary` | Generate a structured meeting summary from raw notes |
| `POST` | `/api/chat` | Chatbot query against the full lead database |
| `POST` | `/api/chat/reset` | Clear chatbot conversation history |

## Known limitations / TODOs (from code comments)

- `chat_history` in `main.py` is a **single global in-memory list** — it is shared across all users/sessions and is not safe for a multi-user deployment. Should be moved to per-session storage (e.g. keyed by a session/user ID) before shipping beyond a single user.
- `/api/sales-assistant/{index}` looks up leads by **array index**, not by stable `record_id`. If leads are deleted/reordered between the dashboard fetching the list and the assistant call, the index can point to the wrong lead. This should be switched to `record_id`-based lookup.
- CSV upload deduplication matches on exact `full_name` + `company_name` string match — case/whitespace variants will be treated as new leads.
- No authentication/authorization is implemented; this is intended for internal/trusted use only.

## Design notes

- Scoring is intentionally deterministic (`scoring.py`) so lead ranking is consistent and auditable; the LLM is only used to generate human-readable explanations (`lead_qualifier.py`) and sales-facing text (`main.py` — discovery questions, pitch, meeting summaries, chat), never to set the score itself.
- All API responses are returned via a shared `json_response()` helper to force UTF-8 JSON encoding (protects against mangled characters from LLM output, e.g. smart quotes).