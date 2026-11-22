"""
/****************/
Mã sinh viên: 202419014
Họ tên: Đào Văn Tuyến
/****************/
"""
import contextlib
import io
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from alerts import AlertEvent, IAlertObserver
from emergency import (Alarm, DoorController, VentilationController,
                       EmergencyMediator, EmergencyBridgeObserver)
from monitor import SensorMonitor
from sensors import LegacySmokeDetector, SmokeSensorAdapter


class Recorder(IAlertObserver):
    def __init__(self):
        self.events = []

    def update(self, alert_event):
        self.events.append(alert_event)


class CampusTests(unittest.TestCase):
    def setUp(self):
        self.legacy = LegacySmokeDetector(0)
        self.sensor = SmokeSensorAdapter(self.legacy)
        self.monitor = SensorMonitor()
        self.recorder = Recorder()
        self.monitor.attach(self.recorder)

    def check(self, raw):
        self.legacy.set_smoke_level(raw)
        with contextlib.redirect_stdout(io.StringIO()):
            self.monitor.check_sensor("Lab", self.sensor)

    def test_adapter_735_and_unit(self):
        self.legacy.set_smoke_level(735)
        self.assertEqual(self.sensor.read_value(), 73.5)
        self.assertEqual(self.sensor.get_unit(), "% smoke")

    def test_adapter_reads_live_state(self):
        self.legacy.set_smoke_level(100)
        self.assertEqual(self.sensor.read_value(), 10)
        self.legacy.set_smoke_level(800)
        self.assertEqual(self.sensor.read_value(), 80)

    def test_adapter_rejects_none(self):
        with self.assertRaises(ValueError):
            SmokeSensorAdapter(None)

    def test_legacy_setter_clamps(self):
        for raw, expected in ((-1, 0), (1001, 100)):
            self.legacy.set_smoke_level(raw)
            self.assertEqual(self.sensor.read_value(), expected)

    def test_boundaries(self):
        for raw, expected in ((0, None), (499, None), (500, "WARNING"),
                              (699, "WARNING"), (700, "CRITICAL"), (1000, "CRITICAL")):
            with self.subTest(raw=raw):
                self.recorder.events.clear()
                self.check(raw)
                self.assertEqual([e.severity for e in self.recorder.events],
                                 [] if expected is None else [expected])

    def test_duplicate_registration(self):
        self.monitor.attach(self.recorder)
        self.check(700)
        self.assertEqual(len(self.recorder.events), 1)

    def test_detach_and_missing_detach(self):
        self.monitor.detach(self.recorder)
        self.monitor.detach(self.recorder)
        self.check(700)
        self.assertEqual(self.recorder.events, [])

    def test_attach_none(self):
        with self.assertRaises(ValueError):
            self.monitor.attach(None)

    def test_snapshot_during_detach(self):
        monitor = self.monitor
        recorder = self.recorder
        class Remover(IAlertObserver):
            def update(self, event):
                monitor.detach(recorder)
        monitor.detach(recorder)
        monitor.attach(Remover())
        monitor.attach(recorder)
        self.check(700)
        self.check(700)
        self.assertEqual(len(recorder.events), 1)

    def test_immutable_event_and_error_isolation(self):
        class BadObserver(IAlertObserver):
            def update(self, event):
                event.value = -1
        monitor = SensorMonitor()
        monitor.attach(BadObserver())
        monitor.attach(self.recorder)
        with contextlib.redirect_stdout(io.StringIO()):
            monitor.check_sensor("Lab", SmokeSensorAdapter(LegacySmokeDetector(735)))
        self.assertEqual(self.recorder.events[0].value, 73.5)
        self.assertEqual(len(monitor.errors), 1)
        with self.assertRaises(FrozenInstanceError):
            self.recorder.events[0].severity = "NORMAL"

    def test_same_event_delivered(self):
        second = Recorder()
        self.monitor.attach(second)
        self.check(700)
        self.assertIs(self.recorder.events[0], second.events[0])

    def test_warning_mediator(self):
        alarm, door, vent = Alarm(), DoorController(), VentilationController()
        self.monitor.attach(EmergencyBridgeObserver(EmergencyMediator(alarm, door, vent)))
        self.check(500)
        self.assertTrue(alarm.is_on)
        self.assertTrue(door.is_locked)
        self.assertTrue(vent.is_running)

    def test_critical_mediator(self):
        alarm, door, vent = Alarm(), DoorController(), VentilationController()
        self.monitor.attach(EmergencyBridgeObserver(EmergencyMediator(alarm, door, vent)))
        self.check(700)
        self.assertTrue(alarm.is_on)
        self.assertFalse(door.is_locked)
        self.assertFalse(vent.is_running)


if __name__ == "__main__":
    unittest.main(verbosity=2)

