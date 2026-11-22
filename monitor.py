"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from datetime import datetime
from alerts import AlertEvent, IAlertObserver
from sensors import ISensor


class SensorMonitor:
    def __init__(self):
        self._observers: list[IAlertObserver] = []
        self.errors: list[str] = []

    def attach(self, observer: IAlertObserver) -> None:
        if observer is None:
            raise ValueError("Observer không được là None")
        if not any(item is observer for item in self._observers):
            self._observers.append(observer)

    def detach(self, observer: IAlertObserver) -> None:
        self._observers = [item for item in self._observers if item is not observer]

    def check_sensor(self, sensor_name: str, sensor: ISensor) -> None:
        value = sensor.read_value()
        severity = "CRITICAL" if value >= 70 else "WARNING" if value >= 50 else None
        if severity is None:
            return
        event = AlertEvent(sensor_name, value, sensor.get_unit(), severity, datetime.now())
        # Snapshot tương đương ToArray(): cho phép gỡ observer khi đang phát tin.
        for observer in tuple(self._observers):
            observer.update(event)
