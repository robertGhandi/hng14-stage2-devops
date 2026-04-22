FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

# system safety
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /home/appuser/.local

COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

# FIX: safer healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD python -c "import redis, os; redis.Redis(host=os.getenv('REDIS_HOST','redis')).ping()" || exit 1

CMD ["python", "worker.py"]