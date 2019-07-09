# -*- coding: utf-8 -*-

#############################################################
#
# author:jin
# summary:拨号并判断获取ipv4，ipv6地址正确
# time ：2019/3/29
# modified by :         //修改者
# modifier-2-date:
# modify-log：
# note:
# 先唤醒4G网卡，然后拨号上网，同时检查回显ipv4和ipv6地址获取是否成功
####################################################################################
import os
import time
import sched
import socket, struct, re
import sys
from subprocess import Popen, PIPE
from time import sleep

schedule = sched.scheduler( time.time,time.sleep )
command_0 = 'ifconfig'
netcard_1 = 'wwp0s20f0u1u2i5' #联通
netcard_2 = 'wwp0s20f0u1u3i5' #移动
netcard_3 = 'wwp0s20f0u1u4i5' #电信
ipv4_flag = 'inet addr'
ipv6_flag = 'Scope:Global'  

def netcard_up():
    os.system('ifconfig '+netcard_1+' up')#没有返回值
    os.system('ifconfig '+netcard_2+' up')
    os.system('ifconfig '+netcard_3+' up')
    return "netcard_up PASS"
	
def udhcp_i():
    os.system('echo "AT\$QCRMCALL=1,1,3" > /dev/ttyUSB3')
    cmd_1 = 'udhcpc -i '+netcard_1
    udhcp_1 = Popen(cmd_1, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_1, err_1 = udhcp_1.communicate()
    ret_1 = udhcp_1.wait()
    print (out_1)
    if out_1.find('Lease') != -1:
	r_1 = 'netcard_1 udhcp PASS'
    else:
	r_1 = 'netcard_1 udhcp FAIL'
		
    os.system('echo "AT\$QCRMCALL=1,1,3" > /dev/ttyUSB8')
    cmd_2 = 'udhcpc -i '+netcard_2
    udhcp_2 = Popen(cmd_2, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_2, err_2 = udhcp_2.communicate()
    ret_2 = udhcp_2.wait()
    print (out_2)
    if out_2.find('Lease') != -1:
	r_2 = 'netcard_2 udhcp PASS'
    else:
        r_2 = 'netcard_2 udhcp FAIL'

    os.system('echo "AT\$QCRMCALL=1,1,3" > /dev/ttyUSB13')
    cmd_3 = 'udhcpc -i '+netcard_3
    udhcp_3 = Popen(cmd_3, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_3, err_3 = udhcp_3.communicate()
    ret_3 = udhcp_3.wait()
    print (out_3)
    if out_3.find('Lease') != -1:
	r_3 = 'netcard_3 udhcp PASS'
    else:
        r_3 = 'netcard_3 udhcp FAIL'
		
    return (r_1, r_2, r_3)
	
def check_ip():
    p = Popen([command_0], stdout = PIPE) 
    a = p.stdout.read().split('\n\n')  
    b = [i for i in a if i and i.startswith(netcard_1)]#根据网卡名字匹配对应段落
    b = ''.join(b)
    if b.find(ipv4_flag) != -1:
	v4_1 = 'ipv4,PASS'
    else:
	v4_1 = 'ipv4,FAIL'
		
    c = [i for i in a if i and i.startswith(netcard_2)]
    c = ''.join(c)
    if c.find(ipv6_flag) != -1:
	v6_1 = 'ipv6_1,PASS'
    else:
	v6_1 = 'ipv6_1,FAIL'		

    d = [i for i in a if i and i.startswith(netcard_3)]
    d = ''.join(d)
    if d.find(ipv6_flag) != -1:
	v6_2 = 'ipv6_2,PASS'
    else:
	v6_2 = 'ipv6_2,FAIL'				
    return (v4_1, v6_1, v6_2)			  
	
if __name__ == "__main__":
    fir = netcard_up()
    sec = udhcp_i()
    thr = check_ip()
    print (fir,sec,thr)
	
