# HNG14 Stage 2 DevOps — Job Processing System

A containerised multi-service job processing application consisting of:

- **frontend** — Node.js/Express UI (port 3000)
- **api** — Python/FastAPI job management (port 8000, internal only)
- **worker** — Python background job processor
- **redis** — Queue and state store (internal only, not exposed)

---

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.20
- Git

---

## Quick Start (clean machine)

```bash
# 1. Clone your fork
git clone https://github.com/<your-username>/hng14-stage2-devops.git
cd hng14-stage2-devops

# 2. Copy env file and adjust if needed
cp .env.example .env

# 3. Build and start everything
docker compose up --build -d

# 4. Check all services are healthy
docker compose ps
```

Open http://localhost:3000 in your browser.

---

## What a Successful Startup Looks Like
NAME                STATUS          PORTS
redis               healthy
api                 healthy
worker              Up (no port)
frontend            healthy         0.0.0.0:3000->3000/tcp

All four services should show **Up**. The three with healthchecks (redis, api, frontend) should show **healthy** within ~30 seconds.

---

## Usage

1. Click **Submit New Job** — a job ID appears and polling starts
2. The worker picks it up within seconds and marks it `completed`
3. The dashboard updates automatically

---

## Environment Variables

See `.env.example` for all variables. Key ones:

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `redis` | Redis service hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `API_URL` | `http://api:8000` | API base URL (used by frontend) |
| `FRONTEND_PORT` | `3000` | Host port for the frontend |

---

## Running Tests Locally

```bash
cd api
pip install -r requirements.txt pytest pytest-cov
pytest tests/ -v --cov=. --cov-report=term
```

---

## Stopping the Stack

```bash
docker compose down          # stop and remove containers
docker compose down -v       # also remove volumes
```
