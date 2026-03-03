from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_run_backtest_and_fetch_result() -> None:
    payload = {
        "strategy": "sma_cross",
        "params": {"short_window": 10, "long_window": 30, "direction": "long"},
        "start_date": "2024-01-01",
        "end_date": "2024-01-05",
        "symbol": "BTCUSD",
        "timeframe": "1d",
    }

    run_response = client.post("/api/backtest/run", json=payload)
    assert run_response.status_code == 200
    run_body = run_response.json()
    assert "run_id" in run_body
    assert run_body["status"] == "completed"

    result_response = client.get(f"/api/backtest/result/{run_body['run_id']}")
    assert result_response.status_code == 200
    result_body = result_response.json()
    assert result_body["strategy"] == payload["strategy"]
    assert result_body["metrics"]["total_trades"] == 1
    assert len(result_body["trades"]) == 1
    assert len(result_body["equity_curve"]) == 5


def test_run_backtest_validation_error() -> None:
    payload = {
        "strategy": "sma_cross",
        "params": {"short_window": 30, "long_window": 10},
        "start_date": "2024-01-01",
        "end_date": "2024-01-05",
        "symbol": "BTCUSD",
        "timeframe": "1d",
    }

    response = client.post("/api/backtest/run", json=payload)
    assert response.status_code == 400
    assert "short_window must be less than long_window" in response.json()["detail"]


def test_get_unknown_run_id() -> None:
    response = client.get("/api/backtest/result/not-found")
    assert response.status_code == 404
    assert response.json()["detail"] == "Run ID not found"
