from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.schemas import BacktestResultResponse, BacktestRunRequest, BacktestRunResponse
from backend.api.services.backtest_service import BacktestService, StrategyValidationError

app = FastAPI(title="Trading Backtesting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = BacktestService()


@app.post("/api/backtest/run", response_model=BacktestRunResponse)
def run_backtest(payload: BacktestRunRequest) -> BacktestRunResponse:
    try:
        run_id = service.run_backtest(payload)
    except StrategyValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BacktestRunResponse(run_id=run_id, status="completed")


@app.get("/api/backtest/result/{run_id}", response_model=BacktestResultResponse)
def get_backtest_result(run_id: str) -> BacktestResultResponse:
    result = service.get_result(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return result
