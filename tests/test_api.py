from fastapi.testclient import TestClient

from phantomscope.api.dependencies import get_analysis_service
from phantomscope.api.main import app
from phantomscope.core.config import Settings
from phantomscope.services.analysis import AnalysisService


def build_client(tmp_path):
    settings = Settings(
        database_url=f"sqlite:///{tmp_path}/phantomscope-api-test.db",
        offline_mode=True,
    )
    service = AnalysisService(settings)
    app.dependency_overrides[get_analysis_service] = lambda: service
    return TestClient(app)


def test_create_and_fetch_analysis_via_api(tmp_path) -> None:
    client = build_client(tmp_path)

    create_response = client.post(
        "/api/v1/analyses",
        json={
            "target": "acme",
            "target_type": "brand",
            "offline_mode": True,
            "max_variants": 8,
        },
    )
    assert create_response.status_code == 200
    payload = create_response.json()
    assert payload["assets"]
    assert payload["summary"]["headline"]

    fetch_response = client.get(f"/api/v1/analyses/{payload['analysis_id']}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["analysis_id"] == payload["analysis_id"]

    app.dependency_overrides.clear()


def test_list_recent_analyses_via_api(tmp_path) -> None:
    client = build_client(tmp_path)

    for target in ["acme", "contoso"]:
        response = client.post(
            "/api/v1/analyses",
            json={
                "target": target,
                "target_type": "brand",
                "offline_mode": True,
                "max_variants": 8,
            },
        )
        assert response.status_code == 200

    list_response = client.get("/api/v1/analyses?limit=5")
    assert list_response.status_code == 200
    payload = list_response.json()
    assert len(payload["analyses"]) == 2
    assert payload["analyses"][0]["summary_headline"]

    app.dependency_overrides.clear()


def test_validation_errors_are_structured(tmp_path) -> None:
    client = build_client(tmp_path)

    response = client.post(
        "/api/v1/analyses",
        json={
            "target": "!!!",
            "target_type": "brand",
            "offline_mode": True,
            "max_variants": 8,
        },
    )
    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"

    app.dependency_overrides.clear()
