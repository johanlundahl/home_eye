from pytils import http
from home_eye.model.solar import Solar, SolarHistory
import json
from datetime import datetime, timedelta

class SolarProxy:
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_today(self):
        status, objs = http.get_json('{}overview?api_key={}'.format(self.base_url, self.api_key))
        return Solar.from_dict(objs)

    def get_energy_latest(self, days):
        start_date = (datetime.now()-timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        return self.get_energy_history(start_date, end_date)

    def get_energy_history(self, start_date, end_date):
        url = '{}energy?api_key={}&timeUnit=DAY&endDate={}&startDate={}'.format(self.base_url, self.api_key, end_date, start_date)
        status, objs = http.get_json(url)
        return SolarHistory.from_dict(objs)
