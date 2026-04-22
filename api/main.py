from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import time

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
JOB_QUEUE = os.getenv("JOB_QUEUE", "job_queue")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# 🔥 FIX: safe startup retry (prevents crash loops)


@app.on_event("startup")
def startup_event():
    for _ in range(10):
        try:
            r.ping()
            return
        except redis.exceptions.ConnectionError:
            time.sleep(2)

    raise RuntimeError("Redis unavailable after retries")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())

    try:
        r.lpush(JOB_QUEUE, job_id)
        r.hset(f"job:{job_id}", mapping={"status": "queued"})
    except redis.exceptions.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
    except redis.exceptions.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    if not status:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": status}

