from datetime import datetime
import json
import unittest
from home_eye.model.sensor import Sensor, ComplexEncoder

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
		

if __name__ == '__main__':
	unittest.main()