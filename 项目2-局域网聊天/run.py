from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5 import QtGui
from UI.StartWindow import Ui_StartWindow
from UI.login_window import Ui_login_window
from UI.register_window import Ui_register_window
from UI.MainWindow import Ui_MainWindow
from UI.ChooseWindow import Ui_ChooseWindow
from qtpy.QtCore import Qt
import threading
import pymysql
import socket
import sys


def connect_return(w1, w2):
    w1.close()
    w2.show()

class MyServerThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self) -> None:
        if self.thread_id == "server":
            while True:
                data = mySocket.recv(1024).decode()
                if data[:2] == "jo":
                    data = data.split("√")
                    myMainWin.ipaddr_list.append((data[1], data[2]))
                    number = len(myMainWin.ipaddr_list) - 1
                    item_ip = QTableWidgetItem(data[2])
                    item_ip.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item_name = QTableWidgetItem(data[1])
                    item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    myMainWin.tableWidget.setRowCount(myMainWin.tableWidget.rowCount() + 1)
                    myMainWin.tableWidget.setItem(number, 0, item_name)
                    myMainWin.tableWidget.setItem(number, 1, item_ip)
                    myMainWin.textbrowser_talk.append(f"——【{data[1]}】上线了——")
                    s = []
                    for n1, n2 in myMainWin.ipaddr_list:
                        s.append(f"{n1}-{n2}")
                    s = "√".join(s)
                    mySocket.sendto(f"su√{s}".encode(), (data[2], 51423))
                elif data[:2] == "ex":
                    data = data.split("√")
                    i = myMainWin.ipaddr_list.index((data[1], data[2]))
                    myMainWin.ipaddr_list.pop(i)
                    myMainWin.tableWidget.removeRow(i)
                    myMainWin.textbrowser_talk.append(f"【——{data[1]}】下线了——")

                elif data[:2] == "ms":
                    data = data.split("√")
                    myMainWin.textbrowser_talk.append(f"【{data[1]}】：{data[3]}")

                elif data[:2] == "su":
                    data = data.split("√")
                    data = data[1:]
                    for d in data:
                        d = d.split("-")
                        myMainWin.ipaddr_list.append((d[0], d[1]))
                        number = len(myMainWin.ipaddr_list) - 1
                        item_name = QTableWidgetItem(d[0])
                        item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item_ip = QTableWidgetItem(d[1])
                        item_ip.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        myMainWin.tableWidget.setRowCount(myMainWin.tableWidget.rowCount() + 1)
                        myMainWin.tableWidget.setItem(number, 0, item_name)
                        myMainWin.tableWidget.setItem(number, 1, item_ip)


class MyStartWindow(QWidget, Ui_StartWindow):
    def __init__(self, parent=None):
        super(MyStartWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_login.clicked.connect(lambda: connect_return(myStWin, myLogWin))
        self.pushButton_register.clicked.connect(lambda: connect_return(myStWin, myRegWin))


class MyLoginWindow(QWidget, Ui_login_window):
    ipaddr_list = []

    def __init__(self, parent=None):
        super(MyLoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_ok.clicked.connect(self.submit)
        self.pushButton_cancel.clicked.connect(lambda: connect_return(myLogWin, myStWin))

    def submit(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        if not username or not password:
            return
        cur.execute(f"select * from userdata where username='{username}'")
        res = cur.fetchone()
        if not res:
            QMessageBox.warning(self, "错误", "该用户名不存在！")
        elif password != res[1]:
            QMessageBox.warning(self, "错误", "密码输入错误！")
        else:
            QMessageBox.information(self, "信息", "登录成功！")
            user.username = username
            myChoWin.label_username.setText(f"你好，{user.username}！")
            myChoWin.lineEdit_inner_ip.setText(user.ip)
            myLogWin.close()
            myChoWin.show()


class MyRegisterWindow(QWidget, Ui_register_window):
    def __init__(self, parent=None):
        super(MyRegisterWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_ok.clicked.connect(self.submit)
        self.pushButton_cancel.clicked.connect(lambda: connect_return(myRegWin, myStWin))

    def submit(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        if not username or not password:
            return
        cur.execute(f"select * from userdata where username='{username}'")
        res = cur.fetchone()
        if res:
            QMessageBox.warning(self, "错误", "该用户名已存在！")
            return
        cur.execute(f"insert into userdata values('{username}', '{password}');")
        conn.commit()
        QMessageBox.information(self, "信息", "注册成功！")


class MyChooseWindow(QWidget, Ui_ChooseWindow):
    def __init__(self, parent=None):
        super(MyChooseWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_create_inner_room.clicked.connect(myMainWin.openWithServer)
        self.pushButton.clicked.connect(lambda: myMainWin.joinServer(self.lineEdit_input.text()))


class User:
    username = ""
    ip = socket.gethostbyname(socket.gethostname())


class MyMainWindow(QMainWindow, Ui_MainWindow):
    server_host_ip = ""
    ipaddr_list = []
    my_socket = None

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_submit.clicked.connect(self.submit)
        self.pushButton_clear.clicked.connect(self.clear)
        self.textEdit.textChanged.connect(self.text_changed)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        for _, ip in myMainWin.ipaddr_list:
            mySocket.sendto(f"ex√{user.username}√{user.ip}".encode(), (ip, 51423))
        mySocket.close()
        sys.exit(0)

    def text_changed(self):
        msg = self.textEdit.toPlainText()
        if '\n' in msg:
            msg = msg.replace('\n', '')
            self.textEdit.setText(msg)
            self.submit()

    def openWithServer(self):
        myChoWin.close()
        self.server_host_ip = user.ip
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ipaddr_list.append((user.username, user.ip))
        number = len(self.ipaddr_list) - 1
        self.tableWidget.setRowCount(myMainWin.tableWidget.rowCount() + 1)
        item_name = QTableWidgetItem(user.username)
        item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        item_ip = QTableWidgetItem(user.ip)
        item_ip.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidget.setItem(number, 0, item_name)
        self.tableWidget.setItem(number, 1, item_ip)
        myThread_server.start()
        self.show()

    def joinServer(self, connect_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((user.ip, 51424))
        try:
            s.sendto(f"jo√{user.username}√{user.ip}".encode(), (connect_ip, 51423))
        except Exception as res:
            QMessageBox.warning(self, "错误！", str(res))

        else:
            QMessageBox.information(self, "信息", "连接成功！")
            myChoWin.close()
            myThread_server.start()
            self.show()

    def submit(self):
        myMainWin.textbrowser_talk.append(f"【{user.username}】：{self.textEdit.toPlainText()}")
        for _, ip in self.ipaddr_list:
            text = self.textEdit.toPlainText()
            if not text:
                return
            if ip == user.ip:
                continue
            self.textbrowser_talk.append(f"【{user.username}】：{text}")
            mySocket.sendto(f"ms√{user.username}√{user.ip}√{text}".encode(), (ip, 51423))
        self.textEdit.setText("")

    def clear(self):
        self.textEdit.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = User()
    myMainWin = MyMainWindow()
    myStWin = MyStartWindow()
    myLogWin = MyLoginWindow()
    myRegWin = MyRegisterWindow()
    myChoWin = MyChooseWindow()
    conn = pymysql.connect(host='192.168.2.3', user='root', password="baihehe123", database='data')
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.bind((user.ip, 51423))
    cur = conn.cursor()
    myThread_server = MyServerThread("server")

    myStWin.show()
    sys.exit(app.exec_())
