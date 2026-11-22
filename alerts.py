"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AlertEvent:
    sensor_name: str
    value: float
    unit: str
    severity: str
    occurred_at: datetime


class IAlertObserver(ABC):
    @abstractmethod
    def update(self, alert_event: AlertEvent) -> None:
        """Nhận một cảnh báo bất biến."""
