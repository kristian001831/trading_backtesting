"""Dynamic strategy loader utilities."""

from __future__ import annotations

import importlib
from typing import Any

from .base import BaseStrategy


def load_strategy(module_path: str, class_name: str, **kwargs: Any) -> BaseStrategy:
    """Load and instantiate a strategy class from a module path and class name."""
    module = importlib.import_module(module_path)

    try:
        strategy_cls = getattr(module, class_name)
    except AttributeError as exc:
        raise ImportError(f"Class '{class_name}' not found in module '{module_path}'") from exc

    instance = strategy_cls(**kwargs)
    if not isinstance(instance, BaseStrategy):
        raise TypeError(f"Loaded class '{class_name}' must inherit from BaseStrategy")

    return instance
