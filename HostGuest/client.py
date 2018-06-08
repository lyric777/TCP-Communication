import socket  # for socket
import sys  # for exit


try:
    # create an AF_INET, STREAM socket (TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET用于 Internet 进程间通信
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + " , Error message : " + msg[1])
    sys.exit()


print('Socket Created')

host = '169.254.200.118'  # IP地址一致，指向服务器地址
port = 22222


print('Ip address is ' + host)

# Connect to remote server
sock.connect((host, port))

print('Socket Connected to ' + host)

while True:
    data = input('>')
    if data == 'exit':
        break
        sock.send(b'exit')
    sock.send(data.encode())  # 发送给服务器的数据
    data = sock.recv(1024)  # 接收数据
    if data == 'exit':
        break
    print(data)

sock.close()
