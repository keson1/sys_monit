#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: limz
# time: 2018-03-06

import urllib2
import sys,os
from bs4 import BeautifulSoup
import paramiko

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

class monit_info():
    def __init__(self, url):
        self.LOGIN = "yisa_oe"
        self.PASSWORD = "yisa_oe"
        self.URL = url
        self.REALM = "monit"

    def handler_version(self):
        from urlparse import urlparse  # urlparse用来将url拆成各个部分scheme netloc path params query fragment
        hdlr = urllib2.HTTPBasicAuthHandler()  # http验证类 里面有用户名和密码
        hdlr.add_password(self.REALM, urlparse(self.URL)[1], self.LOGIN, self.PASSWORD)  # 将url 用户名 密码添加进去
        opener = urllib2.build_opener(hdlr)  # urlopen不支持验证等高级功能 所以自定义opener
        urllib2.install_opener(opener)  # 建立url开启器
        return self.URL

    def request_version(self):
        from base64 import encodestring  # 编码
        req = urllib2.Request(self.URL)  # 开始请求页面
        b64str = encodestring('%s:%s' % (self.LOGIN, self.PASSWORD))[:-1]  # 将sting转换成base64-data形式 base64为一种形式的二进制编码
        req.add_header("Authorization", "Basic %s" % b64str)  # 添加header标头
        return req

    def run(self):
        for funcType in ('self.handler', 'self.request'):
            url = eval('%s_version' % funcType)()  # eval 将字符串转换成有效的表达式并返回结果
            f = urllib2.urlopen(url)
            html = f.readline()
            f.close()

        soup = BeautifulSoup(html, 'lxml')
        list1 = []
        city_info=[]
        for li in soup.select('td'):
            list1.append(li.get_text())  # monit页面所有内容信息列表

        sys = list1[0:10]  # 系统信息列表
        sys_info=[self.URL,sys[4],sys[6], sys[7], sys[8], sys[9]]
        city_info.append(sys_info)
        daemon = list1[10:]   # 服务信息列表
        if sys[2] == 'Monit 5.22.0':
            flag = 7
        else:
            flag = 5
        n = len(daemon) / flag
        daemon_all = []
        for i in xrange(n):
            daemon_one=[]
            daemon_one.append(daemon[0 + flag * i])
            daemon_one.append(daemon[1 + flag * i])
            daemon_all.append(daemon_one)
        city_info.append(daemon_all)
        return city_info



def ssh(ip,port,password,cmd):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=ip, port=port, username='root', password=password)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    result = stdout.read()
    # 关闭连接
    ssh.close()
    return result