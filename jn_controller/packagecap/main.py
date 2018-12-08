import utils
import datetime
import sys
import os
import signal
import re


mypid = str(os.getpid())
mypidfilename = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + '.pid'    # the file named pid is to store the running processs' pids


def store_pid():
    with open(mypidfilename, 'a') as f:
        f.writelines(mypid + '\n')

def del_pid():
    try:
        with open(mypidfilename, 'r') as f:
            pids = f.readlines()
    except IOError as e:
        print('Error: ', e)
        exit(1)
    else:
        pids.remove(mypid + '\n')
        with open(mypidfilename, 'w') as f:
            f.writelines(pids)

def get_interfaces():
    ifaces = os.listdir('/sys/class/net')
    return ifaces

def get_start_args():
    interfaces = get_interfaces()
    interface = sys.argv[2]
    if interface not in interfaces:
        print('device %s is not found!' % interface)
        exit(1)
    protocol = ''
    time_last = 60
    if sys.argv.__len__() == 5:
        protocol = sys.argv[3]
        time_last = int(sys.argv[4])
    elif sys.argv.__len__() == 4:
        try:
            time_last = int(sys.argv[3])
        except ValueError:
            protocol = sys.argv[3]
    elif sys.argv.__len__() == 3:
        pass
    else:
        help()
    return (interface, protocol, time_last)

def help():
    print('Usage:\n\tStart :python main.py start interface [protocol] [time_last]\n\tStop :python main.py stop\n\tHelp: python main.py help')
    print('Mind!\n\tif time_last <0, it means the process won\'t stop until the user stop is manually.\n\ttime_last is set to 60s by default.')
    exit(1)

def stop():
    # stop the tcpdump process
    pids = os.popen('ps aux | grep "tcpdump -i " | grep -v grep')
    pids = pids.read().splitlines()
    for i in pids:
        result = re.search('\d+', i)
        pid = result.group()
        try:
            os.kill(int(pid), signal.SIGTERM)
        except OSError:
            continue
    # stop the last main process
    try:
        with open(mypidfilename, 'r') as f:
            pids = f.readlines()
    except IOError:
        print('No main process is running!')
    else:
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except OSError:
                continue
        os.remove(mypidfilename)
        print('All capture processes are over...')

def start(instance):
    print('Begin capturing...')
    store_pid()
    instance.start_capture()
    del_pid()
    print('Capture is over...')

if __name__ == '__main__':
    if sys.argv.__len__() >= 2:
        status = sys.argv[1]
        if status == 'start':
            if sys.argv.__len__() >= 3:
                (interface, protocol, time_last) = get_start_args()
                filename = interface + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f'))
                instance = utils.utils(time_last, interface=interface, protocol=protocol, filename=filename)
                start(instance)
            else:
                help()
        elif status == 'stop':
            stop()
        else:
            help()
    else:
        help()
