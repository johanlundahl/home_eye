import unittest
from home_eye.model.solar import SolarHistory


class SolarTest(unittest.TestCase):

    def test_min_value(self):
        dates = ['2021-02-0{}'.format(x) for x in range(1, 10, 1)]
        values = [1, -2, 7, 4, 1, 6, 9, 8, 9]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh.min.value, -2)

    def test_max_value(self):
        dates = ['2021-02-{:02d}'.format(x) for x in range(1, 10, 1)]
        values = [2, 3, 3, -45, 5, 11, 7, 8, 9]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh.max.value, 11)

    def test_avg_value(self):
        dates = ['2021-02-{:02d}'.format(x) for x in range(10, 20, 1)]
        values = [21, 7, 10, 0, 5, 11, 7, 8, 9, 10]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh.avg.value, 8.8)

    def test_avg_with_none(self):
        dates = ['2021-02-{:02d}'.format(x) for x in range(1, 6, 1)]
        values = [1, 2, 3, None, None]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh.avg.value, 2)

    def test_missing_values(self):
        dates = ['2021-02-{:02d}'.format(x) for x in range(1, 6, 1)]
        values = [None if x % 2 == 0 else x for x in range(1, 6, 1)]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh._values, [1, None, 3, None, 5])
        self.assertEqual(sh.values, [1, 0, 3, 0, 5])

    def test_from_dict(self):
        dct = {
            'energy': {
                'values': [
                    {'date': '2021-02-12 00:00:00', 'value': None},
                    {'date': '2021-02-13', 'value': 55.5}]
            }
        }
        sh = SolarHistory.from_dict(dct)
        self.assertEqual(len(sh.values), 2)
        self.assertTrue(None in sh._values)
        self.assertFalse(None in sh.values)
        self.assertTrue(0 in sh.values)

    def test_sum_value(self):
        dates = ['2021-02-{:02d}'.format(x) for x in range(1, 6, 1)]
        values = [1, 3, 5, 7, 9]
        sh = SolarHistory(dates, values)
        self.assertEqual(sh.sum.value, 25)


if __name__ == '__main__':
    unittest.main()
