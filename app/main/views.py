#!/usr/bin/env python
# encoding: utf-8
# Author: limz
# time: 2018-03-08


from flask import render_template
import sys,os
from . import main
import yaml
from paramiko_ssh import ssh
import threading
import time
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
info = yaml.safe_load(config_file)
config_file.close()
back_info = []

def func(queue, password, port, cmdlist):
    thread = threading.current_thread()
    thread_name = thread.getName()
    while 1:
        if queue.empty():
            break
        else:
            ip = queue.get()
            a = ssh(ip, password, port, cmdlist)
            a.append(ip)
            a.append(thread_name)
            back_info.append(a)


def huoquxinxi(city):
    name = info[city]['name']
    message_ip = info[city]['message_ip']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    ips = info[city]['ips']
    return name,message_ip,password,port,ips

@main.route('/')
def index():
    info1 = info
    return render_template('index.html', info=info1)


@main.route('/<city>/redis/<redis_port>/<redis_key>/<auth>/')
def redis(city, redis_port, redis_key, auth):
    name, message_ip, password, port, ips = huoquxinxi(city)
    cmdlist = []
    if auth == 0:
        cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " llen " + redis_key
    else:
        cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " -a " + auth + " llen " + redis_key
    cmdlist.append(cmd)
    redis_info = ssh(message_ip, password, port, cmdlist)
    return render_template('redis.html', result=redis_info, city=name, ip=message_ip)

@main.route('/<city>/info/<arg>/')
def chaxun_info(city, arg):
    threads = []
    queue = Queue.Queue(maxsize=20)
    name, message_ip, password, port, ips = huoquxinxi(city)
    for ip in ips:
        queue.put(ip)
    if arg == 'sys':
        cmdlist = ['df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\'',
                   'free -h | sed -n 2p| awk \'{print  $2,$7}\'', 'vmstat| sed -n 3p| awk \'{x=100-$15} END {print x}\'',
                   'uptime|grep load|awk -F: \'{print $NF}\'', 'hostname']
    else:
        cmdlist = ['dmidecode | grep  -A2 \'System Information\'|sed -n \'2,3p\'',  # 主板
                   'dmidecode -t 4 |grep Version | uniq',  # cpu
                   'dmidecode -t 17 | grep -e \'Manufacturer\|Size\' | grep -v \'NO DIMM\|No Module Installed\'',  # 内存
                   '/usr/bin/lsusb |grep \'Aladdin Knowledge Systems HASP\' |wc -l',  # 加密狗
                   'fdisk -l | grep -e \'/dev/s.*:\|/dev/s.*：\'|awk -F\' \' \'{print $2 $3 $4}\'',  # 硬盘大小
                   'lspci | grep VGA | grep NVIDIA | awk -F[ \'{print $2}\' | awk -F] \'{print $1}\'',  # 显卡
                   'cat /proc/scsi/scsi | grep \'Model:\'',  # 硬盘厂商
                   'hostname']  # 主机名
    for x in xrange(3):
        t = threading.Thread(target=func, args=(queue, password, port, cmdlist))
        threads.append(t)
    for t in threads:
        t.start()
        time.sleep(1)
    for t in threads:
        t.join()
    global back_info
    tmp_info = back_info
    back_info = []
    if arg == 'sys':
        return render_template('system_info.html', info=tmp_info, city=name)
    elif arg == 'dev':
        return render_template('device_info.html', info=tmp_info, city=name)
    else:
        return render_template('404.html')
