import struct, os
import subprocess
import socketserver

dataFormat = '8s32s100s100sl'


class fileServer(socketserver.StreamRequestHandler):
    def struct_pack(self):
        ret = struct.pack(dataFormat, self.action.encode(), self.md5sum.encode(), self.clientfilePath.encode(),
                          self.serverfilePath.encode(), self.size)
        return ret

    def struct_unpack(self, package):
        self.action, self.md5sum, self.clientfilePath, self.serverfilePath, self.size = struct.unpack(dataFormat,
                                                                                                      package)
        self.action = self.action.decode().strip('\x00')
        self.md5sum = self.md5sum.decode().strip('\x00')
        self.clientfilePath = self.clientfilePath.decode().strip('\x00')
        self.serverfilePath = self.serverfilePath.decode().strip('\x00')

    def handle(self):
        print('connected from:', self.client_address)
        fileinfo_size = struct.calcsize(dataFormat)
        self.buf = self.request.recv(fileinfo_size)
        if self.buf:
            self.struct_unpack(self.buf)
            print("get action:" + self.action)
            if self.action.startswith("upload"):
                try:
                    if os.path.isdir(self.serverfilePath):
                        fileName = (os.path.split(self.clientfilePath))[1]
                        self.serverfilePath = os.path.join(self.serverfilePath, fileName)
                    filePath, fileName = os.path.split(self.serverfilePath)
                    if not os.path.exists(filePath):
                        self.request.send(str.encode('dirNotExist'))
                    else:
                        self.request.send(str.encode('ok'))
                        recvd_size = 0
                        file = open(self.serverfilePath, 'wb')
                        while not recvd_size == self.size:
                            if self.size - recvd_size > 1024:
                                rdata = self.request.recv(1024)
                                recvd_size += len(rdata)
                            else:
                                rdata = self.request.recv(self.size - recvd_size)
                                recvd_size = self.size
                            file.write(rdata)
                        file.close()
                        (status, output) = subprocess.getstatusoutput(
                            "md5sum " + self.serverfilePath + " | awk '{printf $1}'")
                        if output == self.md5sum:
                            self.request.send(str.encode('ok'))
                        else:
                            self.request.send(str.encode('md5sum error'))
                except Exception as e:
                    print(e)
                finally:
                    self.request.close()
            elif self.action.startswith("download"):
                try:
                    if os.path.exists(self.serverfilePath):
                        (status, output) = subprocess.getstatusoutput(
                            "md5sum " + self.serverfilePath + " | awk '{printf $1}'")
                        if status == 0:
                            self.md5sum = output
                        self.action = 'ok'
                        self.size = os.stat(self.serverfilePath).st_size
                        ret = self.struct_pack()
                        self.request.send(ret)
                        fo = open(self.serverfilePath, 'rb')
                        while True:
                            filedata = fo.read(1024)
                            if not filedata:
                                break
                            self.request.send(filedata)
                        fo.close()
                    else:
                        self.action = 'nofile'
                        ret = self.struct_pack()
                        self.request.send(ret)
                except Exception as e:
                    print(e)
                finally:
                    self.request.close()


import threading
import socketserver
import time

serverIp = '127.0.0.1'
serverPort = 12345
serverAddr = (serverIp, serverPort)


class fileServerth(threading.Thread):  # 建立线程
    def __init__(self):
        threading.Thread.__init__(self)
        self.create_time = time.time()
        self.local = threading.local()

    def run(self):
        print("fileServer is running...")
        fileserver.serve_forever()


fileserver = socketserver.ThreadingTCPServer(serverAddr, fileServer)
fileserverth = fileServerth()
fileserverth.start()
