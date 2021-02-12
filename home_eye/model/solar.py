from home_eye.model.value import Value
from datetime import datetime

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
        return self._values

    @classmethod
    def from_dict(cls, dct):
        readings = dct['energy']['values']
        dates = [x['date'].split(' ')[0] for x in readings]
        values = [x['value'] if x['value'] is not None else 0 for x in readings]
        return SolarHistory(dates, values)
