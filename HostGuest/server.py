import socket
import threading
import time


addr = ('169.254.200.118', 22222)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
sock.bind(addr)  # 监听
sock.listen(10)  # 最大监听数


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')  # 相当于.encode()
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


while True:  # 服务器程序通过一个永久循环来接受来自客户端的连接，accept()会等待并返回一个客户端的连接
    # 接受一个新连接:
    Clisock, ADDR = sock.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(Clisock, ADDR))
    t.start()
