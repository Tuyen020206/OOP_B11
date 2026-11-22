"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
from abc import ABC, abstractmethod


class ISensor(ABC):
    @abstractmethod
    def read_value(self) -> float:
        """Đọc giá trị theo thang đo chuẩn."""

    @abstractmethod
    def get_unit(self) -> str:
        """Trả về đơn vị đo."""


class LegacySmokeDetector:
    """Chuyển nguyên hành vi lớp cũ trong đề sang Python, không thêm logic."""

    def __init__(self, smoke_level: int):
        self._smoke_level = smoke_level

    def get_smoke_level(self) -> int:
        return self._smoke_level

    def get_description(self) -> str:
        return "Legacy smoke detector"

    def set_smoke_level(self, value: int) -> None:
        self._smoke_level = max(0, min(value, 1000))


class SmokeSensorAdapter(ISensor):
    def __init__(self, legacy: LegacySmokeDetector):
        if legacy is None:
            raise ValueError("Cảm biến cũ không được là None")
        self._legacy = legacy

    def read_value(self) -> float:
        # Chứa tham chiếu đến thiết bị cũ; không sao chép trạng thái.
        return self._legacy.get_smoke_level() / 10.0

    def get_unit(self) -> str:
        return "% smoke"
