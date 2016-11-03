import sys
import urllib.request
import requests
import urllib3
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import socket
import json
import threading
import os

#from client import Client

class Widget(QWidget):
    HOST = 'remote.control.server.local'
    GET = '/socket.php'
    PORT = 8000
    ACCESS_TOKEN = '333'
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.pushButton.clicked.connect(self.sendLogin)
        self.lineEdit.setText("brdnlsrg@gmail.com")
        self.lineEdit_2.setText("admin")
        
    def sendLogin(self):
        login = self.lineEdit.text();
        password = self.lineEdit_2.text()
        data = {'login': login, 'password': password}
        self.sendRequest(data)
        

    def sendRequest(self, data):
        url = 'http://remote.control.server.local/api/login/'
        request = Request(url, urlencode(data).encode())
        token = urlopen(request).read().decode()
        if token:
            print(token)
            self.ACCESS_TOKEN = token
            print(self.ACCESS_TOKEN)
            #client = Client()
            try:
                idDownload = self.doConnectServer()
            except BaseException as exp:
                print(exp)  

    def doConnectServer(self):
        sock = socket.socket()
        sock.connect((self.HOST, 8000))
        #sock.setblocking(0)
        accessToken = self.getAccessToken()
        
        sendStr = "GET %s HTTP/1.0\r\nHost: %s\r\nAccess-token: %s\r\n\r\n" % (
            self.GET, self.HOST, accessToken
        )

        print(sendStr)
        
        sock.send(sendStr.encode())
        #sock.setblocking(0)

        e1 = threading.Event()
        def writer():
            while True:
                try:
                    data = sock.recv(1024)
                except socket.error: # данных нет
                    print(1)
                    pass # тут ставим код выхода
                else: # данные есть
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
        
        
                

        
    def getAccessToken(self):
        return self.ACCESS_TOKEN
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
