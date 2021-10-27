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

    def test_mega_prefix(self):
        measure = Measure(3000000, 'b')
        self.assertEqual(measure.value, 3000000)
        self.assertEqual(measure.display, '3 Mb')

    def test_giga_prefix(self):
        measure = Measure(5500000000, 'b')
        self.assertEqual(measure.value, 5500000000)
        self.assertEqual(measure.display, '5.5 Gb')


if __name__ == '__main__':
    unittest.main()
