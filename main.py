from threading import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import time
import socket

form_class=uic.loadUiType(f"./ui/ui_main.ui")[0]


class MainW(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.client=None


        self.pb_connect.clicked.connect(self.connect)
        self.pb_send.clicked.connect(self.cmd)

        self.pb_dock.clicked.connect(self.pb_func)
        self.pb_stop.clicked.connect(self.pb_func)
        self.pb_goal1.clicked.connect(self.pb_func)
        self.pb_goal2.clicked.connect(self.pb_func)



    def closeEvent(self, evt):
        if self.client != None:
            self.client.close()
            self.client=None

    ##############################################################

    def connect(self):
        if self.client != None:
            self.client.close()
            self.client = None

        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.lineEdit_ip.text(),int(self.lineEdit_port.text())))
        th_read=Thread(target=self.read, daemon=True)
        th_read.start()
        
    def read(self):
        while True:
            data=self.client.recv(1024).decode()
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
        self.client.send(cmd.encode()+b"\n\r")
        self.lineEdit_cmd.setText("")

    def pb_func(self):
        pb = self.sender().text()
        print( pb )
        self.client.send(pb.encode()+b"\n\r")



if __name__=="__main__":
    app=QApplication([])
    w=MainW()
    w.show()
    app.exec()
