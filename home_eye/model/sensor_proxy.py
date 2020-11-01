from datetime import datetime, timedelta
from home_eye.model.sensor import SensorDecoder, Sensor, SensorHistory, StatusDecoder
from pytils import http
import json

class SensorProxy:

	def __init__(self, base_url):
		self.base_url = base_url

	def get_latest(self, name):
		status, obj = http.get('{}/api/sensors/{}/latest'.format(self.base_url, name))
		return json.loads(obj, object_hook=SensorDecoder.decode)

	def get_history(self, name, days, size):
		from_day = datetime.now() - timedelta(days=days)
		status, trend = http.get('{}/api/sensors/{}/history?from={}&resolution={}'.format(self.base_url, name, from_day.strftime('%Y-%m-%d %H:%M:%S'), size))
		sensors = json.loads(trend, object_hook=SensorDecoder.decode)
		return SensorHistory(list(reversed(sensors)))
	
	def get_day(self, name, day):
		status, trend = http.get('{}/api/v2/sensors/{}/history?date={}&page_size=1000'.format(self.base_url, name, day))
		sensors = json.loads(trend, object_hook=SensorDecoder.decode)
		return SensorHistory(list(reversed(sensors)))
		
	def get_days(self, name, first, last):
		status, trend = http.get('{}/api/v2/sensors/{}/history?date[ge]={}&date[le]={}&page_size=1000'.format(self.base_url, name, first, last))
		sensors = json.loads(trend, object_hook=SensorDecoder.decode)
		return SensorHistory(list(reversed(sensors)))

	def get_status(self):
		status, summary = http.get('{}/api/status'.format(self.base_url))
		return json.loads(summary, object_hook=StatusDecoder.decode)
