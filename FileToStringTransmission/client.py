# -*- coding:utf-8 -*-

import socket
import json


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = ('169.254.200.118', 22222)
    s.connect(ADDR)
    user_input = input('>>>:').strip()
    if len(user_input) == 0:
        continue
    if user_input == 'q':
        break
    s.send(user_input.encode())
    server_head_msg = json.loads(s.recv(1024).decode('utf-8'))
    print(server_head_msg)
    # 文件名res_name，文件大小res_size
    res_name = server_head_msg['file_name']
    res_size = server_head_msg['file_size']
    s.send('已经收到头部信息,你可以发送数据了'.encode())
    # 下面是循环接收文件内容的部分
    num = res_size / 1204.0
    if num != int(num):
        num = int(num) + 1
    else:
        num = int(num)
    for i in range(num):
        content = s.recv(1024)
        print(content)
