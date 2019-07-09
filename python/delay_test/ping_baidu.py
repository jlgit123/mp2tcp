# -*- coding: utf-8 -*-

#############################################################
#
# author:jin
# summary:测试三个网卡ping到百度服务器的平均时延，并以表格形式输出平均时延和均方差(过滤掉均方差＞30的结果)
# time ：2019/5/13
# modified-1 by :    
# modify-1-log：
# modified-2 by :  
# modify-2-log：
####################################################################################
import os
import re
import subprocess 
from time import sleep

command_0_telecom = 'ip netns exec ns2 ifconfig' 

ipv4_baidu = ''
ipv6_baidu = ''

unicom_ipv4 = ''
unicom_ipv6 = ''
mobile_ipv4 = ''
mobile_ipv6 = ''
telecom_ipv4 = ''
telecom_ipv6 = ''

file_name = 'delay.txt' 


def get_unicom_v4(cmd):
  c = '100'
  while eval(c) > 50: 
    global ipv4_baidu
    global unicom_ipv4
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    p1 = re.compile(r'[(](.*?)[)]',re.S)
    ipv4_baidu = re.findall(p1,a[0])[0]
    unicom_ipv4 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('unicom_ipv4',b,c))
    
def get_unicom_v6(cmd):
  c = '100'
  while eval(c) > 50: 
    global ipv6_baidu
    global unicom_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    p1 = re.compile(r'[(](.*?)[)]',re.S)
    ipv6_baidu = re.findall(p1,a[0])[0]
    unicom_ipv6 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('unicom_ipv6',b,c))
 
def get_mobile_v4(cmd):
  c = '300'
  while eval(c) > 100:
    global mobile_ipv4
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    mobile_ipv4 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('mobile_ipv4',b,c))

def get_mobile_v6(cmd):
  c = '300'
  while eval(c) > 100:
    global mobile_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    mobile_ipv6 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('mobile_ipv6',b,c))

def get_telecom_v4(cmd):
  c = '300'
  while eval(c) > 200: 
    global telecom_ipv4
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    telecom_ipv4 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('telecom_ipv4',b,c))

def get_telecom_v6(cmd):
  c = '300'
  while eval(c) > 200: 
    global telecom_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    telecom_ipv6 = b
  print('{0:^10}\t{1:^6}\t{2:^6}'.format('telecom_ipv6',b,c))
    
if __name__ == "__main__":
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('netcard','avg','mdev'))
    command_0_unicom = 'ip netns exec ns0 ping www.baidu.com -c 5'
    get_unicom_v4(command_0_unicom)
    command_1_unicom = 'ip netns exec ns0 ping6 ipv6.baidu.com -c 5'
    get_unicom_v6(command_1_unicom)

    command_0_mobile = 'ip netns exec ns1 ping ' + ipv4_baidu + ' -c 5'
    get_mobile_v4(command_0_mobile)
    command_1_mobile ='ip netns exec ns1 ping6 ' + ipv6_baidu + ' -c 5'
    get_mobile_v6(command_1_mobile)


    command_0_telecom = 'ip netns exec ns2 ping ' + ipv4_baidu + ' -c 5'
    get_telecom_v4(command_0_telecom)
    command_1_telecom ='ip netns exec ns2 ping6 ' + ipv6_baidu + ' -c 5'
    get_telecom_v6(command_1_telecom)
   
   
