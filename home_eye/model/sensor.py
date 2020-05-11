from home_eye.model.value import Value
from datetime import datetime, timedelta

class Sensor:   
    def __init__(self, name, temperature, humidity, updated):
        self._name = name
        self._temperature = Value(temperature, '°C')
        self._humidity = Value(humidity, '%')
        self._updated = Value(updated)
        self._now = datetime.now()

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

    @property
    def age(self):
        delta = self._now - self._updated.value
        return delta.seconds // 3600

    def __repr__(self):
        return 'Sensor({}, {}, {}, {})'.format(self.name, self.temperature, self.humidity, self.updated)
    
    def __str__(self):
        return 'Sensor({}, {}, {}, {})'.format(self.name, self.temperature, self.humidity, self.updated)
        
class SensorDecoder:
    @classmethod
    def decode(cls, dct):
        if 'humidity' in dct and 'temperature' in dct: 
            return Sensor(dct['name'], dct['temperature'], dct['humidity'], datetime.strptime(dct['timestamp'], '%Y-%m-%d %H:%M:%S'))


class SensorHistory:
    def __init__(self, sensors):
        self._sensors = sensors

    @property
    def timestamps(self):
        return [x.updated.display_value for x in self._sensors]
    
    @property
    def humidities(self):
        return [x.humidity.value for x in self._sensors]
    
    @property
    def temperatures(self):
        return [x.temperature.value for x in self._sensors]
    
    @property
    def humidity_avg(self):
        h = self.humidities
        return round(sum(h)/len(h), 1) if len(h) > 0 else 0

    @property
    def temperature_avg(self):
        t = self.temperatures
        return round(sum(t)/len(t), 1) if len(t) > 0 else 0

    def __repr__(self):
        return 'SensorHistory({}, {}, {})'.format(len(self._sensors), self.humidity_avg, self.temperature_avg)

    def __str__(self):
        return 'SensorHistory({}, {}, {})'.format(len(self._sensors), self.humidity_avg, self.temperature_avg)
