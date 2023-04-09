from telnetlib import Telnet
from threading import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import time

form_class=uic.loadUiType(f"./ui/ui_main.ui")[0]


class MainW(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.client=None


        self.pb_connect.clicked.connect(self.connect)
        self.pb_send.clicked.connect(self.cmd)



    def closeEvent(self, evt):
        if self.client != None:
            self.client.close()
            self.client=None

    ##############################################################

    def connect(self):
        if self.client != None:
            self.client.close()
            self.client = None

        self.client=Telnet()
        self.client.open(self.lineEdit_ip.text(),int(self.lineEdit_port.text()))
        th_read=Thread(target=self.read, args=(self.client, ), daemon=True)
        th_read.start()
        
    def read(self,client):
        sock=client.get_socket()
        while sock:
            data=sock.recv(1024).decode("ascii")
            if len(data):
                self.textBrowser.append(data)
                self.textBrowser.moveCursor(QTextCursor.End)
            else:
                break
            time.sleep(0.1)

    def cmd(self):
        cmd=self.lineEdit_cmd.text()
        self.textBrowser.append(cmd)
        self.textBrowser.moveCursor(QTextCursor.End)
        self.client.write(cmd.encode("ascii")+b"\n")
        self.lineEdit_cmd.setText("")


if __name__=="__main__":
    app=QApplication([])
    w=MainW()
    w.show()
    app.exec()
