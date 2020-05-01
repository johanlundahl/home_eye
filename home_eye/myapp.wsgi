#! /usr/bin/python3.6

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/home_eye/')

from home_eye.myapp import logger as logr
logr.init()

from home_eye.myapp import app as application
application.secret_key = 'anything you wish'




