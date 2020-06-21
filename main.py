"""Kivy app entry point"""
import logging

from kivy.lang import Builder
# from kivy.logger import Logger
from kivy.utils import platform


class LogHandler(logging.Handler):
    """The custom handler to populate RecycleView data"""
    def __init__(self, view, level=logging.NOTSET):
        super().__init__(level=level)
        self.data = view.data

    def emit(self, record):
        self.data.append({
            'text': record.levelname
            + record.message.replace('[', ': ').replace(']', ':')
        })


def start_service(data=None):
    if platform == 'android' and data is None:
        import android
        from jnius import autoclass

        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        Context = autoclass('android.content.Context')

        wifi_info = activity.getSystemService(
            Context.WIFI_SERVICE).getConnectionInfo()
        ipaddr = wifi_info.getIpAddress()

        # debug
        android.start_service(title='Minode')

        # service = autoclass(
        #     '{}.ServiceMinode'.format(activity.getPackageName()))
        # argument = ''
        # service.start(activity, argument)

        return '%d.%d.%d.%d' % (
            (ipaddr & 0xff), (ipaddr >> 8 & 0xff),
            (ipaddr >> 16 & 0xff), (ipaddr >> 24 & 0xff))
    else:
        from minode.app import app
        app.main()


if __name__ == '__main__':
    from kivy.base import runTouchApp

    addr = start_service()

    root = Builder.load_string("""
<LogItem@Label>
    size_hint_x: 1
    text_size: self.width-dp(28), self.height

RecycleView:
    id: debug
    viewclass: 'LogItem'
    RecycleBoxLayout:
        orientation: 'vertical'
        default_size_hint: 1, None
        default_size: 0, dp(28)
        size_hint_y: None
        height: self.minimum_height
""")

    root.data.append({'text': 'Listening %s:8444' % addr})
    # log = logging.getLogger()
    # handler = LogHandler(root, logging.DEBUG)
    # log.addHandler(handler)
    runTouchApp(root)
