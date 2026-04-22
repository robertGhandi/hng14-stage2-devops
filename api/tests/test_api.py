from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("main.r")
def test_create_job(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    assert "job_id" in response.json()


@patch("main.r")
def test_get_job(mock_redis):
    mock_redis.hget.return_value = "queued"

    response = client.get("/jobs/test-id")

    assert response.status_code == 200
    assert response.json()["status"] == "queued"
