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

## Prerequisites

- Python 3.11+
- Docker (for the Postgres database)
- A Telegram bot token + chat ID (optional, only for notifications)

## Quick Start

```bash
git clone https://github.com/Sanket17052006/msme-inventory-automation.git
cd msme-inventory-automation

# 1. Start Postgres
docker compose up -d db

# 2. Set up the Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Create tables and seed demo data
python backend/init_db.py
python seed_data.py

# 4. Start the API
uvicorn backend.main:app --reload

# 5. Start the dashboard (in a second terminal)
streamlit run dashboard/app.py
```

Open http://localhost:8000/docs for the API, or http://localhost:8501 for the dashboard.

## Telegram Notifications (optional)

Create a `.env` file in the project root with your bot credentials:

```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Then run the automation scripts in separate terminals:

```bash
# Auto-detects low stock, creates reorder orders, and alerts suppliers
python stock_monitor.py

# Interactive bot — suppliers confirm/reject orders via Telegram
python telegram_bot.py
```

## Notes

- If you already have PostgreSQL running locally on port `5432`, the app will use it instead of the Docker container — make sure it has a `msme` database (`msme`/`msme` user and password), or stop it before running `docker compose up -d db`.
- To reset the database and reseed: rerun `python seed_data.py` (it clears existing data first) and restart the backend.
