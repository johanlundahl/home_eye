from datetime import datetime
from flask.json import JSONEncoder
from home_eye.model.value import Value


class Sensor:
    def __init__(self, name, temperature, humidity, updated):
        self.name = name
        self.temperature = Value(temperature, '°C')
        self.humidity = Value(humidity, '%')
        self.updated = Value(updated)
        self._now = datetime.now()

    @property
    def age(self):
        delta = self._now - self.updated.value
        return delta.total_seconds() // 3600

    def to_json(self):
        result = {'name': self.name,
                  'temperature': self.temperature.to_json(),
                  'humidity': self.humidity.to_json(),
                  'updated': self.updated.to_json(),
                  'age': self.age}
        return result

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'Sensor({self.name}, {self.temperature}, '
                f'{self.humidity}, {self.updated})')


class SensorDecoder:
    @classmethod
    def decode(cls, dct):
        if 'min' in dct and 'max' in dct:
            return dct
        if 'humidity' in dct and 'temperature' in dct:
            time = datetime.strptime(dct['timestamp'], '%Y-%m-%d %H:%M:%S')
            return Sensor(dct['name'], dct['temperature'],
                          dct['humidity'], time)


class ComplexEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        return JSONEncoder.default(self, o)


class Status:
    def __init__(self, count, size, oldest, newest):
        self.count = Value(count)
        self.size = Value(size, 'b')
        self.oldest = Value(oldest)
        self.newest = Value(newest)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'Status({self.count}, {self.size}, '
                f'{self.oldest}, {self.newest})')


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
        return str(self)

    def __str__(self):
        return (f'SensorHistory({len(self._sensors)}, {self.humidity_avg}, '
                f'{self.temperature_avg})')
