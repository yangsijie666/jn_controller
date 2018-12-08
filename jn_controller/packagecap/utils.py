import command as cmd
import os
import datetime
import time


class utils(object):

    def __init__(self, time_last, **kwargs):
        self.time_last = time_last
        if not kwargs['filename'].endswith('.pcap'):
            kwargs['filename'] += '.pcap'
        self.dirname = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(
            __file__))) + os.path.sep + '.') + os.path.sep + 'data' + os.path.sep + 'package_capture' + os.path.sep + str(
            datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        kwargs['filename'] = self.dirname + os.path.sep + kwargs['filename']
        self.pkcp = cmd.tcpdump(kwargs)

    def start_capture(self):
        self.pkcp.start()
        if self.time_last > 0:
            time.sleep(float(self.time_last))
            self.pkcp.stop()

    def stop_capture(self):
        self.pkcp.stop()
