
import requests

BASE = "http://127.0.0.1:8081"

def test_health_endpoint():
    requests.post(f"{BASE}/simulate/up", timeout=3)
    response = requests.get(f"{BASE}/health", timeout=3)
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_outage_and_recovery():
    requests.post(f"{BASE}/simulate/down", timeout=3)
    assert requests.get(f"{BASE}/health", timeout=3).status_code == 503

    requests.post(f"{BASE}/simulate/up", timeout=3)
    assert requests.get(f"{BASE}/health", timeout=3).status_code == 200

def test_monitoring_services():
    assert requests.get(
        "http://127.0.0.1:9090/-/ready", timeout=5
    ).status_code == 200

    assert requests.get(
        "http://127.0.0.1:8090/", timeout=5
    ).status_code == 200
