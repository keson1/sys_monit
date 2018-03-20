#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: test.py
@time: 2018/3/20 10:57
@Description:
'''
import sys,os,yaml
import paramiko
config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
info = yaml.safe_load(config_file)
config_file.close()

city='dazhou'
ips = info[city]['ips']
password = info[city]['ssh_password']
port = info[city]['ssh_port']
def ssh(ip,password,port):
    try:
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=ip, port=port, username='root', password=password, timeout=5)
        # 执行命令
        cmdlist=['df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\'', 'free -h | sed -n 2p| awk \'{print  $2,$7}\'', 'vmstat| sed -n 3p| awk \'{x=100-$15} END {print x}\'', 'uptime|grep load|awk -F: \'{print $NF}\'', 'hostname']
        for cmd in cmdlist:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result1 = stdout.read()
            result = result1.strip('\n').split('\n')
            yield result
        # 关闭连接
        ssh.close()
    except Exception, e:
        result = 'error'
        yield result
sys_info = []
for ip in ips:
    a = ssh(ip, password, port)
    sys_info.append(a)
print sys_info
for i in sys_info:
    for c in i:
        print c