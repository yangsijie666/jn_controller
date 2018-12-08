import json
import os


class API(object):

    def __init__(self):
        self.abs_cwd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
        self.mainpath = self.abs_cwd + 'main.py'
        self.logfile = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'log' + os.path.sep + 'packagecap.log'
        cfg_json_name = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'config.json'
        with open(cfg_json_name, 'r') as f:
            all_cfg_json_dict = json.load(f)
        self.packagecap_cfg = all_cfg_json_dict['packagecap']

    def get_packagecap_status(self):
        status = self.packagecap_cfg['status']
        if status == 'on':
            return True
        elif status == 'off':
            return False
        else:
            print('json file: packagecap status should be \'on\' or \'off\'!')
            exit(1)

    # functions that can be called
    def start_packagecap(self):
        if self.get_packagecap_status():
            args = self.packagecap_cfg['args']
            for arg in args:
                interface = arg['interface']
                protocol = arg['protocol']
                time_last = arg['time_last']
                cmd = 'nohup python %s start %s %s %s > %s 2>&1 &' % (self.mainpath, interface, protocol, time_last, self.logfile)
                os.system(cmd)

    def stop_packagecap(self):
        if self.get_packagecap_status():
            cmd = 'nohup python %s stop > %s 2>&1 &' % (self.mainpath, self.logfile)
            os.system(cmd)
