#!/usr/bin/env python
import utils
import sys
import os
import signal


pid = str(os.getpid())
pidfilename = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + '.pid'    # the file named pid is to store the running processs' pids


def store_pid():
    with open(pidfilename, 'a') as f:
        f.writelines(pid + '\n')

def del_pid():
    try:
        with open(pidfilename, 'r') as f:
            pids = f.readlines()
    except IOError as e:
        print('Error: ', e)
        exit(1)
    else:
        pids.remove(pid + '\n')
        with open(pidfilename, 'w') as f:
            f.writelines(pids)

def start(instance):
    print('Start routetable record...')
    store_pid()
    instance.start_get_route_table()
    del_pid()
    print('Finish routetable record...')

def stop():
    try:
        with open(pidfilename, 'r') as f:
            pids = f.readlines()
    except IOError:
        print('No process is running!')
    else:
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except OSError:
                continue
        os.remove(pidfilename)
        print('Finish routetable record...')

def help():
    print('Usage:\n\tStart :python main.py start [time_last [time_interval]]\n\tStop :python main.py stop\n\tHelp: python main.py help')
    print('Mind!\n\tif time_last or time_interval not set, time_last will be set to 60s and time_interval will be set to 1s.')
    exit(1)


if __name__ == '__main__':
    time_last = 60
    time_interval = 1
    if sys.argv.__len__() == 1:
        help()
    if sys.argv[1] == 'help':
        help()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'start':
        if sys.argv.__len__() == 2:
            pass
        elif sys.argv.__len__() == 3:
            time_last = sys.argv[2]
        elif sys.argv.__len__() == 4:
            time_last = sys.argv[2]
            time_interval = sys.argv[3]
        else:
            help()
        instance = utils.utils(time_last, time_interval)
        start(instance)
    else:
        help()
