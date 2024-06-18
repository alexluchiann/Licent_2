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
from stackwidget_logic.network_page import Network_page
from stackwidget_logic.router_page import Router_page
from stackwidget_logic.sec_groupe_page import SecurityGroupPage
from stackwidget_logic.floating_ip_page import FloatingIPPage

class Logic_Gui(QMainWindow, Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.conn_openstack = OpenstackConnect()
        self.os_info = Volumes_Management()
        self.setupUi(window)
        self.Launch_inst = None

        # Instance Management
        self.Instance_Peg = InstancePage(self.stackedWidget, self.page_25, self.Ansible_Layout_btn,
                                         self.tableWidget_management, self.tableWidget_management_Ansible, self.comboBox_Scripts, self.output_label)
        self.show_instances_management_btn.clicked.connect(self.show_instances_management)
        self.Delete_instance_btn_5.clicked.connect(self.Instance_Peg.delete_checked_lines_instances)
        self.Delete_All_instances_management_btn_2.clicked.connect(self.Instance_Peg.delete_checked_lines_instances)
        self.Launch_instance_btn_25.clicked.connect(self.open_launch_window)
        self.Delete_All_instances_management_btn_2.clicked.connect(self.Instance_Peg.delete_all_instances)

        # Ansible Management
        self.show_scripts_management_btn_2.clicked.connect(self.Instance_Peg.populate_table_2)
        self.Delete_Ansible_Script_btn.clicked.connect(self.Instance_Peg.delete_checked_lines_scripts)
        self.Delete_All_scripts_management_btn_3.clicked.connect(self.Instance_Peg.delete_all_scripts)
        self.Add_Ansible_Script_btn.clicked.connect(self.Instance_Peg.add_ansible_scripts)
        self.Run_ANsible_Script_btn.clicked.connect(self.Instance_Peg.run_script)


        # Network Page
        self.Network_Layout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Networks_Pages))
        self.NetworkInstance = Network_page(self.stackedWidget, self.Networks_Pages_5, self.Network_Layout_btn, self.tableWidget_networks)
        self.show_networks_btn.clicked.connect(self.show_network_management)
        self.Delete_All_Network_btn.clicked.connect(self.NetworkInstance.delete_all_networks)
        self.Delete_Network_btn.clicked.connect(self.NetworkInstance.delete_checked_networks)
        self.Create_Network_btn.clicked.connect(self.NetworkInstance.create_network)

        #Router Page
        self.Router_Layout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Router_Pages))
        self.RouterInstance = Router_page(self.stackedWidget, self.Router_Pages_5, self.Router_Layout_btn,
                                         self.tableWidget_routers)
        self.show_routers_btn_2.clicked.connect(self.show_router_management)
        self.Delete_All_Router_btn_2.clicked.connect(self.RouterInstance.delete_all_routers)
        self.Delete_Router_btn.clicked.connect(self.RouterInstance.delete_checked_routers)
        self.Create_Router_btn.clicked.connect(self.RouterInstance.create_router)


        #Floating IPs
        self.Floating_IP_Layout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Floating_IP_Page))
        self.FloatingIPInstance = FloatingIPPage(self.stackedWidget, self.Floating_IP_Page, self.Floating_IP_Layout_btn,
                                                 self.tableWidget_floating_ips)
        self.show_floating_btn_3.clicked.connect(self.show_floating_ip_management)
        self.Delete_All_Floating_IP_btn_2.clicked.connect(self.FloatingIPInstance.delete_all_floating_ips)
        self.Delete__Floating_IP_btn.clicked.connect(self.FloatingIPInstance.delete_checked_floating_ips)
        self.Create_Floating_IP_btn.clicked.connect(self.FloatingIPInstance.create_floating_ip)



        #Sec groups
        self.Security_Group_Layout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        self.SecurityGroupInstance = SecurityGroupPage(self.stackedWidget, self.page, self.Security_Group_Layout_btn,
                                                       self.tableWidget_sec_grups)
        self.show_Sec_Grups_btn_4.clicked.connect(self.show_security_group_management)
        self.Delete_All_Security_Groups_btn_3.clicked.connect(self.SecurityGroupInstance.delete_all_security_groups)
        self.Delete_Security_Groups_btn_2.clicked.connect(self.SecurityGroupInstance.delete_checked_security_groups)
        self.Create_Security_Groups_btn.clicked.connect(self.SecurityGroupInstance.create_security_group)

    def show_instances_management(self):
        self.Instance_Peg.populate_table()
        self.stackedWidget.setCurrentWidget(self.page_25)

    def show_network_management(self):
        self.NetworkInstance.populate_network_table()
        self.stackedWidget.setCurrentWidget(self.Networks_Pages_5)

    def open_launch_window(self):
        self.Launch_inst = Launch_instance()
        self.Launch_inst.show()

    def show_router_management(self):
        self.RouterInstance.populate_router_table()
        self.stackedWidget.setCurrentWidget(self.Router_Pages_5)

    def show_floating_ip_management(self):
        self.FloatingIPInstance.populate_floating_ip_table()
        self.stackedWidget.setCurrentWidget(self.Floating_IP_Page)

    def show_security_group_management(self):
        self.SecurityGroupInstance.populate_security_group_table()
        self.stackedWidget.setCurrentWidget(self.page)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindowss = QtWidgets.QMainWindow()
    ui = Logic_Gui(MainWindowss)
    MainWindowss.show()
    app.exec_()
