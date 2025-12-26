from ..core.interfaces import Observer
from ..core.models import WeatherData


class WeatherDisplay(Observer):
    def __init__(self) -> None:
        super().__init__()

    def update(self, data: WeatherData) -> None:
        print(
            f"WeatherDisplay: Showing Temperature = {data.temperature}°C, "
            f"Humidity = {data.humidity}%, Wind Speed = {data.wind_speed} km/h"
        )
