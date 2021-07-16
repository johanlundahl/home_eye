from home_eye.model.sensor import SensorDecoder, SensorHistory, StatusDecoder
from pytils import http
import json


class SensorProxy:

    def __init__(self, base_url):
        self.base_url = base_url

    def get_latest(self, name):
        status, obj = http.get(f'{self.base_url}/api/v2/sensors/{name}/latest')
        return json.loads(obj, object_hook=SensorDecoder.decode)

    def get_min_max(self, name, date):
        status, obj = http.get(f'{self.base_url}/api/v2/sensors/{name}/'
                               f'min-max?date={date}')
        return json.loads(obj, object_hook=SensorDecoder.decode)

    def get_day(self, name, day):
        status, trend = http.get(f'{self.base_url}/api/v2/sensors/{name}/'
                                 f'readings?date={day}&page_size=1000')
        sensors = json.loads(trend, object_hook=SensorDecoder.decode)
        return SensorHistory(list(reversed(sensors)))

    def get_days(self, name, first, last):
        status, trend = http.get(f'{self.base_url}/api/v2/sensors/{name}/'
                                 f'readings?date[ge]={first}&date[le]={last}&'
                                 f'page_size=100000')
        sensors = json.loads(trend, object_hook=SensorDecoder.decode)
        return SensorHistory(list(reversed(sensors)))

    def get_status(self):
        status, summary = http.get('{}/api/v2/status'.format(self.base_url))
        return json.loads(summary, object_hook=StatusDecoder.decode)
