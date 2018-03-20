#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: limz
# time: 2018-03-08

import sys,os,yaml
import paramiko

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
info = yaml.safe_load(config_file)
config_file.close()

class sys_info():
    def __init__(self,ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password

    def ssh(self,cmd):
        try:
            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=self.ip, port=self.port, username='root', password=self.password, timeout=5)
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result = stdout.read()
            # 关闭连接
            ssh.close()
            return result
        except Exception,e:
            return 'error'

    #磁盘信息
    def disk(self):
        cmd = 'df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\'df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\''
        disk = self.ssh(cmd)
        if disk == 'error':
            return disk
        else:
            list1 = disk.replace('\n', ' ').split(" ")
            list2 = list1[0:-1]
            n = len(list2) / 3
            disk_all = []
            for i in xrange(n):
                disk_one = []
                for m in xrange(3):
                    disk_one.append(list2[(m + i * 3)])
                disk_all.append(disk_one)
            return disk_all

    # 内存
    def memory(self):
        cmd = 'free -h | sed -n 2p| awk \'{print $7}\''
        available = self.ssh(cmd)
        cmd = 'free -h | sed -n 2p| awk \'{print $2}\''
        total = self.ssh(cmd)
        mem_info=[]
        mem_info.append(available)
        mem_info.append(total)
        return mem_info

    def cpu(self):
        cmd = 'vmstat| sed -n 3p| awk \'{x=100-$15} END {print x}\''
        cpu_info = self.ssh(cmd)
        return cpu_info

    def load(self):
        cmd = 'uptime|grep load|awk -F: \'{print $NF}\''
        load_info = self.ssh(cmd)
        return load_info

    def hostname(self):
        cmd = 'hostname'
        hostname_info = self.ssh(cmd)
        return hostname_info

    def motherboard(self):
        cmd = 'dmidecode |grep -A16 \'System Information$\'|grep -E \'Manufacturer|Product\''
        mb_info = self.ssh(cmd)
        return mb_info

    def cpu_info(self):
        cmd = 'dmidecode -t 4 |grep Version'
        cpu_info = self.ssh(cmd)
        return cpu_info

    def mem_info(self):
        cmd = 'dmidecode -t 17 | grep \'Size:\'|grep -v \'No Module Installed\''
        mem_info = self.ssh(cmd)
        return mem_info

    def Aladdin_info(self):
        cmd = '/usr/bin/lsusb |grep Aladdin |wc -l'
        Ala_info = self.ssh(cmd)
        return Ala_info

    def disk_info(self):
        cmd = 'fdisk -l | grep \'Disk /dev/s\'|awk -F\' \' \'{print $3 $4}\''
        disk_info = self.ssh(cmd)
        return disk_info

    def redis(self, redis_port, redis_key, auth):
        if auth == 0:
            cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " llen " + redis_key
        else:
            cmd = "/yisa_oe/redis/redis-cli -p " + redis_port + " -a " + auth + " llen " + redis_key
        jiya = self.ssh(cmd)
        return jiya

#if __name__== "__main__":
#    city='dazhou'
#    ips = info[city]['ips']
#    password = info[city]['ssh_password']
#    port = info[city]['ssh_port']
#    info_all = []
#    for ip in ips:
#        system_info = sys_info(ip, port, password)
#        disk = system_info.disk()
#        mem = system_info.memory()
#        cpu = system_info.cpu()
#        load = system_info.load()
#        hostname = system_info.hostname()
#        info1 = []
#        info1.append(disk)
#        info1.append(mem)
#        info1.append(cpu)
#        info1.append(load)
#        info1.append(hostname)
#        info1.append(ip)
#        info_all.append(info1)
#    for i in info_all:
#        print i

#if __name__== "__main__":
#    ip='51.116.31.244'
#    port = '22'
#    password = 'yisa_lz_030509'
#    system_info = sys_info(ip, port, password)
#    disk = system_info.disk_info()
#    print disk

