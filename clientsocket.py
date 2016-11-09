import socket
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import threading

class ClientSocket:
    HOST = 'remote.control.server.local'
    GET = '/socket.php'
    PORT = 8000
    URL_API_LOGIN = 'http://remote.control.server.local/api/login/'

    def doConnectServer(self, dataUser):
        sock = socket.socket()

        sock.connect((self.HOST, 8000))
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
                        if command == 'vol_plus':
                            vid = os.popen("nircmd.exe changesysvolume 2000")
                        if command == 'vol_minus':
                            vid = os.popen("nircmd.exe changesysvolume -2000")
                        if command == 'gibernation':
                            vid = os.popen("shutdown /h")
                        if command == 'shutdown':
                            vid = os.popen("shutdown /s /t 0")
        t1 = threading.Thread(target=writer)

        t1.start()
        
    def getAccessToken(self, data):
        request = Request(self.URL_API_LOGIN, urlencode(data).encode())
        token = urlopen(request).read().decode()
        return token
