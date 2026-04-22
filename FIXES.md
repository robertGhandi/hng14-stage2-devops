# FIXES.md

## API Service Fixes

---

### 1. Redis connection hardcoded to localhost

- **File:** api/main.py  
- **Line:** 11  

- **Problem:**  
Redis was configured to use `localhost`, which works only in local development.  
In a Docker environment, `localhost` refers to the API container itself, not the Redis service. This caused connection failure between API and Redis.

- **Fix:**  
Replaced hardcoded host with environment variable `REDIS_HOST`, defaulting to `redis` (Docker service name).

---

### 2. Missing environment variable usage for Redis configuration

- **File:** api/main.py  
- **Line:** 11–13  

- **Problem:**  
Redis password and host configuration were not loaded from environment variables, making the application non-portable and insecure for production deployment.

- **Fix:**  
Introduced environment variable support using `os.getenv()` for:
- REDIS_HOST
- REDIS_PORT
- REDIS_PASSWORD

---

### 3. Redis response decoding inconsistency

- **File:** api/main.py  
- **Line:** 21–26  

- **Problem:**  
Redis values were returned as bytes and manually decoded using `.decode()` in some places only, causing inconsistent behavior.

- **Fix:**  
Enabled `decode_responses=True` in Redis client configuration to ensure all responses are automatically returned as strings.

---

### 4. Inconsistent Redis key naming

- **File:** api/main.py  
- **Line:** 16–18  

- **Problem:**  
Queue key was named `job`, which is unclear and not scalable for multiple job types.

- **Fix:**  
Renamed Redis queue key from `job` to `job_queue` for clarity and maintainability.

---

### 5. Missing structured Redis HSET usage

- **File:** api/main.py  
- **Line:** 17  

- **Problem:**  
Redis hash fields were being set individually instead of using structured mapping.

- **Fix:**  
Replaced multiple `hset` calls with:
`r.hset(f"job:{job_id}", mapping={"status": "queued"})`
for cleaner and atomic updates.

## Frontend Service Fixes

---

### 1. Hardcoded API URL breaks container deployment

- **File:** frontend/app.js  
- **Line:** 5  

- **Problem:**  
The API base URL was hardcoded as `http://localhost:8000`, which only works in local development.  
In a Docker environment, `localhost` refers to the frontend container itself, not the API service, causing failed requests.

- **Fix:**  
Replaced hardcoded URL with environment-based configuration using `API_URL` so the service can communicate across containers in Docker Compose.

---

### 2. Missing API proxy configuration between frontend and backend

- **File:** frontend/app.js  
- **Line:** 8–22  

- **Problem:**  
Frontend assumed same-origin API routing (`/submit`, `/status/:id`) without configuring a reverse proxy.  
This causes request failures unless explicitly handled in production.

- **Fix:**  
Explicitly routed requests through Axios using backend service URL instead of relying on same-origin assumptions.

---

### 3. Lack of error handling in frontend API responses

- **File:** frontend/app.js  
- **Line:** 10–25  

- **Problem:**  
API responses were parsed without validating response status codes.  
This causes silent failures or uncaught exceptions when API returns errors or non-JSON responses.

- **Fix:**  
Added try/catch blocks around API calls and return structured error messages to the UI.

---

### 4. Static file serving path not production-safe

- **File:** frontend/app.js  
- **Line:** 6  

- **Problem:**  
Static files are served from a fixed `views` directory path which may break in containerized environments if working directory changes.

- **Fix:**  
Ensured static path uses `__dirname` to guarantee correct resolution inside Docker containers.

## Worker Service Fixes

---

### 1. Redis connection hardcoded to localhost

- **File:** worker/worker.py  
- **Line:** 5  

- **Problem:**  
Redis connection was hardcoded to `localhost`, which fails in Docker since services run in separate containers.

- **Fix:**  
Replaced with environment variables (`REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`) and defaulted host to `redis`.

---

### 2. Queue name mismatch between API and worker

- **File:** worker/worker.py  
- **Line:** 16  

- **Problem:**  
Worker was consuming jobs from queue `job`, while API was pushing jobs to `job_queue`.  
This caused jobs to never be processed.

- **Fix:**  
Updated worker to consume from `job_queue` to match API.

---

### 3. Missing environment variable configuration

- **File:** worker/worker.py  
- **Line:** 5–7  

- **Problem:**  
Redis connection settings were hardcoded, making the service non-configurable and unsuitable for production environments.

- **Fix:**  
Introduced environment variable configuration using `os.getenv()`.

---

### 4. No graceful shutdown handling

- **File:** worker/worker.py  
- **Line:** 13  

- **Problem:**  
Worker ran in an infinite loop without handling termination signals, preventing clean shutdown during container restarts or deployments.

- **Fix:**  
Added signal handlers (`SIGTERM`, `SIGINT`) to allow graceful shutdown.

---

### 5. Manual decoding of Redis responses

- **File:** worker/worker.py  
- **Line:** 19  

- **Problem:**  
Redis responses were manually decoded using `.decode()`, leading to inconsistent data handling.

- **Fix:**  
Enabled `decode_responses=True` in Redis client configuration.

### X. Misplaced environment configuration file

- **File:** api/.env  

- **Problem:**  
Environment variables were stored inside the API service directory, which is not recognized by Docker Compose. This caused missing configuration during container startup.

- **Fix:**  
Moved `.env` file to the project root where `docker-compose.yml` is located, and ensured variables are injected correctly into all services.

## Infrastructure Fixes

---

### 1. Redis exposed publicly

- **File:** docker-compose.yml  
- **Problem:**  
Redis was initially exposed to host, creating a security risk.

- **Fix:**  
Removed port binding to keep Redis internal only.

---

### 2. Missing service health checks

- **File:** Dockerfiles / docker-compose.yml  

- **Problem:**  
Services started without verifying readiness, causing race conditions.

- **Fix:**  
Added HEALTHCHECK instructions and `depends_on: condition: service_healthy`.

---

### 3. Containers running as root

- **File:** all Dockerfiles  

- **Problem:**  
Containers ran as root, violating security best practices.

- **Fix:**  
Created and switched to non-root users in all services.