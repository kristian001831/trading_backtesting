"""RSI mean-reversion strategy example."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseStrategy


class RSIReversionStrategy(BaseStrategy):
    """Buy on oversold RSI and sell on overbought RSI."""

    def __init__(
        self,
        period: int = 14,
        oversold: float = 30.0,
        overbought: float = 70.0,
        quantity: float = 1.0,
    ):
        if period <= 0:
            raise ValueError("period must be positive")
        if oversold >= overbought:
            raise ValueError("oversold must be below overbought")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.quantity = quantity

    def on_start(self, context: Dict[str, Any]) -> None:
        context.setdefault("prices", [])
        context.setdefault("orders", [])

    def on_bar(self, candle: Dict[str, Any], context: Dict[str, Any]) -> None:
        prices: List[float] = context.setdefault("prices", [])
        prices.append(float(candle["close"]))

        if len(prices) <= self.period:
            return

        rsi = self._compute_rsi(prices)
        if rsi <= self.oversold:
            context["orders"].append(self.buy(quantity=self.quantity, price=candle["close"], reason="rsi_oversold"))
        elif rsi >= self.overbought:
            context["orders"].append(self.sell(quantity=self.quantity, price=candle["close"], reason="rsi_overbought"))

    def _compute_rsi(self, prices: List[float]) -> float:
        window = prices[-(self.period + 1) :]
        gains = 0.0
        losses = 0.0
        for prev, curr in zip(window, window[1:]):
            change = curr - prev
            if change >= 0:
                gains += change
            else:
                losses -= change

        avg_gain = gains / self.period
        avg_loss = losses / self.period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
