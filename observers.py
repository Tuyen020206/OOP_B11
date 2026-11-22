"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from alerts import AlertEvent, IAlertObserver


class DashboardObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        print(f"[DASHBOARD] {alert_event.sensor_name}: "
              f"{alert_event.value:.1f}{alert_event.unit} [{alert_event.severity}]")


class EmailAlertObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        # Chỉ mô phỏng console, không gửi email thật.
        print(f"[EMAIL MOCK] {alert_event.severity} tại {alert_event.sensor_name}")


class AuditLogObserver(IAlertObserver):
    def __init__(self):
        self.events: list[AlertEvent] = []

    def update(self, alert_event: AlertEvent) -> None:
        self.events.append(alert_event)
        print(f"[AUDIT] {alert_event.occurred_at.isoformat(timespec='seconds')} "
              f"{alert_event.severity} {alert_event.value:.1f}")
