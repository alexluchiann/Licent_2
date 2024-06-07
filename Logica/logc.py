import sys
import os
from PyQt5 import QtWidgets

# Add the base directory and necessary subdirectories to the system path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, 'env'))
sys.path.append(os.path.join(base_dir, 'ansible_management'))

# Importing modules from the correct paths
from Gui_Ferestre.MainWindow import Ui_MainWindow
from env.instance import OpenstackConnect
from ansible_management.volumes_management import Volumes_Management


class Logic_Gui(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.conn_openstack = OpenstackConnect()
        self.os_info = Volumes_Management()
        self.setupUi(window)
        #self.Show_VMBtn_2.clicked.connect(self.load_table)
        self.list_vm = self.conn_openstack.list_All_VM()

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
