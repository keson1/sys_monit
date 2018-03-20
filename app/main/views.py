#!/usr/bin/env python
# encoding: utf-8
# Author: limz
# time: 2018-03-08


from flask import render_template
import sys,os
from . import main
import yaml
from paramiko_ssh import ssh

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
info = yaml.safe_load(config_file)
config_file.close()

@main.route('/')
def index():
    info1 = info
    return render_template('index.html', info=info1)


@main.route('/<city>/redis/<redis_port>/<redis_key>/<auth>/')
def redis(city, redis_port, redis_key, auth):
    name = info[city]['name']
    message_ip = info[city]['message_ip']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    cmdlist = []
    if auth == 0:
        cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " llen " + redis_key
    else:
        cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " -a " + auth + " llen " + redis_key
    cmdlist.append(cmd)
    redis_info = ssh(message_ip, password, port, cmdlist)
    return render_template('redis.html', result=redis_info, city=name, ip=message_ip)


@main.route('/<city>/system_info/')
def system_info(city):
    name = info[city]['name']
    ips = info[city]['ips']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    cmdlist = ['df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\'',
               'free -h | sed -n 2p| awk \'{print  $2,$7}\'', 'vmstat| sed -n 3p| awk \'{x=100-$15} END {print x}\'',
               'uptime|grep load|awk -F: \'{print $NF}\'', 'hostname']
    sys_info = []
    for ip in ips:
        a = ssh(ip, password, port, cmdlist)
        a.append(ip)
        sys_info.append(a)
    return render_template('system_info.html', info=sys_info, city=name)

@main.route('/<city>/device_info/')
def device_info(city):
    name = info[city]['name']
    ips = info[city]['ips']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    device_info = []
    cmdlist = ['dmidecode |grep -A16 \'System Information$\'|grep -E \'Manufacturer|Product\'',
               'dmidecode -t 4 |grep Version | uniq',
               'dmidecode -t 17 | grep \'Size:\'|grep -v \'No Module Installed\'',
               '/usr/bin/lsusb |grep Aladdin |wc -l',
               'fdisk -l | grep \'Disk /dev/s\'|awk -F\' \' \'{print $2 $3 $4}\'', 'hostname']
    for ip in ips:
        a = ssh(ip, password, port, cmdlist)
        a.append(ip)
        device_info.append(a)
    return render_template('device_info.html', info=device_info, city=name)