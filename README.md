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

## Current State (Phase 1 — Foundation)

The backend infrastructure is fully set up and running:

- **FastAPI** application with async SQLAlchemy + PostgreSQL
- **4 database models**: `products`, `orders`, `suppliers`, `sales_log`
- **Pydantic schemas** for all request/response validation
- **Clean layered architecture**: routes → controllers → services
- **Docker Compose** with PostgreSQL service
- `GET /health` endpoint returning `{"status": "ok"}`

Verified working with PostgreSQL running locally and FastAPI serving on port 8000.

---

## Phase 2 — Core API Implementation

The 13 REST API endpoints need to be implemented across routes, controllers, and services to power the full inventory workflow:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/products` | List all products with stock levels |
| `GET` | `/products/{id}` | Single product details |
| `GET` | `/products/low-stock` | Products where stock < reorder_point |
| `POST` | `/products/{id}/simulate-sale` | Reduce stock by qty (demo trigger) |
| `GET` | `/orders` | List orders (filterable by status) |
| `GET` | `/orders/{id}` | Single order details |
| `POST` | `/orders` | Create a new order manually |
| `PATCH` | `/orders/{id}/status` | Confirm, reject, or fulfill an order |
| `GET` | `/suppliers` | List all suppliers |
| `GET` | `/suppliers/{id}` | Single supplier details |
| `GET` | `/sales-log` | Sales history for charts |
| `GET` | `/analytics/summary` | Dashboard summary counts |
| `GET` | `/health` | Health check |

**Success criteria for Phase 2:**
- All 13 endpoints return correct data from PostgreSQL
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
