from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any
from uuid import uuid4

from backend.api.schemas import BacktestResultResponse, BacktestRunRequest, EquityPoint, Metrics, Trade


class StrategyValidationError(ValueError):
    """Raised when strategy parameters are invalid."""


@dataclass
class Candle:
    timestamp: date
    open: float
    high: float
    low: float
    close: float
    volume: float


class Backtester:
    """Simple backtester interface implementation."""

    @staticmethod
    def run(*, strategy: str, params: dict[str, Any], candles: list[Candle]) -> dict[str, Any]:
        if not candles:
            return {
                "metrics": {"total_return": 0.0, "win_rate": 0.0, "total_trades": 0, "max_drawdown": 0.0},
                "trades": [],
                "equity_curve": [],
            }

        entry = candles[0]
        exit_ = candles[-1]
        direction = 1 if params.get("direction", "long") == "long" else -1
        pnl = (exit_.close - entry.open) * direction
        total_return = pnl / entry.open if entry.open else 0.0

        return {
            "metrics": {
                "total_return": round(total_return, 6),
                "win_rate": 1.0 if pnl > 0 else 0.0,
                "total_trades": 1,
                "max_drawdown": round(min(total_return, 0.0), 6),
            },
            "trades": [
                {
                    "entry_time": entry.timestamp,
                    "exit_time": exit_.timestamp,
                    "side": params.get("direction", "long"),
                    "pnl": round(pnl, 2),
                }
            ],
            "equity_curve": [
                {"timestamp": c.timestamp, "equity": round(10000.0 + (c.close - entry.open) * direction, 2)}
                for c in candles
            ],
        }


class BacktestService:
    def __init__(self) -> None:
        self._runs: dict[str, BacktestResultResponse] = {}

    def run_backtest(self, payload: BacktestRunRequest) -> str:
        self.validate_strategy_parameters(payload.strategy, payload.params)
        candles = self.load_historical_candles(
            symbol=payload.symbol,
            timeframe=payload.timeframe,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
        raw_result = Backtester.run(strategy=payload.strategy, params=payload.params, candles=candles)
        run_id = str(uuid4())
        self._runs[run_id] = BacktestResultResponse(
            run_id=run_id,
            strategy=payload.strategy,
            status="completed",
            metrics=Metrics(**raw_result["metrics"]),
            trades=[Trade(**trade) for trade in raw_result["trades"]],
            equity_curve=[EquityPoint(**point) for point in raw_result["equity_curve"]],
        )
        return run_id

    def get_result(self, run_id: str) -> BacktestResultResponse | None:
        return self._runs.get(run_id)

    def validate_strategy_parameters(self, strategy: str, params: dict[str, Any]) -> None:
        rules: dict[str, dict[str, tuple[float, float]]] = {
            "sma_cross": {"short_window": (2, 200), "long_window": (5, 400)},
            "rsi_reversion": {"period": (2, 100), "oversold": (1, 50), "overbought": (50, 99)},
        }
        if strategy not in rules:
            raise StrategyValidationError(f"Unsupported strategy: {strategy}")

        for name, (minimum, maximum) in rules[strategy].items():
            if name not in params:
                raise StrategyValidationError(f"Missing required parameter: {name}")
            value = params[name]
            if not isinstance(value, (int, float)):
                raise StrategyValidationError(f"Parameter {name} must be numeric")
            if not minimum <= value <= maximum:
                raise StrategyValidationError(
                    f"Parameter {name} must be between {minimum} and {maximum}, got {value}"
                )

        if strategy == "sma_cross" and params["short_window"] >= params["long_window"]:
            raise StrategyValidationError("short_window must be less than long_window")

    def load_historical_candles(
        self, *, symbol: str, timeframe: str, start_date: date, end_date: date
    ) -> list[Candle]:
        if end_date < start_date:
            raise StrategyValidationError("end_date must be on or after start_date")

        days = (end_date - start_date).days
        candles: list[Candle] = []
        for i in range(days + 1):
            ts = start_date + timedelta(days=i)
            base = 100 + i
            candles.append(
                Candle(
                    timestamp=ts,
                    open=base,
                    high=base + 1,
                    low=base - 1,
                    close=base + 0.5,
                    volume=1000 + i * 10,
                )
            )
        return candles
