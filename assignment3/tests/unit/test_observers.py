from unittest.mock import MagicMock, patch

from weather_system.core.models import WeatherData
from weather_system.observers.alerts import (
    HumidityAlert,
    TemperatureAlert,
    WindSpeedAlert,
)


class TestTemperatureAlert:
    def test_should_initialize_with_random_threshold(self) -> None:
        with patch("random.randint", return_value=35):
            alert = TemperatureAlert()
            assert alert._threshold == 35

    def test_should_alert_when_temperature_exceeds_threshold(self) -> None:
        with patch("random.randint", return_value=30):
            alert = TemperatureAlert()
            mock_print = MagicMock()
            with patch("builtins.print", mock_print):
                alert.update(WeatherData(31.0, 50.0, 10.0))
                mock_print.assert_called_once()
                assert "30°C: 31.0°C" in mock_print.call_args[0][0]

    def test_should_not_alert_when_temperature_equals_threshold(self) -> None:
        with patch("random.randint", return_value=30):
            alert = TemperatureAlert()
            mock_print = MagicMock()
            with patch("builtins.print", mock_print):
                alert.update(WeatherData(30.0, 50.0, 10.0))
                mock_print.assert_not_called()

    def test_should_not_alert_when_temperature_is_below_threshold(self) -> None:
        with patch("random.randint", return_value=30):
            alert = TemperatureAlert()
            mock_print = MagicMock()
            with patch("builtins.print", mock_print):
                alert.update(WeatherData(29.0, 50.0, 10.0))
                mock_print.assert_not_called()

class TestHumidityAlert:
    def test_should_initialize_with_random_threshold(self) -> None:
        with patch("random.randint", return_value=80):
            alert = HumidityAlert()
            assert alert._threshold == 80

    def test_should_alert_when_humidity_exceeds_threshold(self) -> None:
        with patch("random.randint", return_value=80):
            alert = HumidityAlert()
            mock_print = MagicMock()
            with patch("builtins.print", mock_print):
                alert.update(WeatherData(25.0, 81.0, 10.0))
                mock_print.assert_called_once()
                assert "80%: 81.0%" in mock_print.call_args[0][0]

    def test_should_not_alert_when_humidity_equals_threshold(self) -> None:
        with patch("random.randint", return_value=80):
            alert = HumidityAlert()
            mock_print = MagicMock()
            with patch("builtins.print", mock_print):
                alert.update(WeatherData(25.0, 80.0, 10.0))
                mock_print.assert_not_called()

class TestWindSpeedAlert:
    def test_should_not_alert_on_first_update(self) -> None:
        alert = WindSpeedAlert()
        mock_print = MagicMock()
        with patch("builtins.print", mock_print):
            alert.update(WeatherData(25.0, 60.0, 10.0))
            mock_print.assert_not_called()

    def test_should_alert_on_increase(self) -> None:
        alert = WindSpeedAlert()
        mock_print = MagicMock()
        with patch("builtins.print", mock_print):
            alert.update(WeatherData(25.0, 60.0, 10.0))
            alert.update(WeatherData(25.0, 60.0, 15.0))
            mock_print.assert_called_once()
            assert "10.0 km/h -> 15.0 km/h" in mock_print.call_args[0][0]

    def test_should_not_alert_on_decrease(self) -> None:
        alert = WindSpeedAlert()
        mock_print = MagicMock()
        with patch("builtins.print", mock_print):
            alert.update(WeatherData(25.0, 60.0, 10.0))
            alert.update(WeatherData(25.0, 60.0, 5.0))
            mock_print.assert_not_called()

    def test_should_not_alert_on_same_speed(self) -> None:
        alert = WindSpeedAlert()
        mock_print = MagicMock()
        with patch("builtins.print", mock_print):
            alert.update(WeatherData(25.0, 60.0, 10.0))
            alert.update(WeatherData(25.0, 60.0, 10.0))
            mock_print.assert_not_called()
