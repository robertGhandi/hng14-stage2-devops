FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

# system safety
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# copy installed dependencies
COPY --from=builder /root/.local /home/appuser/.local

# ensure permissions are correct
RUN chown -R appuser:appuser /home/appuser

COPY --chown=appuser:appuser . .

# safer PATH setup
ENV PATH=/home/appuser/.local/bin:/usr/local/bin:$PATH

USER appuser

# healthcheck (explicit redis connection)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379)), password=os.getenv('REDIS_PASSWORD',None)); r.ping()" || exit 1

CMD ["python", "worker.py"]