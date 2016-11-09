import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMessageBox
from PyQt5 import uic
from PyQt5 import QtGui
from clientsocket import ClientSocket

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.pushButton.clicked.connect(self.sendLogin)
        self.lineEdit.setText("brdnlsrg@gmail.com")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setText("admin")
        
    def sendLogin(self):
        login = self.lineEdit.text();
        password = self.lineEdit_2.text()
        data = {'login': login, 'password': password}

        try:
            cli = ClientSocket()
            idDownload = cli.doConnectServer(data)
        except BaseException as exp:
            if exp.errno == 10061:
                QMessageBox.warning(self, "Connection Error", "Could not connect to remote server")
            print(exp)
        except BaseException as exp:
            print(exp)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
