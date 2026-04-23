# Stage 2 DevOps – Microservices Job Processing System

## Overview

This project is a containerized microservices job processing system consisting of:

- Frontend (Node.js) – submits and tracks jobs
- API (FastAPI) – creates jobs and returns job status
- Worker (Python) – processes jobs from a Redis queue
- Redis – shared message broker

The system is fully containerized using Docker Compose and includes a CI/CD pipeline using GitHub Actions.

## Architecture

Frontend → API → Redis → Worker → Redis → API → Frontend

All services communicate over a private Docker network called `app-network`.

## Requirements

- Docker
- Docker Compose
- Git

## Environment Variables

Create a `.env` file in the project root:

Copy `.env.example` to `.env` and update values if needed:

REDIS_HOST=redis  
REDIS_PORT=6379  
REDIS_PASSWORD=supersecretpassword123  
API_URL=http://api:8000  

## How to Run Locally

Clone the repository:

git clone https://github.com/<your-username>/hng14-stage2-devops.git  
cd hng14-stage2-devops  

Start the system:

docker compose up --build  

## Services

Frontend: http://localhost:3000  
API: http://localhost:8000  
API Docs: http://localhost:8000/docs  
Redis: internal only (not exposed externally)

## API Endpoints

Create Job:

POST /jobs  

Response:
{
  "job_id": "uuid",
  "status": "queued"
}

Get Job Status:

GET /jobs/{job_id}  

Response:
{
  "job_id": "uuid",
  "status": "completed"
}

Health Check:

GET /health  

Response:
{
  "status": "ok"
}

## CI/CD Pipeline

The pipeline runs in this strict order:

lint → test → build → security scan → integration test → deploy

### Lint
- Python (flake8)
- JavaScript (eslint)
- Dockerfiles (hadolint)

### Test
- Pytest unit tests with Redis mocked
- Coverage report generated and uploaded

### Build
- Builds Docker images for API, Worker, Frontend
- Tags images with Git SHA and latest
- Pushes to local Docker registry

### Security Scan
- Trivy scans all images
- Fails on HIGH or CRITICAL vulnerabilities
- Uploads SARIF report

### Integration Test
- Starts full stack using Docker Compose
- Submits a job via API
- Polls until completion
- Verifies final status
- Tears down stack

## Integration Test Flow

1. Start services
2. Submit job
3. Receive job ID
4. Poll job status
5. Wait for "completed"
6. Assert success
7. Tear down environment

## FIXES

All bugs found and fixed are documented in FIXES.md.

Includes:
- API response parsing fixes
- Worker queue fixes
- Docker networking fixes
- CI/CD pipeline corrections

## Security Notes

- No secrets are committed
- .env is excluded from git
- Environment variables used everywhere
- Redis is not exposed publicly
- Containers run as non-root users

## Shutdown

Stop all services:

docker compose down -v  

## Author

