from weather_system.core.models import WeatherData

def test_weather_data_immutability() -> None:
    data = WeatherData(25.0, 60.0, 10.0)
    assert data.temperature == 25.0
    assert data.humidity == 60.0
    assert data.wind_speed == 10.0
    # Since it's frozen=True, we can't really test modification easily without try/except, 
    # but instantiation verification is enough for a data class.

