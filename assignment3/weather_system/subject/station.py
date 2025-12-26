from ..core.interfaces import Observer, Subject
from ..core.models import WeatherData


class WeatherStation(Subject):
    def __init__(self) -> None:
        self._head: Observer | None = None
        self._data: WeatherData | None = None

    def register_observer(self, observer: Observer) -> None:
        if not self._head:
            self._head = observer
        else:
            current = self._head
            while current.next_observer:
                if current == observer:
                    return
                current = current.next_observer

            if current == observer:
                return

            current.set_next(observer)

        if self._data:
            observer.handle(self._data)

    def remove_observer(self, observer: Observer) -> None:
        if not self._head:
            return

        if self._head == observer:
            self._head = self._head.next_observer
            observer.next_observer = None
            return

        current = self._head
        while current.next_observer:
            if current.next_observer == observer:
                current.next_observer = observer.next_observer
                observer.next_observer = None
                return
            current = current.next_observer

    def notify_observers(self) -> None:
        if self._data and self._head:
            self._head.handle(self._data)

    def set_measurements(
        self, temperature: float, humidity: float, wind_speed: float
    ) -> None:
        self._data = WeatherData(temperature, humidity, wind_speed)
        self.notify_observers()
