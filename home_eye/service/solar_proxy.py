from datetime import datetime, timedelta
from enum import Enum
import json
from pytils import http
import requests
from home_eye.model.solar import Solar, SolarHistory


class TimeUnit(Enum):

    DAY = 1
    MONTH = 2


class SolarProxy:
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_today(self):
        status, objs = http.get_json('{}overview?api_key={}'.format(self.base_url, self.api_key))
        return Solar.from_dict(objs) if status == 200 else None

    def get_energy_latest(self, days):
        start_date = (datetime.now()-timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        return self.get_energy_history(start_date, end_date)

    def get_energy_history(self, start_date, end_date, time_unit=TimeUnit.DAY):
        url = '{}energy?api_key={}&timeUnit={}&endDate={}&startDate={}'.format(self.base_url, self.api_key, time_unit.name, end_date, start_date)
        status, objs = http.get_json(url)
        return SolarHistory.from_dict(objs)