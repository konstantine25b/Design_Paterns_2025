from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .habits import Log


class StatStrategy(ABC):
    @abstractmethod
    def calculate(self, logs: list[Log], goal: float) -> Any:
        pass


class TotalProgressStrategy(StatStrategy):
    def calculate(self, logs: list[Log], _goal: float) -> float:
        return sum(log.value for log in logs)


class CurrentStreakStrategy(StatStrategy):
    def calculate(self, logs: list[Log], goal: float) -> int:
        if not logs:
            return 0

        sorted_logs = sorted(logs, key=lambda log_entry: log_entry.date, reverse=True)
        streak = 0

        for log in sorted_logs:
            if log.value >= goal:
                streak += 1
            else:
                break
        return streak


class CompletionRateStrategy(StatStrategy):
    def calculate(self, logs: list[Log], goal: float) -> float:
        if not logs:
            return 0.0
        compliant = sum(1 for log in logs if log.value >= goal)
        return (compliant / len(logs)) * 100.0


class StatContext:
    def __init__(self, strategy: StatStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StatStrategy) -> None:
        self._strategy = strategy

    def analyze(self, logs: list[Log], goal: float) -> Any:
        return self._strategy.calculate(logs, goal)
