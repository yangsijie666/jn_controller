import json
import os


class API(object):

    def __init__(self):
        self.abs_cwd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
        self.mainpath = self.abs_cwd + 'main.py'
        self.logfile = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'log' + os.path.sep + 'tfn2k.log'
        cfg_json_name = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'config.json'
        with open(cfg_json_name, 'r') as f:
            all_cfg_json_dict = json.load(f)
        self.tfn2k_cfg = all_cfg_json_dict['tfn2k']

    def get_tfn2k_status(self):
        status = self.tfn2k_cfg['status']
        if status == 'on':
            return True
        elif status == 'off':
            return False
        else:
            print('json file: tfn2k status should be \'on\' or \'off\'!')
            exit(1)

    # functions that can be called
    def start_tfn2k(self):
        if self.get_tfn2k_status():
            args = self.tfn2k_cfg['args']
            time_last = args['time_last']
            attack_interval = args['attack_interval']
            wait_interval = args['wait_interval']
            phy_interface = args['phy_interface']['name']
            bandwidth = args['phy_interface']['bandwidth']
            packet_size = args['packet_size']
            flood_type = args['flood_type']
            victims = args['victims']
            victims = '@'.join(victims)
            cmd = 'nohup python %s start %s %s %s %s %s %s %s %s > %s 2>&1 &' % (
            self.mainpath, time_last, attack_interval, wait_interval, phy_interface, bandwidth, packet_size, flood_type,
            victims, self.logfile)
            os.system(cmd)

    def stop_tfn2k(self):
        if self.get_tfn2k_status():
            cmd = 'nohup python %s stop > %s 2>&1 &' % (self.mainpath, self.logfile)
            os.system(cmd)
