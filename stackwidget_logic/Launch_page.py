import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QCheckBox, QTableWidgetItem, QMessageBox

# Adjusting the system path to include necessary directories
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, 'env'))
sys.path.append(os.path.join(base_dir, 'ansible_management'))
sys.path.append(os.path.join(base_dir, 'stackwidget_logic'))
sys.path.append(os.path.join(base_dir, 'Gui_Ferestre'))

# Importing necessary modules
from env.instance import OpenstackConnect
from env.networks_class import openstack_network_operations
from Gui_Ferestre.Launch_instanc import Ui_Launch_instances
from ansible_management.openstack_images_info import Openstack_images_info

class Launch_instance(QtWidgets.QMainWindow, Ui_Launch_instances):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.opn_img_info = Openstack_images_info()
        self.opn_con = OpenstackConnect()
        self.opn_net = openstack_network_operations()
        self.load_network_table()
        self.load_flavor_table()
        self.load_images_table()
        self.setup_spinBox()
        self.Launch_instances_btn.clicked.connect(self.launche_instances)

    def load_network_table(self):
        column_headers = ['Check', 'Network Name', 'Is external Network']
        net = [network.name for network in self.opn_net.network_list]
        external_network_names = [network.name for network in self.opn_net.list_external_netwroks()]

        self.table_network.setRowCount(len(net))
        self.table_network.setColumnCount(len(column_headers))
        self.table_network.setHorizontalHeaderLabels(column_headers)
        self.table_network.setColumnWidth(0, 45)
        self.table_network.setColumnWidth(1, 340)
        self.table_network.setColumnWidth(2, 150)

        self.network_checkboxes = []

        # Populate the table
        for row, network_name in enumerate(net):
            self.table_network.setRowHeight(row, 40)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.on_network_checkbox_state_change)
            self.table_network.setCellWidget(row, 0, checkbox)
            self.table_network.setItem(row, 1, QTableWidgetItem(network_name))
            rez = 'Yes' if network_name in external_network_names else 'No'
            self.table_network.setItem(row, 2, QTableWidgetItem(rez))
            self.network_checkboxes.append(checkbox)

    def on_network_checkbox_state_change(self, state):
        if state == QtCore.Qt.Checked:
            sender = self.sender()
            for checkbox in self.network_checkboxes:
                if checkbox != sender:
                    checkbox.setChecked(False)

    def get_selected_network(self):
        for row in range(self.table_network.rowCount()):
            if self.table_network.cellWidget(row, 0).isChecked():
                return self.table_network.item(row, 1).text()
        return None

    def load_flavor_table(self):
        column_headers = ['Check', 'Flavor Name', 'VCPUS', 'RAM', 'Disk']
        flavors = self.opn_img_info.flavors_list

        self.table_flavor.setRowCount(len(flavors))
        self.table_flavor.setColumnCount(len(column_headers))
        self.table_flavor.setHorizontalHeaderLabels(column_headers)
        self.table_flavor.setColumnWidth(0, 45)
        self.table_flavor.setColumnWidth(1, 150)
        self.table_flavor.setColumnWidth(2, 100)
        self.table_flavor.setColumnWidth(3, 100)
        self.table_flavor.setColumnWidth(4, 100)

        self.flavor_checkboxes = []

        for row, flavor in enumerate(flavors):
            self.table_flavor.setRowHeight(row, 40)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.on_flavor_checkbox_state_change)
            self.table_flavor.setCellWidget(row, 0, checkbox)
            self.table_flavor.setItem(row, 1, QTableWidgetItem(flavor[0]))
            self.table_flavor.setItem(row, 2, QTableWidgetItem(str(flavor[1])))
            self.table_flavor.setItem(row, 3, QTableWidgetItem(str(flavor[2])))
            self.table_flavor.setItem(row, 4, QTableWidgetItem(str(flavor[3])))
            self.flavor_checkboxes.append(checkbox)

    def on_flavor_checkbox_state_change(self, state):
        if state == QtCore.Qt.Checked:
            sender = self.sender()
            for checkbox in self.flavor_checkboxes:
                if checkbox != sender:
                    checkbox.setChecked(False)

    def get_selected_flavor(self):
        for row in range(self.table_flavor.rowCount()):
            if self.table_flavor.cellWidget(row, 0).isChecked():
                return self.table_flavor.item(row, 1).text()
        return None

    def load_images_table(self):
        column_headers = ['Check', 'Image Name', 'Updated', 'Size']
        images = self.opn_img_info.os_data

        self.table_Imagess.setRowCount(len(images))
        self.table_Imagess.setColumnCount(len(column_headers))
        self.table_Imagess.setHorizontalHeaderLabels(column_headers)
        self.table_Imagess.setColumnWidth(0, 45)
        self.table_Imagess.setColumnWidth(1, 250)
        self.table_Imagess.setColumnWidth(2, 200)
        self.table_Imagess.setColumnWidth(3, 100)

        self.image_checkboxes = []

        for row, image in enumerate(images):
            self.table_Imagess.setRowHeight(row, 40)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.on_image_checkbox_state_change)
            self.table_Imagess.setCellWidget(row, 0, checkbox)
            self.table_Imagess.setItem(row, 1, QTableWidgetItem(image[0]))

            update_date = self.opn_con.get_image_update_date(image[0])
            self.table_Imagess.setItem(row, 2, QTableWidgetItem(update_date))
            self.table_Imagess.setItem(row, 3, QTableWidgetItem(str(image[1])))
            self.image_checkboxes.append(checkbox)

    def on_image_checkbox_state_change(self, state):
        if state == QtCore.Qt.Checked:
            sender = self.sender()
            for checkbox in self.image_checkboxes:
                if checkbox != sender:
                    checkbox.setChecked(False)

    def get_selected_image(self):
        for row in range(self.table_Imagess.rowCount()):
            if self.table_Imagess.cellWidget(row, 0).isChecked():
                return self.table_Imagess.item(row, 1).text()
        return None

    def setup_spinBox(self):
        nr_vm = self.opn_con.number_of_vm()
        if nr_vm >= 10:
            self.spinBox.setRange(0, 0)
        else:
            self.spinBox.setRange(1, 10 - nr_vm)

    def convert_size_to_mb(self, size_str):
        size, unit = size_str.split()
        size = float(size)
        if unit == 'GB':
            size *= 1024
        return int(size)

    def launche_instances(self):
        name = self.instances_name.text()
        flavor = self.get_selected_flavor()
        image = self.get_selected_image()
        network = self.get_selected_network()
        desc = self.instnaces_description.text()

        error_message = ""
        if not name:
            error_message += "Instance name is required.\n"
        if not flavor:
            error_message += "Flavor is required.\n"
        if not image:
            error_message += "Image is required.\n"
        if not network:
            error_message += "Network is required.\n"

        flavor_disk_size = None
        image_size = None
        for row in range(self.table_flavor.rowCount()):
            if self.table_flavor.item(row, 1).text() == flavor:
                flavor_disk_size_str = self.table_flavor.item(row, 4).text()
                flavor_disk_size = self.convert_size_to_mb(flavor_disk_size_str)
                break
        for row in range(self.table_Imagess.rowCount()):
            if self.table_Imagess.item(row, 1).text() == image:
                image_size_str = self.table_Imagess.item(row, 3).text()
                image_size = self.convert_size_to_mb(image_size_str)
                break

        if flavor_disk_size is not None and image_size is not None and flavor_disk_size < image_size:
            error_message += f"Flavor's disk size ({flavor_disk_size} MB) is too small for the requested image ({image_size} MB).\n"

        if error_message:
            QMessageBox.critical(self, "Error", error_message)
        else:
            for inst in range(self.spinBox.value()):
                try:
                    instance = self.opn_con.add_node(name, flavor, image, network, description=desc if desc else None)
                    if instance:
                        self.opn_con.associate_floating_ip(instance)
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))
                    return

            QMessageBox.information(self, "Success", "Instances launched and floating IPs associated successfully!")
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Launch_instance()
    MainWindow.show()
    sys.exit(app.exec_())
