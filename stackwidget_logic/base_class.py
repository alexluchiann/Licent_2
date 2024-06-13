from time import time, sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QTableWidget, QCheckBox, QMessageBox

from Gui_Ferestre.index import Ui_MainWindow
from env.instance import OpenstackConnect


class BaseClassGui(Ui_MainWindow):
    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__()
        self.stackedWidget = stackedWidget
        self.page_widget = page_widget
        self.button_widget = button_widget
        self.table_widget = table_widget
        self.openstack = OpenstackConnect()
        self.button_widget.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_widget))
        self.list_of_instances=self.openstack.list_All_VM()


    def warning_box(self,descript=None):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Warning')
        msg_box.setText('Are you sure you want to delete all the ' + descript + ' ?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        return_value = msg_box.exec_()

        if return_value == QMessageBox.Yes:
            print("You pressed Yes")
            return True
        else:
            print("You pressed No")
            return False

    def populate_table(self):
        columns_headers = [' Check ', 'Name', 'Operating System', 'IP Address', 'Flavor']
        self.table_widget.setRowCount(len(self.list_of_instances))
        self.table_widget.setColumnCount(len(columns_headers))
        self.table_widget.setHorizontalHeaderLabels(columns_headers)

        self.table_widget.setColumnWidth(0, 45)
        for col, header in enumerate(columns_headers):
            self.table_widget.setColumnWidth(col + 1, 350)

        for row in range(len(self.list_of_instances)):
            self.table_widget.setRowHeight(row, 40)

        for row, VM in enumerate(self.list_of_instances[::-1]):
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)

            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(VM.name)))

