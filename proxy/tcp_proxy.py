 #-*-coding:utf-8-*-
import sys
import socket
import threading
def proxy_handler(client_socket,remote_host,remote_port,receive_first):
    
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    
    #如果必要从远程接受信息
    if receive_first:
        
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
        remote_buffer = response_handler(remote_buffer)
        
        if len(remote_buffer):
            print "[<==] Sending %d bytes to loaclhsot." % len(remote_buffer)
            len(remote_buffer)
            client_socket.send(remote_buffer)
            
    while True:
        
        #发送给我们的本地请求
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print "[==>] Rec %d bytes from loaclhost" % len(local_buffer)
            hexdump(local_buffer)
            
            local_buffer = response_handler(local_buffer)
            
            remote_socket.send(local_buffer)
            print "[==>] Send to remote"
            
        #接受响应数据
        remote_buffer = receive_from(remote_socket)    
        if len(remote_buffer):
            print "[<==] Rec %d bytes from remote" % len(remote_buffer)
            hexdump(remote_buffer)
            #发送到响应处理函数response_handler
            remote_buffer = response_handler(remote_buffer)
            
            client_socket.send(remote_buffer)
            print "[<==] Send to local"
        
        #两边没数据关闭链接    
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more date,close socket"
            break
# this is a pretty hex dumping function directly taken from
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    print b'\n'.join(result)
    
#接受远程或本地的数据
def receive_from(connection):
    
    buffer = ""
    
    #设置2秒超时
    connection.settimeout(2)
    
    try:
        #持续读取到没有数据或超时
        while True:
            date = connection.recv(4096)
            if not date:
                break
            buffer += date
            
    except:
        pass
    return buffer

#对目标是远程主机的请求
def request_handler(buffer):
    #修改操作
    return buffer

#球目标是本地的相应
def response_handler(buffer):
    #修改操作
    return buffer
    
    
    
    
def server_loop(local_host,local_port,remote_host,remote_port,recevice_first):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except:
        print "[!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!] Check for other listening sockets or correct permissions"
        sys.exit(0)
    print "[*] Listening on %s:%d" % (local_host,local_port)
    
    server.listen(5)
    
    while True:
        client_scoket,addr = server.accept()
        
        print "[===>] Recived from %s:%d" % (addr[0],addr[1])
        proxy_thread = threading.Thread(group=None, target=proxy_handler, name=None, 
                                       args=(client_scoket,remote_host,remote_port,
                                             recevice_first), 
                                       kwargs=None, 
                                       verbose=None)
        proxy_thread.start()
        
def main():
    if len(sys.argv[1:]) != 5:
        print "usgae:tcp_proxy.py [localhsot][loacalport][remotehost][remoteport][recevice_first]"
        sys.exit()
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    recevice_first =sys.argv[5]
    
    if "True" in recevice_first:
        recevice_first = True
    else:
        recevice_first = False
        
    server_loop(local_host, local_port, remote_host, remote_port, 
               recevice_first)
main()