from twisted.internet.protocol import DatagramProtocol


class SyslogListener(DatagramProtocol):
    """Draw syslog messages on the *widget*"""
    color_code = {
        5: '2dcc70',
        4: 'f39c11',
        3: 'd82619'
    }

    def __init__(self, widget, config):
        self.config = config
        self.widget = widget

    def datagramReceived(self, msg, addr):
        msg = self._parse_datagram(msg)
        if msg:
            self.widget.text += '\n' + msg

    def _parse_datagram(self, msg):
        msg = msg.decode('utf-8').strip()
        if msg[0] != '<':
            return msg

        close = msg.find('>', 1, 5)
        if close > 0:
            pri, msg = int(msg[1:close]), msg[close+1:]
            severity = pri & 7
            if 'failed. Reason:' in msg:
                if not self.config.getboolean('debug'):
                    return ''
                severity = 7
                # facility = (pri & 248) >> 3
            try:
                color = self.color_code[severity]
            except KeyError:
                pass
            else:
                msg = '[color=#{}]{}[/color]'.format(color, msg)

        return msg
