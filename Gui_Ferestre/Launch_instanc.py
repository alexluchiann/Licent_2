# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Launch_instanc.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Launch_instances(object):
    def setupUi(self, Launch_instances):
        Launch_instances.setObjectName("Launch_instances")
        Launch_instances.resize(1557, 901)
        self.centralwidget = QtWidgets.QWidget(Launch_instances)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1551, 861))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1551, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setGeometry(QtCore.QRect(0, 50, 1551, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.instances_name = QtWidgets.QLineEdit(self.widget)
        self.instances_name.setGeometry(QtCore.QRect(10, 100, 281, 31))
        self.instances_name.setObjectName("instances_name")
        self.instnaces_description = QtWidgets.QLineEdit(self.widget)
        self.instnaces_description.setGeometry(QtCore.QRect(10, 170, 281, 31))
        self.instnaces_description.setObjectName("instnaces_description")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(30, 76, 251, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 251, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(10, 220, 251, 21))
        self.label_4.setObjectName("label_4")
        self.table_Imagess = QtWidgets.QTableWidget(self.widget)
        self.table_Imagess.setGeometry(QtCore.QRect(320, 80, 591, 761))
        self.table_Imagess.setObjectName("table_Imagess")
        self.table_Imagess.setColumnCount(0)
        self.table_Imagess.setRowCount(0)
        self.table_network = QtWidgets.QTableWidget(self.widget)
        self.table_network.setGeometry(QtCore.QRect(930, 80, 591, 401))
        self.table_network.setObjectName("table_network")
        self.table_network.setColumnCount(0)
        self.table_network.setRowCount(0)
        self.table_flavor = QtWidgets.QTableWidget(self.widget)
        self.table_flavor.setGeometry(QtCore.QRect(940, 510, 581, 331))
        self.table_flavor.setObjectName("table_flavor")
        self.table_flavor.setColumnCount(0)
        self.table_flavor.setRowCount(0)
        self.Launch_instances_btn = QtWidgets.QPushButton(self.widget)
        self.Launch_instances_btn.setGeometry(QtCore.QRect(10, 460, 281, 41))
        self.Launch_instances_btn.setStyleSheet("background-color: rgb(28, 113, 216);\n"
"color: rgb(255, 255, 255);\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/Icons/upload_15414468.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Launch_instances_btn.setIcon(icon)
        self.Launch_instances_btn.setIconSize(QtCore.QSize(28, 28))
        self.Launch_instances_btn.setObjectName("Launch_instances_btn")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView.setGeometry(QtCore.QRect(70, 300, 121, 111))
        self.graphicsView.setObjectName("graphicsView")
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setGeometry(QtCore.QRect(10, 240, 281, 31))
        self.spinBox.setObjectName("spinBox")
        Launch_instances.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Launch_instances)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1557, 22))
        self.menubar.setObjectName("menubar")
        Launch_instances.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Launch_instances)
        self.statusbar.setObjectName("statusbar")
        Launch_instances.setStatusBar(self.statusbar)

        self.retranslateUi(Launch_instances)
        QtCore.QMetaObject.connectSlotsByName(Launch_instances)

    def retranslateUi(self, Launch_instances):
        _translate = QtCore.QCoreApplication.translate
        Launch_instances.setWindowTitle(_translate("Launch_instances", "MainWindow"))
        self.label.setText(_translate("Launch_instances", "            Launch Instance"))
        self.label_2.setText(_translate("Launch_instances", "Instance Name"))
        self.label_3.setText(_translate("Launch_instances", "Description"))
        self.label_4.setText(_translate("Launch_instances", "Number of instnaces"))
        self.Launch_instances_btn.setText(_translate("Launch_instances", "Launch Instance"))
import resources_rc
