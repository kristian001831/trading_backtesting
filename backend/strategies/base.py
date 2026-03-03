"""Base strategy interfaces and helper order APIs."""

from __future__ import annotations

from abc import ABC
from typing import Any, Dict


class BaseStrategy(ABC):
    """Base strategy class used by the backtesting engine.

    Subclasses should override ``on_bar`` and can optionally override
    ``on_start`` and ``on_finish``.
    """

    def on_start(self, context: Any) -> None:
        """Called once before the first candle is processed."""

    def on_bar(self, candle: Dict[str, Any], context: Any) -> None:
        """Called for each incoming candle."""
        raise NotImplementedError("Strategies must implement on_bar")

    def on_finish(self, context: Any) -> None:
        """Called once after all candles are processed."""

    def buy(self, quantity: float = 1.0, price: float | None = None, **metadata: Any) -> Dict[str, Any]:
        """Create a buy order payload."""
        return {"side": "buy", "quantity": quantity, "price": price, **metadata}

    def sell(self, quantity: float = 1.0, price: float | None = None, **metadata: Any) -> Dict[str, Any]:
        """Create a sell order payload."""
        return {"side": "sell", "quantity": quantity, "price": price, **metadata}

    def set_stop_loss(self, price: float, **metadata: Any) -> Dict[str, Any]:
        """Create a stop-loss instruction payload."""
        return {"type": "stop_loss", "price": price, **metadata}

    def set_take_profit(self, price: float, **metadata: Any) -> Dict[str, Any]:
        """Create a take-profit instruction payload."""
        return {"type": "take_profit", "price": price, **metadata}
