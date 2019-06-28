import socket

traget_host = "127.0.0.1"
traget_port = 9999

#建立socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#发起连接
client.connect((traget_host,traget_port))
#发送数据
client.send("GET / HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n")
#取回数据
response = client.recv(4096)

print response