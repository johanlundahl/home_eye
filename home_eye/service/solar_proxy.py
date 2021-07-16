from datetime import datetime, timedelta
from enum import Enum
from pytils import http
from home_eye.model.solar import Solar, SolarHistory


class TimeUnit(Enum):

    DAY = 1
    MONTH = 2


class SolarProxy:

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_today(self):
        status, objs = http.get_json(f'{self.base_url}overview?'
                                     f'api_key={self.api_key}')
        return Solar.from_dict(objs) if status == 200 else None

    def get_energy_latest(self, days):
        start_date = (datetime.now()-timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        return self.get_energy_history(start_date, end_date)

    def get_energy_history(self, start_date, end_date, time_unit=TimeUnit.DAY):
        url = (f'{self.base_url}energy?api_key={self.api_key}&'
               f'timeUnit={time_unit.name}&endDate={end_date}&'
               f'startDate={start_date}')
        status, objs = http.get_json(url)
        return SolarHistory.from_dict(objs)

    def __get(self, path):
        url = f'{self.base_url}{path}?api_key={self.api_key}'
        status, objs = http.get_json(url)
