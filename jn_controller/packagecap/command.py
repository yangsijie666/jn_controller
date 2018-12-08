import os
import re
import signal


class tcpdump(object):

    def __init__(self, args):
        self.interface = args['interface']
        self.protocol = args['protocol']    # protocol can be empty
        self.filename = args['filename']

    def start(self):
        os.system('tcpdump -i %s %s -w "%s" & > /dev/null' % (self.interface, self.protocol, self.filename))

    def stop(self):
        pids = os.popen('ps aux | grep "tcpdump -i %s %s -w" | grep -v grep' % (self.interface, self.protocol))
        pids = pids.read().splitlines()
        for i in pids:
            result = re.search('\d+', i)
            pid = result.group()
            try:
                os.kill(int(pid), signal.SIGTERM)
            except OSError:
                continue
