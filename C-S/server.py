import socket


addr = ('169.254.200.118', 22222)
sock = socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
sock.bind(addr)                      # 监听
sock.listen(5)

while True:
    print('wating for connection...')
    CliSock, ADDR = sock.accept()  # 被动接收连接
    print('...connected from:', addr)

    while True:
        data = CliSock.recv(1024)  # 接收来自客户端的数据
        if data == 'exit':
            break
        print(data)                      # 输出客户端的数据
        servedata = input("what do you want to say")
        CliSock.send('%s' % servedata)  # 返回给客户端的数据
    CliSock.close()

sock.close()
