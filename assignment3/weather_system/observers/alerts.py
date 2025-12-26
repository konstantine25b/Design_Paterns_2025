import random

from ..core.interfaces import Observer
from ..core.models import WeatherData


class TemperatureAlert(Observer):
    def __init__(self) -> None:
        super().__init__()
        self._threshold = random.randint(30, 40)

    def update(self, data: WeatherData) -> None:
        if data.temperature > self._threshold:
            print(
                f"TemperatureAlert: **Alert! Temperature exceeded "
                f"{self._threshold}°C: {data.temperature}°C**"
            )


class WindSpeedAlert(Observer):
    def __init__(self) -> None:
        super().__init__()
        self._last_wind_speed: float | None = None
        self._trend_count = 0

    def update(self, data: WeatherData) -> None:
        if self._last_wind_speed is not None:
            if data.wind_speed > self._last_wind_speed:
                self._trend_count += 1
                if self._trend_count >= 1:
                    print(
                        f"WindSpeedAlert: **Alert! Wind speed is increasing: "
                        f"{self._last_wind_speed} km/h -> {data.wind_speed} km/h**"
                    )
            else:
                self._trend_count = 0

        self._last_wind_speed = data.wind_speed


class HumidityAlert(Observer):
    def __init__(self) -> None:
        super().__init__()
        self._threshold = random.randint(70, 90)

    def update(self, data: WeatherData) -> None:
        if data.humidity > self._threshold:
            print(
                f"HumidityAlert: **Alert! Humidity exceeded "
                f"{self._threshold}%: {data.humidity}%**"
            )
