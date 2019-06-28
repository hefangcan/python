import threading
import paramiko
import subprocess

#方法函数ssh_command
def ssh_command(ip,user,passwd,command):
    #创建一个SSH客户端对象
    client = paramiko.SSHClient()
    #以传统用户密码验证，还有一种可以用SSH密钥认证
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #开始连接
    client.connect(hostname=ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        #如果链接成功，执行命令并打出结果
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
        ssh_session.close
    return

ssh_command('kjol.cc','123','123','command命令')
