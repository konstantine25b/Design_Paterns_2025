from weather_system.core.models import WeatherData


def test_weather_data_immutability() -> None:
    data = WeatherData(25.0, 60.0, 10.0)
    assert data.temperature == 25.0
    assert data.humidity == 60.0
    assert data.wind_speed == 10.0
