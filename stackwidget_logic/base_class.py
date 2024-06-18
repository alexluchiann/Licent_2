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

    def warning_box(self, descript=None):
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

