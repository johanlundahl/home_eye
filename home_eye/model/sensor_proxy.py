from datetime import datetime, timedelta
from home_eye.model.sensor import SensorDecoder, Sensor, SensorHistory
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
		status, trend = http.get('{}/api/sensors/{}?size={}&timestamp[gt]={}'.format(self.base_url, name, size, from_day.strftime('%Y-%m-%d %H:%M:%S')))
		sensors = json.loads(trend, object_hook=SensorDecoder.decode)
		return SensorHistory(list(reversed(sensors)))
		

