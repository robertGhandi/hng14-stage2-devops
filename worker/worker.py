import redis
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while True:
    try:
        job = r.brpop("job_queue", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.exceptions.ConnectionError:
        print("Redis not ready, retrying...")
        time.sleep(2)

    except Exception as e:
        print(f"Worker error: {e}")
        time.sleep(2)

