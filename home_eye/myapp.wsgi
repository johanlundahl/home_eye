#! /usr/bin/python3.6

import logging
import sys
from home_eye.myapp import logger as logr
from home_eye.myapp import app as application
from home_eye.config import config as config

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, config.app_root_path)
logr.init()
application.secret_key = config.app_secret_key




