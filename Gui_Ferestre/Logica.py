import sys
import os
from PyQt5 import QtWidgets
import time
# Add the base directory and necessary subdirectories to the system path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, 'env'))
sys.path.append(os.path.join(base_dir, 'ansible_management'))
sys.path.append(os.path.join(base_dir, 'stackwidget_logic'))

# Importing modules from the correct paths
from Gui_Ferestre.index import Ui_MainWindow
from env.instance import OpenstackConnect
from ansible_management.volumes_management import Volumes_Management
from stackwidget_logic.base_class import BaseClassGui
from stackwidget_logic.instances_page import InstancePage
from PySide2.QtWidgets import QTableWidget

#from stackwidget_logic.instances_page import
#from ui_functions import *

class Logic_Gui(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.conn_openstack = OpenstackConnect()
        self.os_info = Volumes_Management()
        self.setupUi(window)
        # self.Instances_Layout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Instances_Pages))

        #instances module
        self.Instance_Peg = InstancePage(self.stackedWidget, self.page_25, self.Launch_instance_btn_25,
                                         self.tableWidget_management)
        self.show_instances_btn.clicked.connect(self.Instance_Peg.populate_table)
        self.Delete_instance_btn.clicked.connect(self.Instance_Peg.delete_checked_lines)


        #Ansible management module
        self.base_class = BaseClassGui(self.stackedWidget, self.page_25, self.Ansible_Layout_btn,self.tableWidget_management)
        self.show_instances_management_btn.clicked.connect(self.base_class.populate_table)
        '''
        self.base_class = BaseClassGui(self.stackedWidget, self.page_25, self.Ansible_Layout_btn,
                                       self.tableWidget_management)
        self.base_class.populate_table()
        self.base_class_2 = InstancePage(self.stackedWidget, self.Instances_Pages, self.Instances_Layout_btn,
                                         self.tableWidget_instances)

        
        self.Delete_instance_btn.clicked.connect( self.base_class_2.delete_checked_lines())  # Pass the method reference without parentheses
        '''

        '''
        self.Mama = InstancePage(
            self.stackedWidget,
            self.Instances_Pages,
            self.Instances_Layout_btn,
            self.tableWidget_instances
        )
        '''
    '''
    def load_table(self):
        self.table_VM_Info.setRowCount(len(self.list_vm))
        row = 0
        for VM in self.list_vm[::-1]:
            print(VM)
            self.table_VM_Info.setItem(row, 0, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_VM_Info.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.os_info.get_os_with_instance_id(VM.id))))
            self.table_VM_Info.setItem(row, 2, QtWidgets.QTableWidgetItem(str(VM.flavor.id)))
            self.table_VM_Info.setItem(row, 3, QtWidgets.QTableWidgetItem("A"))
            self.table_VM_Info.setItem(row, 4, QtWidgets.QTableWidgetItem("B"))
            self.table_VM_Info.setItem(row, 5, QtWidgets.QTableWidgetItem("C"))
            row += 1
    '''


app = QtWidgets.QApplication(sys.argv)
MainWindowss = QtWidgets.QMainWindow()

ui = Logic_Gui(MainWindowss)

MainWindowss.show()
app.exec_()
