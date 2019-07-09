# -*- coding: utf-8 -*-

#############################################################
#
# author:jin
# summary:获取网卡0的ipv4，网卡1、2的ipv6，全部转换为十进制(register可读)，仅在变化时打印并写入文件，simple_switch_cli读取文件
# time ：2019/3/22
# modified by :         //修改者
# modifier-2-date:
# modify-log：
# note:src_ipv4 1条 src_ipv6 4条 共写入5条
# 存在error无法屏蔽，因为调用函数p.stdout.read():close failed in file object destructor:
# sys.excepthook is missing
# lost sys.stderr
####################################################################################
import os
import time
import sched
import socket, struct, re
import sys
import subprocess
from subprocess import Popen, PIPE
from time import sleep

#STDERR = sys.stderr
#def excepthook(*args):
 #   print >> STDERR, 'caught'
  #  print >> STDERR, args

#sys.excepthook = excepthook
flag_id0 = 'wwp0s20f0u1u2i5'  #网卡名字
flag_id1 = 'wwp0s20f0u1u3i5'  
flag_id2 = 'wwp0s20f0u1u4i5'
command_0 = 'ifconfig'
command_0_liantong = 'ip netns exec ns0 ifconfig' #查看具体namespace下的网卡信息
command_0_yidong = 'ip netns exec ns1 ifconfig'
command_0_dianxin = 'ip netns exec ns2 ifconfig' 
command_1 = 'simple_switch_CLI --thrift-port 9090 < ' 
ipv4_0 = ''
ipv4_temp_0 = ''
mac_0 = ''

ipv4_1 = ''
ipv4_temp_1 = ''
ipv6_1 = ''
ipv6_temp_1 = ''
mac_1 = ''

ipv4_2 = ''
ipv4_temp_2 = ''
ipv6_2 = ''
ipv6_temp_2 = ''
mac_2 = ''


file_name = 's1_dynamic.txt'

schedule = sched.scheduler( time.time,time.sleep )

#被周期性调度触发的函数
def get_ipv4_0():
    #p = Popen([command_0], stdout = PIPE)
    p = subprocess.Popen(command_0_liantong,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id0)]
    mac_0 = b[0].split('\n')[0].split()[4]
    ipv4_temp_0 = b[0].split('\n')[1].split()[1].split(':')[1] 
    global ipv4_0
    if ipv4_temp_0 != ipv4_0:
       ipv4_0 = ipv4_temp_0
       ipv4_0_out = str(ip2long(ipv4_0))
       print 'wwp0s20f0u4u2i5: ' + mac_0 
       print 'ipv4_netcard_0: ' + ipv4_0 +' '+ipv4_0_out +'\n'
       f = open(file_name, 'w+') 
       #f.write('register_write dst_mac 0 '+str(mac_0) +'\n')
       f.write('register_write src_ipv4 0 '+str(ipv4_0_out) + '\n')
       f.close()
      #ret = os.popen(command_1+file_name)
	  #print str(ret)



#被周期性调度触发的函数
def get_ipv6_1():
    #p = Popen([command_0], stdout = PIPE)
    p = subprocess.Popen(command_0_yidong,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id1)]
    mac_1 = b[0].split('\n')[0].split()[4]
    ipv6_temp_1 = b[0].split('\n')[2].split()[2] 
    global ipv6_1   
    if ipv6_temp_1 != ipv6_1:
       ipv6_1 = ipv6_temp_1
       ipv6_1_out = ipv6_1.split('/')[0]
       ipv6_1_out_0 = str(int(ipv62dec_0(ipv6_1_out), 16))
       ipv6_1_out_1 = str(int(ipv62dec_1(ipv6_1_out), 16))
       print 'wwp0s20f0u4u3i5: ' + mac_1 
       print 'ipv6_netcard_1: ' + ipv6_1 +'\n' +ipv6_1_out_0+'  '+ipv6_1_out_1 +'\n'
       f = open (file_name, 'a+') 
       #f.write('register_write dst_mac 1 '+str(mac_1) +'\n')
       f.write('register_write src_ipv6_1 0 '+str(ipv6_1_out_0) + '\n')
       f.write('register_write src_ipv6_1 1 '+str(ipv6_1_out_1) + '\n')
       f.close()

