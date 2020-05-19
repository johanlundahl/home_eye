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

class Status:
    def __init__(self, count, size, oldest, newest):
        self._count = Value(count)
        self._size = Value(size, 'b')
        self._oldest = Value(oldest)
        self._newest = Value(newest)

    @property
    def count(self):
        return self._count
    
    @property
    def size(self):
        return self._size
    
    @property
    def oldest(self):
        return self._oldest
    
    @property
    def newest(self):
        return self._newest

    def __repr__(self):
        return 'Status({}, {}, {}, {})'.format(self._count, self._size, self._oldest, self._newest)

    def __str__(self):
        return 'Status({}, {}, {}, {})'.format(self._count, self._size, self._oldest, self._newest)        

class StatusDecoder:
    @classmethod
    def decode(cls, dct):
        if 'newest' in dct and 'oldest' in dct:
            oldest = datetime.strptime(dct['oldest'], '%Y-%m-%d %H:%M:%S')
            newest = datetime.strptime(dct['newest'], '%Y-%m-%d %H:%M:%S')            
            return Status(dct['count'], dct['size'], oldest, newest)

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
