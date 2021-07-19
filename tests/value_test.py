import unittest
from home_eye.model.value import Value


class ValueTest(unittest.TestCase):

    def test_to_json(self):
        value = Value(12.0, 'C')
        value_json = value.to_json()
        self.assertIn('value', value_json)
        self.assertIn('display_value', value_json)
        self.assertIn('unit', value_json)

    def test_to_json_unit_prefix(self):
        value = Value(3000, 'b')
        value_json = value.to_json()
        self.assertEqual('kb', value_json['unit'])
        self.assertEqual(3000, value_json['value'])
        self.assertEqual('3', value_json['display_value'])

    def test_kilo_prefix(self):
        value = Value(1500, 'g')
        self.assertEqual(value.value, 1500)
        self.assertEqual(value.display_value, '2')
        self.assertEqual(str(value), '2 kg')


if __name__ == '__main__':
    unittest.main()
