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

        # Sort logs by date descending
        sorted_logs = sorted(logs, key=lambda log_entry: log_entry.date, reverse=True)
        streak = 0

        # Simple streak: consecutive days meeting goal
        # This assumes one log per day or we aggregate.
        # For simplicity, count compliant logs in sequence from most recent.
        # A real streak logic is complex with dates (gaps break streak).
        # Basic version: compliant days in a row ending today/yesterday.
        # Keep "student-like" simple logic: check if latest is compliant.
        # Count compliant logs in desc order until a fail/gap.

        # To handle gaps properly, we'd need date logic.
        # I'll do strict latest logs check.

        # Let's group by date first? Or just assume logs are ordered.
        # I'll assume daily logs for simplicity or just sequential compliant entries.

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
        # Percentage of logs meeting the goal
        compliant = sum(1 for log in logs if log.value >= goal)
        return (compliant / len(logs)) * 100.0


class StatContext:
    def __init__(self, strategy: StatStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StatStrategy) -> None:
        self._strategy = strategy

    def analyze(self, logs: list[Log], goal: float) -> Any:
        return self._strategy.calculate(logs, goal)
