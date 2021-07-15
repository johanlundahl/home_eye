import unittest
from datetime import datetime
from home_eye.model.solar import Solar


class SolarTest(unittest.TestCase):

	def test_create(self):
		solar = Solar(10, 20, datetime(year=2021, month=3, day=21))
		self.assertTrue(isinstance(solar, Solar))
		self.assertEqual(solar.power.value, 10)

		


if __name__ == '__main__':
	unittest.main()