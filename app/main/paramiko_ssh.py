#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: paramiko_ssh.py
@time: 2018/3/20 10:57
@Description:
'''
import sys,os,yaml
import paramiko

def ssh(ip,password,port,cmdlist):
    try:
        # 创建SSH对象
        result = []
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=ip, port=port, username='root', password=password, timeout=5)
        # 执行命令
        for cmd in cmdlist:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result1 = stdout.read()
            result.append(result1)
        ssh.close()
        return result
    except Exception, e:
        result = ['error']
        return result
