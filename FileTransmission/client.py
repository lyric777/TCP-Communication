import socket
import os
import struct
import sys

# in guest OS

host = '169.254.200.118'
port = 23333
fmt = '128si'
send_buffer = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
except ConnectionRefusedError:
    print("Connection refused")
    sys.exit()

filepath = input("enter file path:")

try:
    filename = os.path.split(filepath)[1]
    filesize = os.path.getsize(filepath)
except FileNotFoundError as e:
    print("FileNotFound")
    sys.exit()

print("filename:" + filename + "\nfilesize:" + str(filesize))
head = struct.pack(fmt, filename.encode(), filesize)
print("head size:" + str(head.__len__()))
sock.sendall(head)
restSize = filesize

try:
    fd = open(filepath, 'rb')
except FileNotFoundError as e:
    print(e.errno)
count = 0
while restSize >= send_buffer:
    data = fd.read(send_buffer)
    sock.sendall(data)
    restSize = restSize - send_buffer
    print(str(count) + " ")
    count = count + 1

data = fd.read(restSize)
sock.sendall(data)
fd.close()
print("Successfully Sent")
sock.close()
