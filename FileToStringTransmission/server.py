import os
import json
import time
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = ('169.254.200.118', 22222)
s.bind((ADDR))
s.listen(5)
file_path = 'D:\chaodawenjian.txt'
file_name = file_path.rsplit(os.sep, 1)[1]
file_size = os.path.getsize(file_path)   # 获取文件内容大小
# 发送给客户端的头部信息
header_data = {
    'file_name': file_name,
    'file_size': file_size,
    'date': time.strftime('%Y-%m-%d %X', time.localtime()),
    'charset': 'utf-8'
}
while True:
    conn, addr = s.accept()
    print("%s:%s is connect"% addr)
    request_data = conn.recv(1024)
    print(request_data)
    # 把头部内容发送过去
    conn.send(json.dumps(header_data).encode())
    request_data1 = conn.recv(1024)
    print(request_data1)
    f = open(file_path, 'r')
    content = f.read()
    # 发送文件内容
    conn.sendall(content.encode())
    conn.close()
