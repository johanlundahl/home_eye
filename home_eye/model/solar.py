class Solar:
    def __init__(self, power, energy, updated):
        self._power = power
        self._energy = energy
        self._updated = updated

    @property
    def updated(self):
        return self._updated
    
    @property
    def power(self):
        return round(self._power)
    
    @property
    def energy(self):
        return round(self._energy/1000)
    
    def __repr__(self):
        return 'Solar({}, {}, {})'.format(self.power, self.energy, self.updated)

    def __str__(self):
        return 'Solar({}, {}, {})'.format(self.power, self.energy, self.updated)        

    @classmethod
    def from_dict(cls, dct):
        updated = dct['overview']['lastUpdateTime']
        power = float(dct['overview']['currentPower']['power'])
        energy = float(dct['overview']['lastDayData']['energy'])
        return Solar(power, energy, updated)


class SolarHistory:
    def __init__(self, dates, values):
        self._dates = dates
        self._values = values

    @property
    def dates(self):
        return self._dates
    
    @property
    def values(self):
        return self._values

    @classmethod
    def from_dict(cls, dct):
        readings = dct['energy']['values']
        dates = [x['date'].split(' ')[0] for x in readings]
        values = [x['value'] for x in readings]
        return SolarHistory(dates, values)
