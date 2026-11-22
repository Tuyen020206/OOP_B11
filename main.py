"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from emergency import (Alarm, DoorController, VentilationController,
                       EmergencyMediator, EmergencyBridgeObserver)
from monitor import SensorMonitor
from observers import DashboardObserver, EmailAlertObserver, AuditLogObserver
from sensors import LegacySmokeDetector, SmokeSensorAdapter


def main() -> None:
    legacy = LegacySmokeDetector(0)
    sensor = SmokeSensorAdapter(legacy)
    monitor = SensorMonitor()
    email = EmailAlertObserver()
    mediator = EmergencyMediator(Alarm(), DoorController(), VentilationController())
    for observer in (DashboardObserver(), email, AuditLogObserver(),
                     EmergencyBridgeObserver(mediator)):
        monitor.attach(observer)
    print("CAMPUS SAFETY HUB - Đào Văn Tuyến - 202419014")
    for raw in (300, 500, 699, 700, 735):
        print(f"\n--- Mức khói cũ {raw} -> {raw / 10:.1f}% ---")
        legacy.set_smoke_level(raw)
        monitor.check_sensor("Phòng máy A", sensor)
    monitor.detach(email)
    print("\n--- Hủy email, kiểm tra lại 80% ---")
    legacy.set_smoke_level(800)
    monitor.check_sensor("Phòng máy A", sensor)


if __name__ == "__main__":
    main()
