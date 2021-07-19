from datetime import datetime
import unittest
from home_eye.model.sensor import Sensor


class SensorTest(unittest.TestCase):

    def test_parameters_in_to_json(self):
        sensor = Sensor('indoor', 12.0, 55.5, datetime.now())
        sensor_json = sensor.to_json()
        self.assertIn('name', sensor_json)
        self.assertIn('temperature', sensor_json)
        self.assertIn('humidity', sensor_json)
        self.assertIn('updated', sensor_json)
        self.assertIn('age', sensor_json)

    def test_to_json(self):
        sensor = Sensor('indoor', 12.0, 55.5, datetime.now())
        sensor_json = sensor.to_json()
        self.assertEqual('indoor', sensor_json['name'])
        self.assertIn('value', sensor_json['temperature'])
        self.assertIn('display_value', sensor_json['temperature'])

    def test_create(self):
        sensor = Sensor('test', 20, 30, datetime(year=2021, month=3, day=21))
        self.assertEqual(sensor.name, 'test')
        self.assertEqual(sensor.temperature.value, 20)
        self.assertEqual(sensor.humidity.value, 30)
        self.assertEqual(sensor.updated.value,
                         datetime(year=2021, month=3, day=21))


if __name__ == '__main__':
    unittest.main()
