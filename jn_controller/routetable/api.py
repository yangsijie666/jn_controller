import json
import os


class API(object):

    def __init__(self):
        self.abs_cwd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
        self.mainpath = self.abs_cwd + 'main.py'
        self.logfile = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'log' + os.path.sep + 'routetable.log'
        cfg_json_name = os.path.abspath(self.abs_cwd + '..') + os.path.sep + 'config.json'
        with open(cfg_json_name, 'r') as f:
            all_cfg_json_dict = json.load(f)
        self.routetable_cfg = all_cfg_json_dict['routetable']

    def get_routetable_status(self):
        status = self.routetable_cfg['status']
        if status == 'on':
            return True
        elif status == 'off':
            return False
        else:
            print('json file: routetable status should be \'on\' or \'off\'!')
            exit(1)

    # functions that can be called
    def start_routetable(self):
        if self.get_routetable_status():
            args = self.routetable_cfg['args']
            time_last = args['time_last']
            time_interval = args['time_interval']
            cmd = 'nohup python %s start %s %s > %s 2>&1 &' % (self.mainpath, time_last, time_interval, self.logfile)
            os.system(cmd)

    def stop_routetable(self):
        if self.get_routetable_status():
            cmd = 'nohup python %s stop > %s 2>&1 &' % (self.mainpath, self.logfile)
            os.system(cmd)
