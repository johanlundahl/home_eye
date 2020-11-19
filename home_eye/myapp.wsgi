import logging
import sys

logging.basicConfig(stream=sys.stderr)

from home_eye.myapp import logz as app_log
from home_eye.myapp import app as application
from home_eye.myapp import cfg as app_cfg

app_log.init()
application.secret_key = app_cfg.web_server.secret_key




