import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mock_redis = MagicMock()

with patch("redis.Redis", return_value=mock_redis):
    from main import app

import main
main.r = mock_redis

from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)


def setup_function():
    mock_redis.reset_mock()


def test_health_ok():
    mock_redis.ping.return_value = True
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_job_returns_job_id():
    resp = client.post("/jobs")
    assert resp.status_code == 200
    data = resp.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36


def test_create_job_pushes_to_redis():
    resp = client.post("/jobs")
    job_id = resp.json()["job_id"]
    mock_redis.lpush.assert_called_with("jobs", job_id)
    mock_redis.hset.assert_called_with(f"job:{job_id}", "status", "queued")


def test_get_job_found():
    mock_redis.hget.return_value = b"completed"
    resp = client.get("/jobs/some-id")
    assert resp.status_code == 200
    assert resp.json() == {"job_id": "some-id", "status": "completed"}


def test_get_job_not_found():
    mock_redis.hget.return_value = None
    resp = client.get("/jobs/missing-id")
    assert resp.status_code == 200
    assert resp.json() == {"error": "not found"}
