from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class BacktestRunRequest(BaseModel):
    strategy: str = Field(..., min_length=1)
    params: dict[str, Any] = Field(default_factory=dict)
    start_date: date
    end_date: date
    symbol: str = Field(default="BTCUSD", min_length=1)
    timeframe: str = Field(default="1d", min_length=1)


class BacktestRunResponse(BaseModel):
    run_id: str
    status: str


class Metrics(BaseModel):
    total_return: float
    win_rate: float
    total_trades: int
    max_drawdown: float


class Trade(BaseModel):
    entry_time: date
    exit_time: date
    side: str
    pnl: float


class EquityPoint(BaseModel):
    timestamp: date
    equity: float


class BacktestResultResponse(BaseModel):
    run_id: str
    strategy: str
    status: str
    metrics: Metrics
    trades: list[Trade]
    equity_curve: list[EquityPoint]


class ErrorResponse(BaseModel):
    detail: str
