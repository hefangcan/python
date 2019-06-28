#-*-coding:utf-8-*-
import socket
import os
import struct
import threading
import time

from netaddr import IPNetwork,IPAddress
from ctypes import *


#监听主机
host   = "192.168.2.249"

#要扫描的目标子网
subnet = "183.1.85.0/24"

#ICMP想要的核对魔法数据，自定义
magic_message = "MAGIC"

#批量发送UDP数据包
def udp_sender(subnet,magic_message):
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message,("%s" % ip,65212))
        except:
            pass
#ip头定义
########################################################################
class IP(Structure):
    
    _fields_ = [
        ("ihl",     c_ubyte,4),
        ("version", c_ubyte,4),
        ("tos",     c_ubyte),
        ("len",     c_ushort),
        ("id",      c_ushort),
        ("offset",  c_ushort),
        ("ttl",     c_ubyte),
        ("protocol_num",c_ubyte),
        ("sum",     c_ushort),
        ("src",     c_ulong),
        ("dst",     c_ulong)
    ]
    
    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self,socket_buffer=None):

        #协议字段跟协议名对应，常见的有如：
        #1 ICMP 
        #2 IGMP 
        #6 TCP 
        #17 UDP 
        #88 IGRP 
        #89 OSPF
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}
        #转换下可读性更强的IP地址
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))
        #协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

########################################################################
class ICMP(Structure):
    
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
        ]

    #----------------------------------------------------------------------
    def __new__(self,socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    def __init__(self,socket_buffer):
       pass



#创建原始套接字，并绑定，跟之前的代码差不多 
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) 

sniffer.bind((host, 0))
#捕获的时候包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
if os.name  == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

#创建发送UDP信息线程
t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()  

try:
    while True:
        #读取数据包
        raw_buffer = sniffer.recvfrom(65565)[0]
        #将缓冲数据的前20字节按IP头格式解析
        ip_header = IP(raw_buffer[0:20])
        #输出双方IP
        #print "Protocol:%s %s -> %s" % (ip_header.protocol,
        #                                ip_header.src_address,
        #                                ip_header.dst_address)
        #如果包是ICMP就进行处理
        if ip_header.protocol == "ICMP":
            #
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            
            icmp_header = ICMP(buf)
            
            #print "ICMP -> Type:%d Code:%d" % (icmp_header.type,icmp_header.code)
            
            #如果检测到类型跟代码都是3的
            if icmp_header.code == 3 and icmp_header.type == 3:
                #确定响应主机在我们设置的目标之内
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    if raw_buffer[len(raw_buffer)-len(magic_message):] == magic_message:
                        print "Host on line:%s" % ip_header.src_address
            
except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        

        