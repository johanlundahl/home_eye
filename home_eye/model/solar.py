from datetime import datetime
import numpy
# from sklearn.linear_model import LinearRegression
from home_eye.model.value import Value


class Solar:

    def __init__(self, power, energy, updated, month=None, year=None):
        self.power = Value(power, 'W')
        self.energy = Value(energy, 'Wh')
        self.updated = Value(updated)
        self.month = Value(month, 'Wh')
        self.year = Value(year, 'Wh')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Solar({self.power}, {self.energy}, {self.updated})'

    @classmethod
    def from_dict(cls, dct):
        updated = datetime.strptime(dct['overview']['lastUpdateTime'],
                                    '%Y-%m-%d %H:%M:%S')
        power = float(dct['overview']['currentPower']['power'])
        energy = float(dct['overview']['lastDayData']['energy'])
        month = float(dct['overview']['lastMonthData']['energy'])
        year = float(dct['overview']['lastYearData']['energy'])
        return Solar(power, energy, updated, month, year)


class SolarHistory:

    def __init__(self, dates, values):
        if len(dates) != len(values):
            raise ValueError('Lists must be of equal length')
        self._dates = dates
        self._values = values

    @property
    def dates(self):
        return self._dates

    @dates.setter
    def dates(self, dates):
        self._dates = dates

    @property
    def values(self):
        values = [x if x is not None else 0 for x in self._values]
        return values

    @property
    def avg(self):
        values = list(filter(lambda x: x is not None, self._values))
        if len(values) == 0:
            return Value(0, 'Wh')
        return Value(sum(values)/len(values), 'Wh')

    @property
    def min(self):
        values = list(filter(lambda x: x is not None, self._values))
        return Value(min(values), 'Wh')

    @property
    def max(self):
        values = list(filter(lambda x: x is not None, self._values))
        if len(values) == 0:
            return Value(0, 'Wh')
        return Value(max(values), 'Wh')

    @property
    def angular_coefficient(self):
        x = numpy.arange(1, len(self._values)+1)
        y = numpy.array(self._values)
        linear_fit = numpy.polyfit(x, y, 1)
        return round(linear_fit[0], 2)

    # linear fit
    # y = mx + q
    # Where “m” is called angular coefficient and “q” intercept.

    @property
    def sum(self):
        values = list(filter(lambda x: x is not None, self._values))
        return Value(sum(values), 'Wh')

    @classmethod
    def from_dict(cls, dct):
        readings = dct['energy']['values']
        dates = [x['date'].split(' ')[0] for x in readings]
        values = [x['value'] for x in readings]
        return SolarHistory(dates, values)
