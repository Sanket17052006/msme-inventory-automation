# MSME Inventory Automation

An AI-powered inventory management and supply chain copilot for MSMEs. Monitors stock levels, auto-calculates reorder quantities, and places orders via Telegram.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python |
| Database | PostgreSQL (via async SQLAlchemy) |
| Dashboard | Streamlit |
| Notifications | Telegram Bot |
| Containers | Docker Compose |

## Quick Start

```bash
git clone https://github.com/Sanket17052006/msme-inventory-automation.git
cd msme-inventory-automation

docker compose up -d db

python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

python backend/init_db.py
python seed_data.py

uvicorn backend.main:app --reload
```

Open http://localhost:8000/docs for the API, or http://localhost:8501 for the dashboard.
