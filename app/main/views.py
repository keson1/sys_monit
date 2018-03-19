#!/usr/bin/env python
# encoding: utf-8
# Author: limz
# time: 2018-03-08


from flask import render_template
import sys,os
from . import main
from system_info import sys_info
import yaml

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

#@main.route('/<city>/')
#def monit(city):
#    city_info = []
#    name = info[city]['name']
#    ip = info[city]['ips']
#    password = info[city]['ssh_password']
#    port = info[city]['ssh_port']
#    for i in ip:
#        url = 'http://'+i+':2812'
#        a = monit_info(url)
#        c = a.run()
#        cmd = 'df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\''
#        disk = ssh(i, port, password, cmd)
#        list1 = disk.replace('\n', ' ').split(" ")
#        list2 = list1[0:-1]
#        n = len(list2) / 3
#        disk_all = []
#        for i in xrange(n):
#            disk_one = []
#            for m in xrange(3):
#                disk_one.append(list2[(m + i * 3)])
#            disk_all.append(disk_one)
#        c.append(disk_all)
#        city_info.append(c)
#    return render_template('monit.html', monit=city_info, city=name)

@main.route('/<city>/redis/<redis_port>/<redis_key>/<auth>/')
def redis(city, redis_port, redis_key, auth):
    name = info[city]['name']
    ip = info[city]['message_ip']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    system_info = sys_info(ip, port, password)
    jiya = system_info.redis(redis_port, redis_key, auth)
    return render_template('redis.html', result=jiya, city=name, ip=ip)


@main.route('/<city>/sys_info/')
def base_info(city):
    name = info[city]['name']
    ips = info[city]['ips']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    info_all = []
    for ip in ips:
        system_info = sys_info(ip, port, password)
        disk = system_info.disk()
        mem = system_info.memory()
        cpu = system_info.cpu()
        load = system_info.load()
        hostname = system_info.hostname()
        info1 = []
        info1.append(disk)
        info1.append(mem)
        info1.append(cpu)
        info1.append(load)
        info1.append(hostname)
        info1.append(ip)
        info_all.append(info1)
    return render_template('sys_info.html', info=info_all, city=name)

@main.route('/<city>/device_info/')
def device_info(city):
    name = info[city]['name']
    ips = info[city]['ips']
    password = info[city]['ssh_password']
    port = info[city]['ssh_port']
    info_all = []
    for ip in ips:
        system_info = sys_info(ip, port, password)
        disk = system_info.disk_info()
        mem = system_info.mem_info()
        cpu = system_info.cpu_info()
        mb = system_info.motherboard()
        al = system_info.Aladdin_info()
        hostname = system_info.hostname()
        info1 = []
        info1.append(disk)
        info1.append(mem)
        info1.append(cpu)
        info1.append(mb)
        info1.append(al)
        info1.append(hostname)
        info1.append(ip)
        info_all.append(info1)
    return render_template('device_info.html', info=info_all, city=name)