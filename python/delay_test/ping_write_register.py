# -*- coding: utf-8 -*-

#############################################################
#
# author:jin
# summary:周期性测试三个网卡ping到服务器的平均时延，计算三条链路需要绕的圈数，分别写入寄存器
# log:比较时延时首先获取时延最大的链路，然后根据最差链路计算剩下两条链路的绕圈数，同时把最差链路的绕圈数置为0
# time ：2019/5/13
# modified-1 by :    
# modify-1-log：
# modified-2 by :  
# modify-2-log：
####################################################################################
import os
import re
import subprocess 
import time
import sched
import re
from time import sleep
 
unicom_ipv6 = ''
mobile_ipv4 = ''
mobile_ipv6 = ''
telecom_ipv4 = ''
telecom_ipv6 = ''
global circle_unicom
global circle_mobile
global circle_telcom

file_name = 's1-runtime.txt' 
schedule = sched.scheduler(time.time,time.sleep)  #用于定时
def get_unicom_v6(cmd):
  #c = '300'
  #while eval(c) > 150: 
    global unicom_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    #p1 = re.compile(r'[(](.*?)[)]',re.S)
    #ipv6_baidu = re.findall(p1,a[0])[0]
    unicom_ipv6 = b
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('unicom_ipv6',b,c))
 
def get_mobile_v4(cmd):
  #c = '300'
  #while eval(c) > 150: 
  global mobile_ipv4
  try:
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stderr.read().split('\n')
    b = a[-2].split('/')[3]
    mobile_ipv4 = b
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('mobile_ipv4',b,'no'))
  except:
    mpbilw_ipv4 = '0'
    pass


def get_telecom_v6(cmd):
  #c = '300'
  #while eval(c) > 200: 
    global telecom_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n')
    b = a[-2].split('/')[4]
    c = a[-2].split('/')[6].split()[0]
    telecom_ipv6 = b
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('telecom_ipv6',b,c))

'''def get_telecom_v6(cmd):
  #c = '300'
  #while eval(c) > 200: 
    global telecom_ipv6
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stderr.read().split('\n')
    b = a[-2].split('/')[3]
    telecom_ipv6 = b
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('telecom_ipv6',b,'no'))'''
 
def write_register(x,circle):
   # i = 100
    #while i:
        p = subprocess.Popen('simple_switch_CLI',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True) 
        p.stdin.write('register_write cy_num '+x+' '+circle)
	print('register_write cy_num '+x+' '+circle)
        out,err = p.communicate()

        p = subprocess.Popen('simple_switch_CLI',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True) 
        p.stdin.write('register_read cy_num '+x)
	print('register_read cy_num '+x)
        out_1,err_1 = p.communicate()
        queue = re.findall('cy_num\[\d\]\= \d*', out_1, re.M)
        print ('register_read:'+str(queue[0]))
        #time.sleep(0.8)
     #   i = i - 1 
		
#enter四个参数分别为：间隔时间、优先级（同时到达的两事件同时执行时定序）、被调用触发的函数，给他的参数（注意：一定要以tuple，如果只有一个参数就(xx,)）
def perform(inc=10):   #每5秒执行一次
    schedule.enter(inc,0,perform,(inc,)) 
    command_1_unicom = 'ip netns exec ns0 ping6 2001:da8:205:2060:6eb3:11ff:fe22:2984 -c 20'
    get_unicom_v6(command_1_unicom)

    command_0_mobile = 'ip netns exec ns1 hping3 -S 219.242.112.251 -p 8080 -c 1'
    get_mobile_v4(command_0_mobile)

    command_1_telecom ='ip netns exec ns2 ping6 2001:da8:205:2060:6eb3:11ff:fe22:2986 -c 20'
    #command_1_telecom = 'ip netns exec ns2 hping3 -S 219.242.112.251 -p 8080 -c 1'
    get_telecom_v6(command_1_telecom)
	
    l_1 = eval(unicom_ipv6)
    l_2 = eval(mobile_ipv4)
    l_3 = eval(telecom_ipv6)
    if l_1 > l_2 :
        maxlink = l_1
    else:
        maxlink = l_2
    if l_3 > maxlink:
        maxlink = l_3
    print(maxlink)

    if maxlink == l_1:
        circle_mobile = (l_1/2-l_2/2)//5+1
	circle_telcom = (l_1/2-l_3/2)//5+2
        circle_mobile = str(int(circle_mobile))
        circle_telcom = str(int(circle_telcom))
        write_register('0','0')
        write_register('1',circle_mobile)
        write_register('2',circle_telcom)
    elif maxlink == l_2:
        circle_unicom = (l_2/2-l_1/2)//5-1
	circle_telcom = (l_2/2-l_3/2)//5+1
        circle_unicom = str(int(circle_unicom))
        circle_telcom = str(int(circle_telcom))
        write_register('0',circle_unicom)
        write_register('1','0')
        write_register('2',circle_telcom)
    elif maxlink == l_3:
        circle_unicom = (l_3/2-l_1/2)//5-2
        circle_mobile = (l_3/2-l_2/2)//5-1
        circle_unicom = str(int(circle_unicom))
        circle_mobile = str(int(circle_mobile))
        write_register('0',circle_unicom)
        write_register('1',circle_mobile)
        write_register('2','0')
	

def mymain(inc=10):
    schedule.enter(0,0,perform,(inc,))
    schedule.run()
	
if __name__ == "__main__":
    print('{0:^10}\t{1:^6}\t{2:^6}'.format('netcard','avg','mdev'))
    mymain()
    




   
   
