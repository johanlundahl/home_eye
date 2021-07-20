import unittest
from home_eye.model.sensor import SensorDecoder, StatusDecoder
from home_eye.model.sensor import Status, Sensor


class SensorDecoders(unittest.TestCase):

    def test_statusdecoder(self):
        dct = {
            'newest': '2021-07-20 18:35:05',
            'oldest': '2021-07-01 12:05:05',
            'size': 100,
            'count': 10,
            'ignored': 'a fake string'
        }
        status = StatusDecoder.decode(dct)
        self.assertTrue(isinstance(status, Status))

    def test_sensordecoder(self):
        dct = {
            'humidity': 60,
            'name': 'sensor',
            'temperature': 21,
            'timestamp': '2021-07-20 18:35:05',
            'ignored': 'a fake string'
        }
        sensor = SensorDecoder.decode(dct)
        self.assertTrue(isinstance(sensor, Sensor))

    def test_sensordecoder_not_decoding(self):
        dct = {
            'humidity': 60,
            'name': 'sensor',
            'temperature': 21,
            'min': 1,
            'max': 10,
            'timestamp': '2021-07-20 18:35:05',
            'ignored': 'a fake string'
        }
        sensor = SensorDecoder.decode(dct)
        self.assertTrue(isinstance(sensor, dict))


if __name__ == '__main__':
    unittest.main()
