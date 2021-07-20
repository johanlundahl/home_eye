import unittest
from unittest.mock import patch
from home_eye.service.solar_proxy import SolarProxy
from home_eye.model.solar import Solar, SolarHistory


class SolarProxyTest(unittest.TestCase):

    @patch('home_eye.service.solar_proxy.http.get_json')
    def test_get_today_http_called(self, mock):
        json = {'overview': {
            'lastUpdateTime': '2021-03-07 19:36:35',
            'lastYearData': {'energy': 10.0},
            'lastMonthData': {'energy': 20.0},
            'lastDayData': {'energy': 30.0},
            'currentPower': {'power': 1.0}}}
        mock.return_value = 200, json

        proxy = SolarProxy('http://a-valid-url', 'valid-key')
        result = proxy.get_today()

        mock.assert_called_once()
        self.assertTrue(isinstance(result, Solar))

    @patch('home_eye.service.solar_proxy.http.get_json')
    def test_get_today_with_bad_api_key(self, mock):
        mock.return_value = 403, {'String': 'Invalid token'}
        proxy = SolarProxy('https://a-valid-url/', 'fake-key')
        solar = proxy.get_today()

        self.assertEqual(solar, None)

    @patch('home_eye.service.solar_proxy.http.get_json')
    def test_get_today_with_bad_url(self, mock):
        mock.return_value = 400, ''
        proxy = SolarProxy('https://an-invalid-url', 'valid-key')
        solar = proxy.get_today()
        self.assertEqual(solar, None)

    @patch('home_eye.service.solar_proxy.http.get_json')
    def test_energy_latest(self, mock):
        dct = {
            'energy': {
                'values': [
                    {'date': '2021-02-12 00:00:00', 'value': None},
                    {'date': '2021-02-13', 'value': 55.5}]
            }
        }
        mock.return_value = 400, dct
        proxy = SolarProxy('http://blabla', 'key')
        history = proxy.get_energy_latest(1)
        self.assertTrue(isinstance(history, SolarHistory))


if __name__ == '__main__':
    unittest.main()
