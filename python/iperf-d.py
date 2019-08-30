#coding:utf-8
import os
import time
import subprocess
import matplotlib.pyplot as plt
filename = input('Please input filename:') #输出文件名
testtime = input('Please input test time:') #单位s

up_throughput = []
down_throughput = []

p = subprocess.Popen('iperf -c 192.168.100.9 -p 8989 -i 1 -M 1400 -t '+testtime+' -f m -d',stdout=subprocess.PIPE,shell=True)
p.wait()
a = p.stdout.read()
print(a)  
s = a.split('\n')
up_id = s[8].split(']')[0]  #区分上传和下载的测试ID
down_id = s[9].split(']')[0]
for item in s:
    if up_id in item and 'MBytes' in item:
        b = str(item).split('MBytes')[1].split('Mbits/sec')[0]
        up_throughput.append(float(b))

    if down_id in item and 'MBytes' in item:
        c = str(item).split('MBytes')[1].split('Mbits/sec')[0]
        down_throughput.append(float(c))
	

file1 = open(filename +'.txt','a')   #被写入数据的文件         
file1.write("upload" + str(up_throughput)+"\n\n")       
file1.write("download" + str(down_throughput)+"\n\n")
file1.close()


plt.title('MP2TCP Performance'+' '+ '(' + filename +')')  #标题
plt.plot(up_throughput,color='green',label='upload')   
plt.plot(down_throughput,color='red',label='download')
plt.grid(alpha=0.4)  #画网格
plt.legend()  #显示图例
plt.xlim(0,eval(testtime))  #坐标范围
plt.ylim(0,)  
plt.xlabel('time [s]')           #横坐标标注
plt.ylabel('throughput[Mbits]')   #纵坐标标注
plt.show()