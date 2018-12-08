import os
import threading
import time
import datetime


class utils(object):

    def __init__(self, time_last, time_interval):
        self.time_last = time_last
        self.time_interval = time_interval
        self.old_route_table = []
        self.route_number = 1
        self.dirname = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(
            __file__))) + os.path.sep + '.') + os.path.sep + 'data' + os.path.sep + 'route_table' + os.path.sep + str(
            datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        os.makedirs(self.dirname)
        self.stop_flag = False

    def get_route_table_(self):
        route_table = os.popen('route -n')
        route_table = route_table.read().splitlines()
        return route_table

    def print_route_table(self, route_table):
        filename = 'route_table_' + str(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')) + '.txt'
        with open(self.dirname + os.path.sep + filename, 'w') as f:
            for route in route_table:
                f.write(str(route) + '\n')
        self.route_number += 1

    def get_route_table(self):
        self.new_route_table = self.get_route_table_()
        if str(self.old_route_table) == str(self.new_route_table):
            pass    # if old table and new table is equal, then do nothing
        else:
            self.print_route_table(self.new_route_table)
            self.old_route_table = self.new_route_table

    def tiktok(self):
        time.sleep(float(self.time_interval))

    def start_get_route_table_(self):
        if self.time_interval != 0:
            while self.stop_flag is False:
                thread = threading.Thread(target=self.tiktok)  # get route table every time_interval second
                thread.start()
                self.get_route_table()
                thread.join()
        else:
            while self.stop_flag is False:
                self.get_route_table()

    def start_get_route_table(self):
        thread = threading.Thread(target=self.start_get_route_table_)
        thread.setDaemon(True)
        thread.start()
        time.sleep(float(self.time_last))
        self.stop_flag = True
