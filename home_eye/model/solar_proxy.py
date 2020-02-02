from pytils import http
from home_eye.model.solar import SolarDecoder, Solar
import json

class SolarProxy:
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_today(self):
        status, objs = http.get_json('{}overview?api_key={}'.format(self.base_url, self.api_key))
        return Solar.from_dict(objs)

