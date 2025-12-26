from __future__ import annotations

from abc import ABC, abstractmethod

from .models import WeatherData


class Observer(ABC):
    def __init__(self) -> None:
        self.next_observer: Observer | None = None

    def set_next(self, observer: Observer) -> Observer:
        self.next_observer = observer
        return observer

    def handle(self, data: WeatherData) -> None:
        self.update(data)
        if self.next_observer:
            self.next_observer.handle(data)

    @abstractmethod
    def update(self, data: WeatherData) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass
