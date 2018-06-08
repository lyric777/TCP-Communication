import socket
import struct
import sys


# in host OS
host = '169.254.200.118'
port = 23333
fmt = '128si'  # 长度为128的字符串（文件名)+整型（size）
recv_buffer = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))


while True:
    print('waiting for connection...')
    s.listen(5)
    conn, addr = s.accept()
    headsize = struct.calcsize(fmt)  # struct.calcsize用于计算格式字符串所对应的结果的长度
    head = conn.recv(headsize)
    try:
        filename = struct.unpack(fmt, head)[0].decode().rstrip('\0')  # 要删掉用来补齐128个字节的空字符
        filename = '/'+filename
        filesize = struct.unpack(fmt, head)[1]
    except struct.error as e:
        print("Error...")
        sys.exit()
    print("filename:" + filename + "\nfilesize:" + str(filesize))
    recved_size = 0
    fd = open(filename, 'wb')
    count = 0
    while True:
        data = conn.recv(recv_buffer)
        recved_size = recved_size + len(data) 
        print("receive:" + str(len(data)))
        fd.write(data)
        if recved_size == filesize:
            break
    fd.close()
    break
print("Successfully Received")
conn.close()
s.close()
