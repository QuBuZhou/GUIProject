import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.window import *




class MyWindow(QMainWindow, Ui_Form):
    res = 0
    count1 = ""
    count2 = ""
    symbol = ""
    has_symbol = False

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

    def clear(self):
        self.res = 0
        self.count2 = ""
        self.symbol = ""
        self.has_symbol = False

    def show_result(self):
        self.lineEdit.setText(str(self.res))

    def set_count(self, n):
        if not self.symbol:
            self.set_count1(n)
        else:
            self.set_count2(n)

    def set_count1(self, n):
        self.count1 += n
        self.lineEdit.setText(self.count1)

    def set_count2(self, n):
        if self.symbol == "/" and n == "0":
            return
        self.count2 += n
        self.lineEdit.setText(self.count1 + self.symbol + self.count2)

    def set_symbol(self, n):
        if self.count1 and not self.has_symbol:
            self.has_symbol = True
            self.symbol = n
            self.lineEdit.setText(self.count1 + self.symbol)

    def count_pre(self):
        if not self.count1:
            return
        self.res = int(self.count1) ** 0.5
        self.show_result()
        self.clear()

    def submit(self):
        if not self.count1 or not self.symbol or not self.count2:
            return
        self.res = eval(self.count1 + self.symbol + self.count2)
        res = str(eval(self.count1 + self.symbol + self.count2))
        self.count1 = res
        self.lineEdit.setText(res)
        self.clear()

    def set_button(self, m):
        eval(f"self.pushButton_{m}").clicked.connect(lambda: self.set_count(str(m)))

    def set_button_C(self):
        self.count1 = ""
        self.clear()
        self.lineEdit.setText("0")

    def backspace(self):
        if not self.count1:
            return
        elif self.count1 and not self.symbol:
            self.count1 = self.count1[:-1]
            self.lineEdit.setText(self.count1 if self.count1 else "0")
        elif self.symbol:
            self.has_symbol = False
            self.symbol = ""
            self.lineEdit.setText(self.count1)
        else:
            self.count2 = self.count2[:-1]
            self.lineEdit.setText(self.count1 + self.symbol + self.count2)

    def initUI(self):
        self.lineEdit.setText("0")
        for i in range(10):
            self.set_button(i)

        self.pushButton_point.clicked.connect(lambda: self.set_count("."))
        self.pushButton_plus.clicked.connect(lambda: self.set_symbol("+"))
        self.pushButton_sub.clicked.connect(lambda: self.set_symbol("-"))
        self.pushButton_time.clicked.connect(lambda: self.set_symbol("*"))
        self.pushButton_div.clicked.connect(lambda: self.set_symbol("/"))
        self.pushButton_pow.clicked.connect(lambda: self.set_symbol("**"))
        self.pushButton_pre.clicked.connect(self.count_pre)
        self.pushButton_enter.clicked.connect(self.submit)
        self.pushButton_C.clicked.connect(self.set_button_C)
        self.pushButton_backspace.clicked.connect(self.backspace)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.initUI()
    myWin.show()
    sys.exit(app.exec_())
