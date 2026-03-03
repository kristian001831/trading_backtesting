"""Simple moving-average crossover strategy example."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseStrategy


class SMACrossStrategy(BaseStrategy):
    """Buy when short SMA crosses above long SMA, sell on bearish cross."""

    def __init__(self, short_window: int = 5, long_window: int = 20, quantity: float = 1.0):
        if short_window <= 0 or long_window <= 0:
            raise ValueError("SMA windows must be positive")
        if short_window >= long_window:
            raise ValueError("short_window must be smaller than long_window")
        self.short_window = short_window
        self.long_window = long_window
        self.quantity = quantity

    def on_start(self, context: Dict[str, Any]) -> None:
        context.setdefault("prices", [])
        context.setdefault("orders", [])
        context["last_signal"] = None

    def on_bar(self, candle: Dict[str, Any], context: Dict[str, Any]) -> None:
        prices: List[float] = context.setdefault("prices", [])
        prices.append(float(candle["close"]))

        if len(prices) < self.long_window:
            return

        short_sma = sum(prices[-self.short_window :]) / self.short_window
        long_sma = sum(prices[-self.long_window :]) / self.long_window
        signal = "long" if short_sma > long_sma else "short"

        if signal == context.get("last_signal"):
            return

        if signal == "long":
            context["orders"].append(self.buy(quantity=self.quantity, price=candle["close"], reason="sma_cross"))
        else:
            context["orders"].append(self.sell(quantity=self.quantity, price=candle["close"], reason="sma_cross"))

        context["last_signal"] = signal
