
class Sensor:   
    def __init__(self, name, temperature, humidity, updated):
        self._name = name
        self._temperature = temperature
        self._humidity = humidity
        self._updated = updated

    @property
    def name(self):
        return self._name
    
    @property
    def temperature(self):
        return self._temperature
    
    @property
    def humidity(self):
        return self._humidity
    
    @property
    def updated(self):
        return self._updated

    def __repr__(self):
        return 'Sensor({}, {}, {}, {})'.format(self.name, self.temperature, self.humidity, self.updated)
    
    def __str__(self):
        return 'Sensor({}, {}, {}, {})'.format(self.name, self.temperature, self.humidity, self.updated)
        

class SensorDecoder:
    @classmethod
    def decode(cls, dct):
        if 'humidity' in dct and 'temperature' in dct: 
            return Sensor(dct['name'], dct['temperature'], dct['humidity'], dct['timestamp'])


class SensorHistory:
    def __init__(self, sensors):
        self._sensors = sensors

    @property
    def timestamps(self):
        return [x.updated for x in self._sensors]
    
    @property
    def humidities(self):
        return [x.humidity for x in self._sensors]
    
    @property
    def temperatures(self):
        return [x.temperature for x in self._sensors]
    
    @property
    def humidity_avg(self):
        h = self.humidities
        return round(sum(h)/len(h), 1)

    @property
    def temperature_avg(self):
        t = self.temperatures
        return round(sum(t)/len(t), 1)

    def __repr__(self):
        return 'SensorHistory({}, {}, {})'.format(len(self._sensors), self.humidity_avg, self.temperature_avg)

    def __str__(self):
        return 'SensorHistory({}, {}, {})'.format(len(self._sensors), self.humidity_avg, self.temperature_avg)
