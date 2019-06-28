import socket

traget_host = "127.0.0.1"
traget_port = 9999

#建立socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#UDP无需建立连接，直接发送数据
client.sendto("AABBCC",(traget_host,traget_port))
#接受数据
addr = client.recvfrom(4096)

print addr