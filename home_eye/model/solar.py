from datetime import datetime
from home_eye.model.value import Value


class Solar:
    def __init__(self, power, energy, updated, month=None, year=None):
        self._power = Value(power, 'W')
        self._energy = Value(energy, 'Wh')
        self._updated = Value(updated)
        self._month = Value(month, 'Wh')
        self._year = Value(year, 'Wh')

    @property
    def updated(self):
        return self._updated
    
    @property
    def power(self):
        return self._power
    
    @property
    def month(self):
        return self._month
    
    @property
    def year(self):
        return self._year
    
    @property
    def energy(self):
        return self._energy
    
    def __repr__(self):
        return 'Solar({}, {}, {})'.format(self.power, self.energy, self.updated)

    def __str__(self):
        return 'Solar({}, {}, {})'.format(self.power, self.energy, self.updated)        

    @classmethod
    def from_dict(cls, dct):
        updated = datetime.strptime(dct['overview']['lastUpdateTime'], '%Y-%m-%d %H:%M:%S')
        power = float(dct['overview']['currentPower']['power'])
        energy = float(dct['overview']['lastDayData']['energy'])
        month = float(dct['overview']['lastMonthData']['energy'])
        year = float(dct['overview']['lastYearData']['energy'])
        return Solar(power, energy, updated, month,)


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
    def sum(self):
        values = list(filter(lambda x: x is not None, self._values))
        return Value(sum(values), 'Wh')

    @classmethod
    def from_dict(cls, dct):
        readings = dct['energy']['values']
        dates = [x['date'].split(' ')[0] for x in readings]
        values = [x['value'] for x in readings]
        return SolarHistory(dates, values)
