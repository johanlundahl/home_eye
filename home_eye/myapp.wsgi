#! /usr/bin/python3.6

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/home_eye/')

from home_eye.myapp import logger as logr
from home_eye.myapp import app as application
from home_eye import config 

logr.init()
application.secret_key = config.app_secret_key




