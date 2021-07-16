from datetime import datetime
import locale
from quantiphy import Quantity

locale.setlocale(locale.LC_ALL, '')


class Value:

    def __init__(self, value, unit=''):
        self._value = value
        self._unit = unit

    @property
    def value(self):
        return self._value

    @property
    def display_value(self):
        if isinstance(self._value, (int, float)):
            return '{0:n}'.format(self.__format_number(self._value))
        if isinstance(self._value, str):
            return str(self._value.capitalize())
        if isinstance(self._value, datetime):
            return self._value.strftime('%Y-%m-%d %-H:%M')
        return str(self._value)

    @property
    def unit(self):
        if self.__isnumber() and self.__need_unit_prefix():
            factor, prefix = self.__get_prefix()
            return prefix + self._unit
        return self._unit

    def to_json(self):
        return {'value': self.value,
                'display_value': self.display_value,
                'unit': self.unit}

    def __get_prefix(self):
        if self._value >= 10**6:
            return (10**6, 'M')
        elif self._value >= 10**3:
            return (10**3, 'k')
        else:
            return (1, '')

    def __format_number(self, value):
        if self.__isnumber() and self.__need_unit_prefix():
            factor, prefix = self.__get_prefix()
            value = value / factor
        value = self.__round(value)
        return value

    def __need_unit_prefix(self):
        return self._value >= 1000 and self._unit != ''

    def __isnumber(self):
        return isinstance(self._value, (int, float))

    def __round(self, value):
        return int(round(value, 0))

    def __str__(self):
        return '{} {}'.format(self.display_value, self.unit)


class Measure:

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    @property
    def display(self):
        return str(self)

    def __str__(self):
        q = Quantity(self.value, self.unit)
        return str(q)


# class Magnitude:

    # def __init__(evaluate, transform)
