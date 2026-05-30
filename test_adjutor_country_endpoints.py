import json
import os
import time
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("ADJUTOR_BASE_URL", "https://adjutor.lendsqr.com/v2").rstrip("/")
API_KEY = os.getenv("ADJUTOR_API_KEY", "")
TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "30"))
PERFORMANCE_THRESHOLD_MS = int(os.getenv("PERFORMANCE_THRESHOLD_MS", "3000"))

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "endpoints.json"


def load_endpoint_cases():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    cases = []
    for module_name, endpoints in data["modules"].items():
        for endpoint in endpoints:
            endpoint["module"] = module_name
            cases.append(endpoint)
    return cases


def build_path(path, path_params=None):
    path_params = path_params or {}
    for key, value in path_params.items():
        path = path.replace("{" + key + "}", str(value))
    return path


@pytest.mark.parametrize("case", load_endpoint_cases(), ids=lambda case: f"{case['module']}::{case['name']}")
def test_adjutor_country_endpoint_status_response_and_performance(case):
    assert API_KEY, "ADJUTOR_API_KEY is required. Add it to your local .env file. Do not commit real keys."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    method = case.get("method", "GET").upper()
    path = build_path(case["path"], case.get("path_params"))
    url = f"{BASE_URL}{path}"

    started_at = time.perf_counter()
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=case.get("query_params"),
        json=case.get("body"),
        timeout=TIMEOUT,
    )
    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)

    print(f"\nMODULE={case['module']} ENDPOINT={case['name']} STATUS={response.status_code} RESPONSE_TIME_MS={elapsed_ms}")
    print(response.text[:1000])

    assert response.status_code == case.get("expected_status", 200)
    assert elapsed_ms <= PERFORMANCE_THRESHOLD_MS, f"Response time {elapsed_ms}ms exceeded {PERFORMANCE_THRESHOLD_MS}ms"

    try:
        body = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    expected_text = case.get("expected_message_contains", "")
    if expected_text:
        assert expected_text.lower() in json.dumps(body).lower()
    else:
        assert isinstance(body, dict), "Expected a JSON object response"
