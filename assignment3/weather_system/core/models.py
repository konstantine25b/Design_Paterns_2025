from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherData:
    temperature: float
    humidity: float
    wind_speed: float

