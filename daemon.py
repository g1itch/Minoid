"""Android service entry point"""

import logging
import json
import os
import sys
from logging.handlers import SysLogHandler

import pkg_resources

from kivy.logger import ConsoleHandler, Logger


try:
    sys.argv = json.loads(os.getenv('PYTHON_SERVICE_ARGUMENT'))
except TypeError:  # not on android
    pass

Logger.addHandler(SysLogHandler(('localhost', 1514)))
for i in Logger.handlers:
    if isinstance(i, ConsoleHandler):
        # Kivy formatter is not suitable for connection logs
        i.setFormatter(logging.Formatter())

app = None
for ep in pkg_resources.iter_entry_points('console_scripts'):
    if ep.name == 'minode':
        app = ep.load()
        Logger.info('Service: Found minode console script')
        break
if not app:
    from minode.app import main as app
    Logger.info('Service: Using minode.app module')


if __name__ == '__main__':
    app()
