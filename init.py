import socket
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import threading

class OsFactory:
    def initCommand(self, command):
        if os.name == 'posix':
            if command == 'vol_plus':
                cmd = 'osascript -e "set volume output volume (output volume of (get volume settings) + 7) --100%"'
                os.system(cmd)
            if command == 'vol_minus':
                cmd = 'osascript -e "set volume output volume (output volume of (get volume settings) - 7) --100%"'
                os.system(cmd)
            if command == 'gibernation':
                print(command)
            if command == 'shutdown':
                print(command)
            if command == 'mute':
                print('mute')
        else:
            if command == 'vol_plus':
                vid = os.popen("nircmd.exe changesysvolume 2000")
            if command == 'vol_minus':
                vid = os.popen("nircmd.exe changesysvolume -2000")
            if command == 'gibernation':
                vid = os.popen("shutdown /h")
            if command == 'shutdown':
                vid = os.popen("shutdown /s /t 0")
            if command == 'mute':
                print('mute')

class ClientSocket:
    HOST = '77.87.195.66'
    GET = '/'
    PORT = 7760
    URL_API_LOGIN = 'http://control.develop-nil.com/api/get/token/'

    def doConnectServer(self, dataUser):
        sock = socket.socket()
        
        sock.connect((self.HOST, self.PORT))
        accessToken = self.getAccessToken(dataUser)
        sendStr = "GET %s HTTP/1.0\r\nHost: %s\r\nAccess-token: %s\r\n\r\n" % (
            self.GET, self.HOST, accessToken
        )

        sock.send(sendStr.encode())

        e1 = threading.Event()
        def writer():
            while True:
                try:
                    data = sock.recv(1024)
                except socket.error:
                    pass#socket.close()
                else:
                    if data:
                        options = json.loads(data.decode('utf-8'))
                        command = options['option']
                        osFactoryInstance = OsFactory()
                        osFactoryInstance.initCommand(command)
        t1 = threading.Thread(target=writer)

        t1.start()
        
    def getAccessToken(self, data):
        request = Request(self.URL_API_LOGIN, urlencode(data).encode())
        dataJson = urlopen(request).read().decode()
        return dataJson

    

client = ClientSocket()
userData = {'login': 'nil.borodulia@gmail.com', 'password': 'admin'}
idDownload = client.doConnectServer(userData)