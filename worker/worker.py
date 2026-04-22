import redis
import time
import os
import signal
import sys

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port)

running = True


def handle_sigterm(signum, frame):
    global running
    print("SIGTERM received, shutting down gracefully...", flush=True)
    running = False


signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


def process_job(job_id):
    print(f"Processing job {job_id}", flush=True)
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}", flush=True)


while running:
    job = r.brpop("jobs", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id.decode())

sys.exit(0)
