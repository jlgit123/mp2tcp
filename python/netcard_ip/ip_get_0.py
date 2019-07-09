# -*- coding: utf-8 -*-

#############################################################
#
# author:jin 
# summary:获取联通网卡的ipv4,移动和电信的ipv6,转换为十进制标准格式,每秒检测一次，
#         仅在变化时打印并写入文件s1_dynamic.txt,simple_switch_cli读取文件,无需打印可自行注释。
# time ：2019/3/21
# modified by :  3/25       
# modifier-2-date: 
# modify-log：查看具体namespace下网卡;匹配方式由位置切片匹配更改为字符匹配(避免地址出现不全的状况);完善注释和代码规范
# note:src_ipv4 1条 src_ipv6 4条(受限于int数据类型,128bit拆分为两个64bit) 共写入5条,本脚本同时实现了网卡mac的获取
####################################################################################
import os
import time
import sched
import socket, struct, re
import sys
from subprocess import Popen, PIPE
from time import sleep

flag_id0 = 'wwp0s20f0u4u2i5'  #网卡名字--联通 ns1 
flag_id1 = 'wwp0s20f0u4u3i5'  #移动 ns2
flag_id2 = 'wwp0s20f0u4u4i5'  #电信 ns3
command_0 = 'ifconfig'
command_0_liantong = 'ip netns exec ns1 ifconfig' #查看具体namespace下的网卡信息
command_0_yidong = 'ip netns exec ns2 ifconfig'
command_0_dianxin = 'ip netns exec ns3 ifconfig' 
command_1 = 'simple_switch_CLI --thrift-port 9090 < '  #读取文件的命令
ipv4_0 = ''
ipv4_temp_0 = ''
mac_0 = ''
ipv4_flag = 'inet addr'

ipv6_flag = 'inet6 addr'
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


file_name = 's1_dynamic.txt' #文件名称

schedule = sched.scheduler( time.time,time.sleep )  #用于定时

#被周期性调度触发的函数
def get_ipv4_0():
    p = Popen([command_0_liantong], stdout = PIPE)  #查看具体namespace下的网卡信息不直接用ipconfig
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id0)]#根据网卡名字匹配对应段落
    list_1 = b[0].split('\n') 
    mac_0 = list_1[0].split()[4] #获得mac-固定位置匹配	     
    for i in range(0,len(list_1)-1):
        if list_1[i].find(ipv4_flag) != -1: 
            list_2 = list_1[i].split() 
            ipv4_temp_0 = list_2[1].split(':')[1]   #根据inet addr字段匹配ipv4地址	       
            global ipv4_0
            if ipv4_temp_0 != ipv4_0:  #当检测到地址变化时重新赋值
                ipv4_0 = ipv4_temp_0
                ipv4_0_out = str(ip2long(ipv4_0))  #十进制转换
                print 'mac_netcard_0: ' + mac_0 
                print 'ipv4_netcard_0: ' + ipv4_0 +' '+ipv4_0_out
                f = open(file_name, 'w+')    #写入文件，文件若不存在就创建
                #f.write('register_write dst_mac 0 '+str(mac_0) +'\n')
                f.write('register_write src_ipv4 0 '+str(ipv4_0_out) + '\n')
                f.close()

#被周期性调度触发的函数
def get_ipv6_1():
    p = Popen([command_0_yidong], stdout = PIPE)
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id1)]
    list_1 = b[0].split('\n') 
    mac_1 = list_1[0].split()[4] #获得mac-固定位置匹配	     
    for i in range(0,len(list_1)-1):
        if list_1[i].find(ipv6_flag) != -1: 
            list_2 = list_1[i].split() 
            ipv6_temp_1 = list_2[2]   #根据inet6 addr字段匹配ipv6地址
            global ipv6_1   
            if ipv6_temp_1 != ipv6_1:    #当检测到地址变化时重新赋值
                ipv6_1 = ipv6_temp_1
                ipv6_1_out = ipv6_1.split('/')[0]
                ipv6_1_out_0 = str(int(ipv62dec_0(ipv6_1_out), 16))  #十进制转换
                ipv6_1_out_1 = str(int(ipv62dec_1(ipv6_1_out), 16))  
                print 'mac_netcard_1: ' + mac_1 
                print 'ipv6_netcard_1: ' + ipv6_1 +'\n' +ipv6_1_out_0+'  '+ipv6_1_out_1
                f = open (file_name, 'a+')   #追加写入文件，文件若不存在就创建
                #f.write('register_write dst_mac 1 '+str(mac_1) +'\n')
                f.write('register_write src_ipv6_1 0 '+str(ipv6_1_out_0) + '\n')
                f.write('register_write src_ipv6_1 1 '+str(ipv6_1_out_1) + '\n')
                f.close()

#被周期性调度触发的函数
def get_ipv6_2():
    p = Popen([command_0_dianxin], stdout = PIPE)
    a = p.stdout.read().split('\n\n') 
    b = [i for i in a if i and i.startswith(flag_id2)]
    list_1 = b[0].split('\n') 
    mac_2 = list_1[0].split()[4] #获得mac-固定位置匹配	     
    for i in range(0,len(list_1)-1):
        if list_1[i].find(ipv6_flag) != -1: 
            list_2 = list_1[i].split() 
            ipv6_temp_2 = list_2[2]   #根据inet6 addr字段匹配ipv6地址
            global ipv6_2   
            if ipv6_temp_2 != ipv6_2:  #当检测到地址变化时重新赋值
                ipv6_2 = ipv6_temp_2
                ipv6_2_out = ipv6_2.split('/')[0]
                ipv6_2_out_0 = str(int(ipv62dec_0(ipv6_2_out), 16))  #十进制转换
                ipv6_2_out_1 = str(int(ipv62dec_1(ipv6_2_out), 16))  
                print 'mac_netcard_1: ' + mac_2 
                print 'ipv6_netcard_1: ' + ipv6_2 +'\n' +ipv6_2_out_0+'  '+ipv6_2_out_1
                f = open (file_name, 'a+')   #追加写入文件，文件若不存在就创建
                #f.write('register_write dst_mac 2 '+str(mac_2) +'\n')
                f.write('register_write src_ipv6_2 0 '+str(ipv6_2_out_0) + '\n')
                f.write('register_write src_ipv6_2 1 '+str(ipv6_2_out_1) + '\n')
                f.write('EOF') #结束退出
                f.close()
                ret = os.popen(command_1+file_name)

#ipv4地址的十进制转换 --shi
def ip2long(ip):
  packedIP = socket.inet_aton(ip)
  return struct.unpack("!L", packedIP)[0]
 
#ipv6地址的十进制转换  
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
def perform(inc=1):   #每秒执行一次
    schedule.enter(inc,0,perform,(inc,)) 
    get_ipv4_0()  
    get_ipv6_1() 
    get_ipv6_2()

def mymain(inc=1):
    schedule.enter(0,0,perform,(inc,))
    schedule.run()
 
if __name__ == "__main__":
    mymain()
