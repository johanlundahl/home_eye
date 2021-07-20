from datetime import datetime
import unittest
from home_eye.model.sensor import Sensor, SensorHistory


class SensorHistoryTest(unittest.TestCase):

    def setUp(self):
        s1 = Sensor('one', 12, 55, datetime(year=2021, month=3, day=21))
        s2 = Sensor('two', 14, 50, datetime(year=2021, month=3, day=21))
        s3 = Sensor('three', 10, 51, datetime(year=2021, month=3, day=21))
        self.sensors = [s1, s2, s3]

    def test_temperatures(self):
        history = SensorHistory(self.sensors)
        temps = history.temperatures
        self.assertIn(14, temps)
        self.assertIn(12, temps)
        self.assertIn(10, temps)

    def test_humidities(self):
        history = SensorHistory(self.sensors)
        hum = history.humidities
        self.assertIn(50, hum)
        self.assertIn(51, hum)
        self.assertIn(55, hum)

    def test_timestamps(self):
        history = SensorHistory(self.sensors)
        hum = history.timestamps
        self.assertIn('2021-03-21 0:00', hum)

    def test_humidity_avg(self):
        history = SensorHistory(self.sensors)
        self.assertEqual(52, history.humidity_avg)

    def test_temperature_avg(self):
        history = SensorHistory(self.sensors)
        self.assertEqual(12, history.temperature_avg)


if __name__ == '__main__':
    unittest.main()
