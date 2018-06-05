import socket
import sys


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + " , Error message : " + msg[1])
    sys.exit()

# 建立连接:
s.connect(('localhost', 9999))  # 小于1024的端口号要管理员才能绑定

# 接收欢迎消息:
print(s.recv(1024))
for data in [b'yee', b'nancy', b'lvy']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024))


'''while True:
    d = input('> ')
    if not d:
        break
    s.send(d.encode())
    d = s.recv(1024).decode()
    if not d:
        break
    print(d)'''


s.send(b'exit')
s.close()
