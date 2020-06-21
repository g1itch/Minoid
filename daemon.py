"""Android service entry point"""

import pkg_resources

from kivy.logger import Logger
from minode import shared


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
