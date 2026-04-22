from fastapi import FastAPI
from contextlib import asynccontextmanager
import redis
import uuid
import os

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global r
    r = redis.Redis(host=redis_host, port=redis_port)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    r.ping()
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}
