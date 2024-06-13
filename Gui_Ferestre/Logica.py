import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from Gui_Ferestre.Launch_instanc import Ui_Launch_instances

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
from stackwidget_logic.instances_page import InstancePage
from stackwidget_logic.Launch_page import Launch_instance

class Logic_Gui(QMainWindow, Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.conn_openstack = OpenstackConnect()
        self.os_info = Volumes_Management()
        self.setupUi(window)
        self.Launch_inst = None

        # Instance Management
        self.Instance_Peg = InstancePage(self.stackedWidget, self.page_25, self.Ansible_Layout_btn,
                                         self.tableWidget_management, self.tableWidget_management_Ansible,self.comboBox_Scripts)
        self.show_instances_management_btn.clicked.connect(self.show_instances_management)
        self.Delete_instance_btn_5.clicked.connect(self.Instance_Peg.delete_checked_lines_instnaces)
        self.Delete_All_instances_management_btn_2.clicked.connect(self.Instance_Peg.delete_all_instnaces)
        self.Launch_instance_btn_25.clicked.connect(self.open_launch_window)

        # Ansible Management
        self.show_scripts_management_btn_2.clicked.connect(self.Instance_Peg.populate_table_2)
        self.Delete_Ansible_Script_btn.clicked.connect(self.Instance_Peg.delete_checked_lines_scripts)
        self.Delete_All_scripts_management_btn_3.clicked.connect(self.Instance_Peg.delete_all_scripts)
        self.Add_Ansible_Script_btn.clicked.connect(self.Instance_Peg.add_ansible_Scrips)
        self.Run_ANsible_Script_btn.clicked.connect(self.Instance_Peg.run_script)


    def show_instances_management(self):
        self.Instance_Peg.populate_table()
        self.stackedWidget.setCurrentWidget(self.page_25)

    def open_launch_window(self):
        self.Launch_inst = Launch_instance()
        self.Launch_inst.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindowss = QtWidgets.QMainWindow()
    ui = Logic_Gui(MainWindowss)
    MainWindowss.show()
    app.exec_()
