# -*- coding: utf-8 -*-

#############################################################
#
# author:jin
# summary:周期性（1s）查询网关mac地址，仅在变化时打印并写入流表
# time ：
# modified by :         //修改者
# modifier-2-date:
# modify-log：
# note:
####################################################################################
import os
import time
import sched

	
flag_message = 'UG'  #匹配1
flag_message_2 = ''  #匹配2
command_1 = 'route -n'
command_2 = 'arp -a' 
ip_gate = ''
ip_temp = ''
mac_gate = ''
mac_temp = ''

schedule = sched.scheduler( time.time,time.sleep )

#被周期性调度触发的函数
def get_gate():
  ret_1 = os.popen(command_1) #ip
  info_1 = ret_1.readlines()  
  for line in info_1:  #按行遍历
     if line.find(flag_message) != -1: 
        list_1 = line.split() 
        for i in range(0,len(list_1)-1): 
           if list_1[i] == flag_message:
	       ip_temp = list_1[i-2]   #网关ip
               global ip_gate	       
	       if ip_temp != ip_gate:
	         ip_gate = ip_temp
                 print 'ip_gate: ' + ip_gate 

	 	
  flag_message_2 = '('+ ip_gate +')'
  ret_2 = os.popen(command_2) #mac
  info_2 = ret_2.readlines()  
  for line in info_2:  #按行遍历
     if line.find( ip_gate ) != -1: 
        list_2 = line.split() 
        for i in range(0,len(list_2)-1): 
           if list_2[i] == flag_message_2:  
               mac_temp = list_2[i+2]	
               global mac_gate  
	       if mac_temp != mac_gate:
	         mac_gate = mac_temp
                 print 'mac_gate: ' + mac_gate   



#enter四个参数分别为：间隔时间、优先级（同时到达的两事件同时执行时定序）、被调用触发的函数，给他的参数（注意：一定要以tuple，如果只有一个参数就(xx,)）
def perform(inc=1):
    schedule.enter(inc,0,perform,(inc,)) 
    get_gate()
    

def mymain(inc=1):
    schedule.enter(0,0,perform,(inc,))
    schedule.run()
 
if __name__ == "__main__":
    mymain()


