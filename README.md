# trading_backtesting

A lightweight backtesting scaffold with pluggable strategy classes.

## Strategy API

Create a strategy by inheriting from `BaseStrategy` and implementing hooks:

- `on_start(context)`: called once before candles are processed.
- `on_bar(candle, context)`: called for every candle.
- `on_finish(context)`: called once after the run is complete.

Helper methods provided by the base class:

- `buy(...)`
- `sell(...)`
- `set_stop_loss(...)`
- `set_take_profit(...)`

Example:

```python
from backend.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    def on_start(self, context):
        context.setdefault("orders", [])

    def on_bar(self, candle, context):
        if candle["close"] < 100:
            context["orders"].append(self.buy(quantity=1, price=candle["close"]))

    def on_finish(self, context):
        print(f"Generated {len(context['orders'])} orders")
```

## Built-in example strategies

- `backend/strategies/sma_cross.py`: moving-average crossover strategy.
- `backend/strategies/rsi_reversion.py`: RSI mean-reversion strategy.

## Dynamic strategy loading

Use `load_strategy(module_path, class_name, **kwargs)` to load any strategy class dynamically:

```python
from backend.strategies.loader import load_strategy

strategy = load_strategy(
    "backend.strategies.sma_cross",
    "SMACrossStrategy",
    short_window=5,
    long_window=20,
    quantity=1,
)
```

## Running a strategy

A minimal run loop:

```python
context = {"orders": []}
strategy.on_start(context)
for candle in candles:
    strategy.on_bar(candle, context)
strategy.on_finish(context)
```

Run tests:

```bash
pytest
```
