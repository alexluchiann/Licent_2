from PyQt5 import QtWidgets
from PySide2.QtWidgets import QTableWidget

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
        self.populate_table()

    def populate_table(self):
        list_of_instances = self.openstack.list_All_VM()
        self.table_widget.clear()
        column_headers = ['Name', 'Operating System', 'Flavor', 'IP Address']
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        for row, VM in enumerate(list_of_instances[::-1]):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(VM.name)))
