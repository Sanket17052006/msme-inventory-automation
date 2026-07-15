# MSME Inventory Automation

An AI-powered inventory management and supply chain copilot for MSMEs. Monitors stock levels, auto-calculates reorder quantities, and places orders via Telegram.

---

## Goal

MSMEs waste 15–20 hours per week on manual inventory tracking. This project automates the entire cycle:

- Monitor stock in real time
- Detect low inventory and calculate optimal reorder quantities
- Send order alerts via Telegram with one-tap CONFIRM / REJECT
- Fallback to alternate suppliers on timeout
- Dashboard for live inventory overview, sales trends, and order tracking

---

## Current State

- **Phase 1 (Foundation)** — ✅ Complete (FastAPI, PostgreSQL, Docker, models, schemas)
- **Phase 2 (Core API)** — 🟡 In progress ([tracked via epic #1](https://github.com/Sanket17052006/msme-inventory-automation/issues/1))

---

## Phase 2 — Core API Implementation

13 REST API endpoints powering the full inventory workflow. Status tracked in [epic #1](https://github.com/Sanket17052006/msme-inventory-automation/issues/1):

| Method | Endpoint | Purpose | Status |
|---|---|---|---|
| `GET` | `/health` | Health check | ✅ Done |
| `GET` | `/products` | List all products with stock levels | 🔲 Pending |
| `GET` | `/products/{id}` | Single product details | ✅ Done |
| `GET` | `/products/low-stock` | Products where stock < reorder_point | 🔲 Pending |
| `GET` | `/products/summary` | Dashboard summary counts | 🔲 Pending |
| `POST` | `/products/{id}/simulate-sale` | Reduce stock by qty (demo trigger) | ✅ Done |
| `GET` | `/orders` | List orders (filterable by status) | 🔲 Pending |
| `GET` | `/orders/{id}` | Single order details | 🔲 Pending |
| `POST` | `/orders` | Create a new order manually | 🔲 Pending |
| `PATCH` | `/orders/{id}/status` | Confirm, reject, or fulfill an order | 🔲 Pending |
| `GET` | `/suppliers` | List all suppliers | 🔲 Pending |
| `GET` | `/suppliers/{id}` | Single supplier details | 🔲 Pending |
| `GET` | `/sales-log` | Sales history for charts | 🔲 Pending |
| `GET` | `/analytics/summary` | Dashboard summary counts | 🔲 Pending |

**Success criteria for Phase 2:**
- All 14 endpoints return correct data from PostgreSQL
- `POST /products/{id}/simulate-sale` reduces stock and logs the sale
- `PATCH /orders/{id}/status` updates order state
- All endpoints testable via Swagger UI at `/docs` or Postman

---

## Current Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python |
| Database | PostgreSQL (via async SQLAlchemy) |
| Dashboard | Streamlit |
| Notifications | Telegram Bot |
| Containers | Docker Compose |

---

## Quick Start

```bash
git clone https://github.com/Sanket17052006/msme-inventory-automation.git
cd msme-inventory-automation

# Start PostgreSQL
docker compose up -d db

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Create tables and seed data
python backend/init_db.py
python seed_data.py

# Start the API
uvicorn backend.main:app --reload

# Open http://localhost:8000/docs
```
