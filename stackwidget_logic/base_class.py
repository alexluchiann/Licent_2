from time import time, sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QTableWidget, QCheckBox

from Gui_Ferestre.index import Ui_MainWindow
from env.instance import OpenstackConnect


class BaseClassGui(Ui_MainWindow):
    def __init__(self, stackedWidget, page_widget, button_widget, table_widget, columns_headers=[' Check ', 'Name', 'Operating System', 'IP Address', 'Flavor']):
        super().__init__()
        self.stackedWidget = stackedWidget
        self.page_widget = page_widget
        self.button_widget = button_widget
        self.table_widget = table_widget
        self.openstack = OpenstackConnect()
        self.button_widget.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_widget))
        self.list_of_instances=self.openstack.list_All_VM()
        self.columns_headers = columns_headers


    def populate_table(self):
        self.clean_table()
        self.table_widget.setRowCount(len(self.list_of_instances))
        self.table_widget.setColumnCount(len(self.columns_headers))
        self.table_widget.setHorizontalHeaderLabels(self.columns_headers)

        self.table_widget.setColumnWidth(0, 45)
        for col, header in enumerate(self.columns_headers):
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

    def clean_table(self):
        row_to_clean=[]
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                row_to_clean.append(row)

        for row in sorted(row_to_clean, reverse=True):
            instance_name = self.table_widget.item(row, 1).text()
            self.table_widget.removeRow(row)
        sleep(2)
        print("A<A<A<AA")
