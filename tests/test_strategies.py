from backend.strategies.base import BaseStrategy
from backend.strategies.loader import load_strategy
from backend.strategies.rsi_reversion import RSIReversionStrategy
from backend.strategies.sma_cross import SMACrossStrategy


class HookTrackingStrategy(BaseStrategy):
    def on_start(self, context):
        context["events"].append("start")

    def on_bar(self, candle, context):
        context["events"].append(("bar", candle["close"]))
        context["orders"].append(self.buy(quantity=1, price=candle["close"]))

    def on_finish(self, context):
        context["events"].append("finish")


def run_backtest(strategy, closes):
    context = {"events": [], "orders": []}
    strategy.on_start(context)
    for close in closes:
        strategy.on_bar({"close": close}, context)
    strategy.on_finish(context)
    return context


def test_hooks_are_invoked_in_order():
    context = run_backtest(HookTrackingStrategy(), [100, 101])
    assert context["events"] == ["start", ("bar", 100), ("bar", 101), "finish"]


def test_base_helper_payloads_are_generated():
    strategy = HookTrackingStrategy()

    assert strategy.buy(quantity=2, price=101) == {"side": "buy", "quantity": 2, "price": 101}
    assert strategy.sell(quantity=1.5, price=99) == {"side": "sell", "quantity": 1.5, "price": 99}
    assert strategy.set_stop_loss(95) == {"type": "stop_loss", "price": 95}
    assert strategy.set_take_profit(110) == {"type": "take_profit", "price": 110}


def test_sma_cross_generates_orders():
    strategy = SMACrossStrategy(short_window=2, long_window=3, quantity=1)
    context = run_backtest(strategy, [100, 101, 102, 100, 99])

    assert len(context["orders"]) >= 2
    assert context["orders"][0]["side"] == "buy"
    assert any(order["side"] == "sell" for order in context["orders"])


def test_rsi_reversion_generates_buy_and_sell_signals():
    strategy = RSIReversionStrategy(period=2, oversold=30, overbought=70, quantity=1)
    context = run_backtest(strategy, [100, 102, 104, 100, 96, 99, 103])

    sides = [order["side"] for order in context["orders"]]
    assert "sell" in sides
    assert "buy" in sides


def test_dynamic_loader_instantiates_strategy():
    strategy = load_strategy("backend.strategies.sma_cross", "SMACrossStrategy", short_window=2, long_window=3)
    assert isinstance(strategy, SMACrossStrategy)
