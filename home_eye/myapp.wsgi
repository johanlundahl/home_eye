#! /usr/bin/python3.6

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/home_eye/')

from home_eye.myapp import log as app_log
from home_eye.myapp import app as application
from home_eye.myapp import cfg as app_cfg

app_log.init()
application.secret_key = app_cfg.web_server.secret_key




