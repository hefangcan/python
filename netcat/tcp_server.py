import socket
import threading

ip   = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定监听
server.bind((ip,port))
#设置连接数0-5，5为由系统分配
server.listen(5)

print "[*] Listen on %s:%d" % (ip,port)

#处理线程
def handle_client(c_socker):
    requset = c_socker.recv(1024)
    print "[*] Recv : %s" % requset
    
    c_socker.send("ACK!")
    c_socker.close()
    
while True:
    client,addr = server.accept()
    print "[*] Accept connection from: %s:%d" % (addr[0],addr[1])
    
    #挂起客户线程，处理传入数据    
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()