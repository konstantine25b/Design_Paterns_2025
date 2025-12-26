import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import random

from weather_system.observers.alerts import (
    HumidityAlert,
    TemperatureAlert,
    WindSpeedAlert,
)
from weather_system.observers.display import WeatherDisplay
from weather_system.subject.station import WeatherStation


def run_simulation() -> None:
    station = WeatherStation()
    display = WeatherDisplay()

    station.register_observer(display)

    temp_alert: TemperatureAlert | None = None
    wind_alert: WindSpeedAlert | None = None
    humid_alert: HumidityAlert | None = None

    fixed_data: list[tuple[float, float, float]] = [
        (28.0, 70.0, 12.0),
        (30.0, 72.0, 15.0),
        (32.0, 74.0, 18.0),
        (36.0, 80.0, 22.0),
        (40.0, 65.0, 25.0),
        (45.0, 90.0, 30.0),
        (43.0, 92.0, 32.0),
        (40.0, 85.0, 30.0),
        (38.0, 82.0, 28.0),
        (36.0, 80.0, 25.0),
    ]

    for week in range(1, 21):
        print(f"\nWeek {week}:")

        if week == 4:
            print("Adding: TemperatureAlert")
            temp_alert = TemperatureAlert()
            station.register_observer(temp_alert)
        elif week == 5:
            print("Adding: WindSpeedAlert")
            wind_alert = WindSpeedAlert()
            station.register_observer(wind_alert)
        elif week == 6:
            print("Adding: HumidityAlert")
            humid_alert = HumidityAlert()
            station.register_observer(humid_alert)

        if week <= len(fixed_data):
            t, h, w = fixed_data[week - 1]
        else:
            t = round(random.uniform(15, 45), 1)
            h = round(random.uniform(40, 100), 1)
            w = round(random.uniform(0, 50), 1)

        station.set_measurements(t, h, w)

        if week == 8 and humid_alert:
            print("Removing: HumidityAlert")
            station.remove_observer(humid_alert)
            humid_alert = None

        print("---")


if __name__ == "__main__":
    run_simulation()
