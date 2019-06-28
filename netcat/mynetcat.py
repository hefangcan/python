 #-*-coding:utf-8-*-
import sys
import socket
import getopt
import threading
import subprocess

#定义全局变量
listen = False
command = False
upload = ""
execute =""
target = ""
upload_destination = ""
port = 0


    
def client_sender(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        #连接到目标主机
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
            
        while True:
            #等待数据回传
            recv_len = 1
            response = ""
            
            while recv_len:
                
                date = client.recv(4096)
                recv_len = len(date)
                response += date
                
                if recv_len < 4096:
                    break
            print response,
            
            
            #等待更多的输入
            buffer = raw_input("")
            buffer += "\n"
            
            #发送出去
            client.send(buffer)
            
    
    except:
        print "[*] Execept error; exiting."
        client.close()
        
def server_loop():
        global target
        global port
        
        # if no target is defined we listen on all interfaces
        if not len(target):
                target = "0.0.0.0"
                
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target,port))
        
        server.listen(5)        
        
        while True:
                client_socket, addr = server.accept()
                
                # spin off a thread to handle our new client
                client_thread = threading.Thread(target=client_handler,args=(client_socket,))
                client_thread.start()
                
def run_command(command):
    #换行
    command = command.rstrip()
    
    #运行命令并输出返回
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command.\r\n"
        
    return output
  
def client_handler(client_socket):
    global upload
    global execute
    global command
    
    #检测上传文件
    if len(upload_destination):
        
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not date:
                break
            else:
                file_buffer += data
        #打开文件并写出
        try:
            file_descriptr = open(upload_destination,"wb")
            file_descriptr.write(file_buffer)
            file_descriptr.close
            
            client_socket.send("Success saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to saved file to %s\r\n" % upload_destination)

    #如果是执行命令        
    if len(execute):
        output =run_command(execute)
        client_socket.send(output)
    #如果是SHELL，就进入另外一个循环
    if command:
        while True:
            #跳出一个窗口
            client_socket.send("<BHP:#>")
            #接受文件知道发现enter key
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)
            
def usage():
    print "Myfirst net tool"
    print
    print "usage:mynetcat.py -t target_host -p port"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
        #读取命令选项
    try:
            opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu",["help","listen","execute",
                                    "target","port","command","upload"])
    except getopt.GetoptError as err:
            print str(err)
            usage()
            
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t","--traget"):    
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"unknow Option"
                
    #判断是在监听还是在终端输入数据        
    if not listen and len(target) and port > 0:
            
        buffer = sys.stdin.read()
        client_sender(buffer)
            
    if listen:
        server_loop()
        
main()