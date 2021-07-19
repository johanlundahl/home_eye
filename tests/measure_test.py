import unittest
from home_eye.model.value import Measure


class MeasureTest(unittest.TestCase):

    def test_create(self):
        measure = Measure(12.0, 'C')
        self.assertEqual(measure.value, 12)

    def test_kilo_prefix(self):
        measure = Measure(1000, 'g')
        self.assertEqual(measure.value, 1000)
        self.assertEqual(measure.display, '1 kg')


if __name__ == '__main__':
    unittest.main()
