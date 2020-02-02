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

class SolarDecoder():
    @classmethod
    def decode(cls, dct):
        if 'lastUpdateTime' in dct:
            print(dct)
            updated = dct['overview']['lastUpdateTime']
            power = float(dct['overview']['currentPower']['power'])
            energy = float(dct['overview']['lastDayData']['energy'])
            return Solar(power, energy, updated)