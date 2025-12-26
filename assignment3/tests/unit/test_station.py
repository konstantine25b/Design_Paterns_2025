from unittest.mock import MagicMock
from weather_system.subject.station import WeatherStation
from weather_system.core.models import WeatherData
from weather_system.core.interfaces import Observer

class MockObserver(Observer):
    def __init__(self) -> None:
        super().__init__()
        self.update_called = False
        self.last_data: WeatherData | None = None

    def update(self, data: WeatherData) -> None:
        self.update_called = True
        self.last_data = data

class TestWeatherStation:
    def test_should_register_single_observer(self) -> None:
        station = WeatherStation()
        observer = MockObserver()
        station.register_observer(observer)
        
        assert station._head == observer
        assert observer.next_observer is None

    def test_should_chain_multiple_observers(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        obs3 = MockObserver()
        
        station.register_observer(obs1)
        station.register_observer(obs2)
        station.register_observer(obs3)
        
        assert station._head == obs1
        assert obs1.next_observer == obs2
        assert obs2.next_observer == obs3
        assert obs3.next_observer is None

    def test_should_not_register_duplicate_observer(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        
        station.register_observer(obs1)
        station.register_observer(obs1)
        
        assert station._head == obs1
        assert obs1.next_observer is None

    def test_should_remove_head_observer(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        
        station.register_observer(obs1)
        station.register_observer(obs2)
        
        station.remove_observer(obs1)
        
        assert station._head == obs2
        assert obs1.next_observer is None  # Should be unlinked

    def test_should_remove_middle_observer(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        obs3 = MockObserver()
        
        station.register_observer(obs1)
        station.register_observer(obs2)
        station.register_observer(obs3)
        
        station.remove_observer(obs2)
        
        assert station._head == obs1
        assert obs1.next_observer == obs3
        assert obs2.next_observer is None  # Should be unlinked

    def test_should_remove_tail_observer(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        
        station.register_observer(obs1)
        station.register_observer(obs2)
        
        station.remove_observer(obs2)
        
        assert station._head == obs1
        assert obs1.next_observer is None
        assert obs2.next_observer is None

    def test_should_handle_remove_non_existent_observer(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        
        station.register_observer(obs1)
        station.remove_observer(obs2)  # Should not crash
        
        assert station._head == obs1

    def test_should_notify_all_observers_in_chain(self) -> None:
        station = WeatherStation()
        obs1 = MockObserver()
        obs2 = MockObserver()
        station.register_observer(obs1)
        station.register_observer(obs2)
        
        station.set_measurements(20.0, 50.0, 10.0)
        
        assert obs1.update_called
        assert obs2.update_called
        assert obs1.last_data == WeatherData(20.0, 50.0, 10.0)
        assert obs2.last_data == WeatherData(20.0, 50.0, 10.0)

    def test_should_notify_new_observer_immediately_if_data_exists(self) -> None:
        station = WeatherStation()
        station.set_measurements(20.0, 50.0, 10.0)
        
        obs1 = MockObserver()
        station.register_observer(obs1)
        
        assert obs1.update_called
        assert obs1.last_data == WeatherData(20.0, 50.0, 10.0)

