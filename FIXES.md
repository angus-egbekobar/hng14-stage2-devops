# Bug Fixes

## api/main.py

| # | Line | Problem | Fix |
|---|------|---------|-----|
| 1 | 6 | `redis.Redis(host="localhost", ...)` — hardcoded `localhost` fails inside containers where Redis runs as a separate service | Changed to `os.getenv("REDIS_HOST", "redis")` |
| 2 | 6 | `port=6379` hardcoded — not configurable via environment | Changed to `int(os.getenv("REDIS_PORT", 6379))` |
| 3 | 6 | Redis client created at module level with no connection error handling — crashes the process if Redis is not yet ready at import time | Moved Redis initialisation into a FastAPI `lifespan` context manager so the app starts and the healthcheck fails cleanly rather than crashing |
| 4 | — | No `/health` endpoint — Docker and compose have no way to probe liveness | Added `GET /health` that calls `r.ping()` |
| 5 | 11 | Queue name `"job"` (singular) — inconsistent naming; renamed to `"jobs"` to match worker and make intent clear | Changed `r.lpush("job", ...)` → `r.lpush("jobs", ...)` |

## api/requirements.txt

| # | Line | Problem | Fix |
|---|------|---------|-----|
| 6 | 1-3 | No version pins on any package — builds are not reproducible and a future release can silently break the service | Pinned: `fastapi==0.111.0`, `uvicorn[standard]==0.29.0`, `redis==5.0.4` |
| 7 | — | `uvicorn` listed without extras — missing `uvloop` and `httptools` for production performance | Changed to `uvicorn[standard]` |

## worker/worker.py

| # | Line | Problem | Fix |
|---|------|---------|-----|
| 8  | 5 | `redis.Redis(host="localhost", ...)` — same container networking bug as API | Changed to `os.getenv("REDIS_HOST", "redis")` |
| 9  | 5 | `port=6379` hardcoded | Changed to `int(os.getenv("REDIS_PORT", 6379))` |
| 10 | 4 | `import signal` present but signal was never actually used — SIGTERM kills the worker mid-job with no cleanup | Implemented `handle_sigterm` that sets `running = False`, registered for both `SIGTERM` and `SIGINT` |
| 11 | — | Infinite `while True` loop with no exit condition — process cannot be stopped cleanly | Changed to `while running:` controlled by the signal handler |
| 12 | 14 | `r.brpop("job", ...)` — queue name `"job"` did not match the renamed `"jobs"` key pushed by the API | Changed to `r.brpop("jobs", ...)` |
| 13 | — | No `flush=True` on print statements — output is buffered and never appears in `docker logs` | Added `flush=True` to all print calls |

## worker/requirements.txt

| # | Line | Problem | Fix |
|---|------|---------|-----|
| 14 | 1 | No version pin on `redis` | Pinned to `redis==5.0.4` |

## frontend/app.js

| # | Line | Problem | Fix |
|---|------|---------|-----|
| 15 | 5 | `API_URL = "http://localhost:8000"` — hardcoded localhost; the frontend container cannot reach the API container via localhost | Changed to `process.env.API_URL \|\| 'http://api:8000'` |
| 16 | — | No `/health` endpoint — Docker HEALTHCHECK and compose have no way to probe frontend liveness | Added `GET /health` returning `{ status: 'ok' }` |

## docker-compose.yml

| # | Problem | Fix |
|---|---------|-----|
| 17 | File was completely empty — no services defined at all | Wrote a complete compose file with all four services |
| 18 | Redis would have been exposed on the host | Redis has no `ports:` mapping — only reachable on the internal network |
| 19 | No named network — services use the default bridge with no isolation | Added `networks: internal:` and attached all services to it |
| 20 | No `depends_on` with health conditions — services start before dependencies are ready | All services use `depends_on: condition: service_healthy` |
| 21 | No resource limits | Added `deploy.resources.limits` (CPU + memory) on every service |
| 22 | No `healthcheck` on any service | Added healthchecks for redis, api, and frontend |

## Missing files (added)

| # | File | Reason |
|---|------|--------|
| 23 | `api/Dockerfile` | Did not exist — required for containerisation |
| 24 | `worker/Dockerfile` | Did not exist |
| 25 | `frontend/Dockerfile` | Did not exist |
| 26 | `.env.example` | Did not exist — required by task; placeholder values for all env vars |
| 27 | `.gitignore` | Did not exist — `.env` would have been committed without it |
