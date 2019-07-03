#!coding=utf-8
import os
import re
import sys
import time
import multiprocessing
import urllib2

#----------------------------------------------------------------------
def main(prots,ip_dic):
    """
    主函数，处理输入的参数
    """
    iplist = None
    try:
        
        iplist=[]
        _ipFile=open(ip_dic, 'r').readlines()
        for echo in _ipFile:
            ip=re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", echo)
            
            if ip != []:
                #print ip[0]
                iplist.append(ip[0])
        p =0
        print "Start test porxy..."
        for proxys in iplist:
            pp =multiprocessing.Process(target=proxy_test,args=(proxys,prots))
            pp.start()
            p +=1
            if p>=50:
                p=0
                pp.join()
        pp.join()
    except Exception:
        print "[!] The path of the dictionary file is incorrect"
        pass
        #exit()
#----------------------------------------------------------------------
def isIP(str):
    """
    判断是否是IP
    """
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False
#----------------------------------------------------------------------
def proxy_test(proxys,prots):
    """
    测试代理是否有效
    """
    proxy = urllib2.ProxyHandler(proxies={"http":"http://{}:{}".format(proxys,prots)})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    
    try:
        testurl ="http://120.79.152.76/ip.php"
        req  =urllib2.Request(testurl)
        res =urllib2.urlopen(req,timeout=5).read()
        #print proxys+":"+prots
        if isIP(res) and res == proxys:
            print "\033[1;32;41m{}\033[0m\n{}".format(proxys+":"+prots,res)
            output = open("good.txt", 'a')
            output.write(proxys+":"+prots+"\n")            
    except Exception as e:
        #print "--------- {}".format(e)
        pass
        
#----------------------------------------------------------------------
if __name__ == '__main__':
    prots = ['3128','1080','8118','9999']
    ip_dic = "proxy.txt"
    ipl="http://ipblock.chacuo.net/down/t_txt=c_CN"
    req  =urllib2.Request(ipl)
    res =urllib2.urlopen(req,timeout=5).read()
    #print res
    ipd=re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}\b", res)
    #print ipd
    for i in ipd:
        print i
        for prot in prots:
            ########################################
            #MASSCAN
            os.system("/root/masscan/bin/./masscan %s -p%s --rate 30000 -oX %s --wait 1" % (i,prot,ip_dic))
            #######################################
            time.sleep(1)
            main(prot,ip_dic)
            time.sleep(10)
    exit()
