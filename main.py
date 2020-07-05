"""Kivy app entry point"""
import json
import sys

from kivy.app import App
from kivy.logger import Logger
from kivy.support import install_twisted_reactor
from kivy.utils import platform

install_twisted_reactor()  # noqa:E402 ! before twisted

from twisted.internet import reactor

from log import SyslogListener


class MinoidApp(App):
    use_kivy_settings = False

    def __init__(self):
        self.app_config_changed = False
        super().__init__()

    def build_config(self, config):
        config.setdefaults('minode', {
            'debug': False,
            'connection-limit': 9,
            'listening-host': '0.0.0.0',
            'listening-port': '8444'
        })

    def build_settings(self, settings):
        settings.add_json_panel(self.name, self.config, data="""
[{
    "type": "numeric",
    "title": "Connection Limit",
    "section": "minode",
    "key": "connection-limit"
},
{
    "type": "numeric",
    "title": "Listen on Port",
    "section": "minode",
    "key": "listening-port"
},
{
    "type": "bool",
    "title": "Debug Logging",
    "section": "minode",
    "key": "debug"
}]
""")

    def close_settings(self, *args):
        if self.app_config_changed:
            self.app_config_changed = False
            start_service(*self.build_app_args())
        return super().close_settings(*args)

    def build_app_args(self):
        appconf = self.config['minode']
        data = [
            'minode', '--connection-limit', appconf['connection-limit']]
        if appconf.getboolean('debug'):
            data.append('--debug')
        # host = appconf['listening-host']
        # if host != '0.0.0.0':
        #     data += ['--host', host]
        port = appconf.getint('listening-port')
        if port != 8444:
            return data + ['-p', str(port)], 'Connect to {}:%s' % port

        return data,

    def on_config_change(self, config, section, *args):
        if config is self.config and section == 'minode':
            self.app_config_changed = True

    def build(self):
        super().build()
        start_service(*self.build_app_args())
        reactor.listenUDP(
            1514, SyslogListener(self.root.debug, self.config['minode']))

        return self.root


def start_service(data=[], msg=None):
    if platform == 'android':
        import android
        from jnius import autoclass

        android.stop_service()

        Context = autoclass('android.content.Context')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity

        # service = autoclass(
        #     '{}.ServiceMinode'.format(activity.getPackageName()))
        # service.stop(activity)

        wifi_info = activity.getSystemService(
            Context.WIFI_SERVICE).getConnectionInfo()
        ipaddr = wifi_info.getIpAddress()
        ipaddr = '%d.%d.%d.%d' % (
            (ipaddr & 0xff), (ipaddr >> 8 & 0xff),
            (ipaddr >> 16 & 0xff), (ipaddr >> 24 & 0xff))

        Logger.info('APP: Starting the service...')

        if not msg:
            msg = 'Connect to {}:8444'
        msg = msg.format(ipaddr)

        # debug
        android.start_service('Minoid', msg, arg=json.dumps(data))

        # service.start(activity, json.dumps(data))
    else:
        sys.argv = data

        from daemon import app
        app()


if __name__ == '__main__':
    MinoidApp().run()
