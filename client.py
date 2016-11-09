import socket
import json
import urllib.request
import urllib3
import http.client
import os
import requests

class Client:
    HOST = 'remote.control.server.local'
    GET = '/socket.php'
    PORT = 8000
    ACCESS_TOKEN = '333'

    def doConnectServer(self):
        
        sock = socket.socket()
        sock.connect((self.HOST, 8000))
        accessToken = self.getAccessToken()
        
        
        sendStr = "GET %s HTTP/1.0\r\nHost: %s\r\nAccess-token: %s\r\n\r\n" % (
            self.GET, self.HOST, accessToken
        )

        
        sock.send(sendStr.encode())
        while True:
            
            data = sock.recv(1024)
           
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
                

        
    def getAccessToken(self):
        return self.ACCESS_TOKEN
        
#client = Client()

#idDownload = client.doConnectServer()
