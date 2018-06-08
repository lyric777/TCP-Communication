import socket
import struct
import os
import subprocess

dataFormat = '8s32s100s100sl'


class fileClient():
    def __init__(self, addr):
        self.addr = addr
        self.action = ''
        self.fileName = ''
        self.md5sum = ''
        self.clientfilePath = ''
        self.serverfilePath = ''
        self.size = 0

    def struct_pack(self):  # 将5个参数进行一层包装
        ret = struct.pack(dataFormat, self.action.encode(), self.md5sum.encode(), self.clientfilePath.encode(),
                          self.serverfilePath.encode(), self.size)
        return ret

    def struct_unpack(self, package):
        self.action, self.md5sum, self.clientfilePath, self.serverfilePath, self.size = struct.unpack(dataFormat,
                                                                                                      package)
        self.action = self.action.decode().strip('\x00')  # 去空格
        self.md5sum = self.md5sum.decode().strip('\x00')
        self.clientfilePath = self.clientfilePath.decode().strip('\x00')
        self.serverfilePath = self.serverfilePath.decode().strip('\x00')

    def sendFile(self, clientfile, serverfile):
        if not os.path.exists(clientfile):
            print('源文件/文件夹不存在')
            return "No such file or directory"
        self.action = 'upload'
        (status, output) = subprocess.getstatusoutput("md5sum " + clientfile + " | awk '{printf $1}'")
        if status == 0:
            self.md5sum = output
        else:
            return ("md5sum error:" , status)
        self.size = os.stat(clientfile).st_size
        self.serverfilePath = serverfile
        self.clientfilePath = clientfile
        ret = self.struct_pack()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            s.send(ret)
            recv = s.recv(1024)
            if recv.decode() == 'dirNotExist':
                print("目标文件/文件夹不存在")
                return "No such file or directory"
            elif recv.decode() == 'ok':
                fo = open(clientfile, 'rb')
                while True:
                    filedata = fo.read(1024)
                    if not filedata:
                        break
                    s.send(filedata)
                fo.close()
                recv = s.recv(1024)
                if recv.decode() == 'ok':
                    print("文件传输成功")
                    s.close()
                    return 0
                else:
                    s.close()
                    return "md5sum error:md5sum is not correct!"
        except Exception as e:
            print(e)
            return "error:" + str(e)

    def recvFile(self, clientfile, serverfile):
        if not os.path.isdir(clientfile):
            filePath, fileName = os.path.split(clientfile)
        else:
            filePath = clientfile
        if not os.path.exists(filePath):
            print('本地目标文件/文件夹不存在')
            return "No such file or directory"
        self.action = 'download'
        self.clientfilePath = clientfile
        self.serverfilePath = serverfile
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            ret = self.struct_pack()
            s.send(ret)
            recv = s.recv(struct.calcsize(dataFormat))
            self.struct_unpack(recv)
            if self.action.startswith("ok"):
                if os.path.isdir(clientfile):
                    fileName = (os.path.split(serverfile))[1]
                    clientfile = os.path.join(clientfile, fileName)
                self.recvd_size = 0
                file = open(clientfile, 'wb')
                while not self.recvd_size == self.size:
                    if self.size - self.recvd_size > 1024:
                        rdata = s.recv(1024)
                        self.recvd_size += len(rdata)
                    else:
                        rdata = s.recv(self.size - self.recvd_size)
                        self.recvd_size = self.size
                    file.write(rdata)
                file.close()
                print('\n等待校验...')
                (status, output) = subprocess.getstatusoutput("md5sum " + clientfile + " | awk '{printf $1}'")
                if output == self.md5sum:
                    print("文件传输成功")
                else:
                    print("文件校验不通过")
                    (status, output) = subprocess.getstatusoutput("rm " + clientfile)
            elif self.action.startswith("nofile"):
                print('远程源文件/文件夹不存在')
                return "No such file or directory"
        except Exception as e:
            print(e)
            return "error:" + str(e)


serverIp = '127.0.0.1'  # 也可以是guest和host之间
serverPort = 12345
serverAddr = (serverIp, serverPort)

fileclient = fileClient(serverAddr)
#fileclient.sendFile(r'D:\chaodawenjian.txt', r'D:\\xin.txt')
fileclient.recvFile(r'D:\\xin.txt', r'D:\chaodawenjian.txt')
