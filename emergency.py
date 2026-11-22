"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from abc import ABC, abstractmethod
from alerts import AlertEvent, IAlertObserver


class Alarm:
    def __init__(self):
        self.is_on = False

    def activate(self) -> None:
        self.is_on = True


class DoorController:
    def __init__(self):
        self.is_locked = True

    def unlock(self) -> None:
        self.is_locked = False


class VentilationController:
    def __init__(self):
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False


class IEmergencyMediator(ABC):
    @abstractmethod
    def handle_alert(self, event: AlertEvent) -> None:
        """Điều phối thiết bị theo sự kiện."""


class EmergencyMediator(IEmergencyMediator):
    def __init__(self, alarm: Alarm, door: DoorController,
                 ventilation: VentilationController):
        self._alarm = alarm
        self._door = door
        self._ventilation = ventilation

    def handle_alert(self, event: AlertEvent) -> None:
        # Quy tắc mô phỏng tự chọn vì PDF chưa chỉ định chi tiết Mediator.
        if event.severity not in ("WARNING", "CRITICAL"):
            return
        self._alarm.activate()
        if event.severity == "CRITICAL":
            self._door.unlock()
            self._ventilation.stop()
        print(f"[MEDIATOR] alarm={self._alarm.is_on} "
              f"door_locked={self._door.is_locked} "
              f"ventilation={self._ventilation.is_running}")


class EmergencyBridgeObserver(IAlertObserver):
    def __init__(self, mediator: IEmergencyMediator):
        self._mediator = mediator

    def update(self, alert_event: AlertEvent) -> None:
        self._mediator.handle_alert(alert_event)