#被周期性调度触发的函数
def get_ipv6_2():
    #p = Popen([command_0], stdout = PIPE)
    p = subprocess.Popen(command_0_dianxin,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id2)]
    mac_2 = b[0].split('\n')[0].split()[4]  
    ipv6_temp_2 = b[0].split('\n')[2].split()[2] 
    global ipv6_2    
    if ipv6_temp_2 != ipv6_2:
       ipv6_2 = ipv6_temp_2
       ipv6_2_out = ipv6_2.split('/')[0]
       ipv6_2_out_0 = str(int(ipv62dec_0(ipv6_2_out), 16))
       ipv6_2_out_1 = str(int(ipv62dec_1(ipv6_2_out), 16))
       print 'wwp0s20f0u4u4i5: ' + mac_2 
       print 'ipv6_netcard_2: ' + ipv6_2 +'\n' +ipv6_2_out_0+'  '+ipv6_2_out_1 +'\n'
       f = open (file_name, 'a+') 
       #f.write('register_write dst_mac 2 '+str(mac_2) +'\n')
       f.write('register_write src_ipv6_2 0 '+str(ipv6_2_out_0) + '\n')
       f.write('register_write src_ipv6_2 1 '+str(ipv6_2_out_1) + '\n')
       f.write('EOF') #结束退出
       f.close()
       #ret = os.popen(command_1+file_name)

       #print str(ret)
   
#ipv4地址转换
def ip2long(ip):
  packedIP = socket.inet_aton(ip)
  return struct.unpack("!L", packedIP)[0]
 
#ipv6地址转换 
def ipv62dec_0(ipv6): #前64bit
    if checkipv6(ipv6):
        compressIndex = ipv6.find('::')
        if compressIndex==-1:  #没有缩写格式
	  s=noCompressipv62str(ipv6) 
	  ss=s.split('-')
	  return ss[0]  
        else:
          s=compressipv62str(ipv6)
	  ss=s.split('-')
	  return ss[0]
    else:
        return ""
		
def ipv62dec_1(ipv6):#后64bit
    if checkipv6(ipv6):
        compressIndex = ipv6.find('::')
        if compressIndex==-1:  #没有缩写格式
	  s=noCompressipv62str(ipv6) 
	  ss=s.split('-')
	  return ss[1]  
        else:
          s=compressipv62str(ipv6)
	  ss=s.split('-')
	  return ss[1]
    else:
        return ""
#2001:DB8:0:23:8:800:200C:417A convert to 2001:0DB8:0000:0023:0008:0800:200C:417A
def ipseg2str(ipseglist):
    ipstr=''
    for ipseg in ipseglist:
        if len(ipseg) == 1:
            ipseg = '000' + ipseg
        elif len(ipseg) == 2:
            ipseg = '00' + ipseg
        elif len(ipseg) == 3:
            ipseg = '0' + ipseg
        elif len(ipseg) == 4:
            ipseg = ipseg
        else:
            return ""
        ipstr += ipseg
    return ipstr

#convert 2001:DB8:0:23:8:800:200C:417A to dec
def noCompressipv62str(ipv6):
    iplist = ipv6.split(":")
    if iplist:
        ipstr = ipseg2str(iplist)  #补零充位
	b=re.findall(r'.{16}',ipstr) 
 	c='-'.join(b)
	return c
    else:
        return ""

#Convert FF01::1101 to dec
def compressipv62str(ipv6):
    compressList = ipv6.split("::")
    ipstr = ""
    part1 = []
    part2 = []
    if len(compressList) == 2:
        part1 = compressList[0].split(":") if compressList[0] else []
        part2 = compressList[1].split(":") if compressList[1] else []
    if part1 or part2:
        ipstr += ipseg2str(part1)
        for i in range(8 - len(part1) - len(part2)):
            ipstr += '0000'
        ipstr += ipseg2str(part2)
        b=re.findall(r'.{16}',ipstr) 
 	c='-'.join(b)
	return c
    else:
        return ""

#check ipv6
def checkipv6(ipv6):
    matchobj = re.match(r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$',ipv6)
    if matchobj:
        return True
    else:
        return False

 
#enter四个参数分别为：间隔时间、优先级（同时到达的两事件同时执行时定序）、被调用触发的函数，给他的参数（注意：一定要以tuple，如果只有一个参数就(xx,)）
def perform(inc=1):
    schedule.enter(inc,0,perform,(inc,)) 
    get_ipv4_0()  
    get_ipv6_1() 
    get_ipv6_2()

def mymain(inc=1):
    schedule.enter(0,0,perform,(inc,))
    schedule.run()
 
if __name__ == "__main__":
    mymain()
