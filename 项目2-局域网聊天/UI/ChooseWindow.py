# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChooseWindow(object):
    def setupUi(self, ChooseWindow):
        ChooseWindow.setObjectName("ChooseWindow")
        ChooseWindow.resize(242, 141)
        self.label_username = QtWidgets.QLabel(ChooseWindow)
        self.label_username.setGeometry(QtCore.QRect(40, 10, 161, 31))
        self.label_username.setStyleSheet("font: 17pt \"楷体\";")
        self.label_username.setAlignment(QtCore.Qt.AlignCenter)
        self.label_username.setObjectName("label_username")
        self.pushButton_create_inner_room = QtWidgets.QPushButton(ChooseWindow)
        self.pushButton_create_inner_room.setGeometry(QtCore.QRect(30, 50, 181, 23))
        self.pushButton_create_inner_room.setObjectName("pushButton_create_inner_room")
        self.pushButton = QtWidgets.QPushButton(ChooseWindow)
        self.pushButton.setGeometry(QtCore.QRect(150, 80, 61, 23))
        self.pushButton.setObjectName("pushButton")
        self.label1 = QtWidgets.QLabel(ChooseWindow)
        self.label1.setGeometry(QtCore.QRect(30, 110, 54, 21))
        self.label1.setObjectName("label1")
        self.lineEdit_inner_ip = QtWidgets.QLineEdit(ChooseWindow)
        self.lineEdit_inner_ip.setGeometry(QtCore.QRect(90, 110, 121, 20))
        self.lineEdit_inner_ip.setReadOnly(True)
        self.lineEdit_inner_ip.setObjectName("lineEdit_inner_ip")
        self.lineEdit_input = QtWidgets.QLineEdit(ChooseWindow)
        self.lineEdit_input.setGeometry(QtCore.QRect(30, 80, 113, 20))
        self.lineEdit_input.setObjectName("lineEdit_input")

        self.retranslateUi(ChooseWindow)
        QtCore.QMetaObject.connectSlotsByName(ChooseWindow)

    def retranslateUi(self, ChooseWindow):
        _translate = QtCore.QCoreApplication.translate
        ChooseWindow.setWindowTitle(_translate("ChooseWindow", "欢迎！"))
        self.label_username.setText(_translate("ChooseWindow", "你好！"))
        self.pushButton_create_inner_room.setText(_translate("ChooseWindow", "创建房间"))
        self.pushButton.setText(_translate("ChooseWindow", "加入房间"))
        self.label1.setText(_translate("ChooseWindow", "局域网IP"))
