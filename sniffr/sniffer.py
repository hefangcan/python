#-*-coding:utf-8-*-
import socket
import os

#监听的主机
host = "192.168.2.249"

#创建原始套接字，并绑定
if os.name == "nt":#判断系统平台
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) 

sniffer.bind((host, 0))
#捕获的时候包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#win下开启IOCTL启用混杂模式
if os.name  == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

print sniffer.recvfrom(65565)

#对应关闭
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)