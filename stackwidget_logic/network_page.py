from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets

from stackwidget_logic.base_class import BaseClassGui
from env.networks_class import openstack_network_operations

class Network_page(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.opn_network = openstack_network_operations()

    def populate_network_table(self):
        column_headers = ['Check', 'Network Name', 'Subnets', 'Is external Network']
        net = [network.name for network in self.opn_network.network_list]
        external_network_names = [network.name for network in self.opn_network.list_external_netwroks()]

        self.table_widget.setRowCount(len(net))
        self.table_widget.setColumnCount(len(column_headers))
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        self.table_widget.setColumnWidth(0, 45)
        self.table_widget.setColumnWidth(1, 550)
        self.table_widget.setColumnWidth(2, 550)
        self.table_widget.setColumnWidth(3, 300)

        self.network_checkboxes = []

        for row, network_name in enumerate(net):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(network_name))
            rez = 'Yes' if network_name in external_network_names else 'No'
            self.table_widget.setItem(row, 3, QTableWidgetItem(rez))

            network = self.opn_network.conn.network.find_network(network_name)
            if network is None:
                subnet_details = ["Network not found"]
            else:
                subnet_details = []
                for subnet_id in network.subnet_ids:
                    try:
                        subnet = self.opn_network.conn.network.get_subnet(subnet_id)
                        if subnet.gateway_ip:
                            subnet_details.append(f"{subnet.name} (Gateway: {subnet.gateway_ip})")
                        else:
                            subnet_details.append(f"{subnet.name} (No Gateway IP)")
                    except Exception as e:
                        subnet_details.append(f"Subnet {subnet_id} not found")

            self.table_widget.setItem(row, 2, QTableWidgetItem(', '.join(subnet_details)))
            self.network_checkboxes.append(checkbox)

    def refresh_network_table(self):
        self.opn_network.network_list = list(self.opn_network.conn.network.networks())
        net = [network.name for network in self.opn_network.network_list]
        external_network_names = [network.name for network in self.opn_network.list_external_netwroks()]

        self.table_widget.setRowCount(len(net))
        self.table_widget.setColumnCount(4)
        self.network_checkboxes.clear()

        for row, network_name in enumerate(net):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(network_name))
            rez = 'Yes' if network_name in external_network_names else 'No'
            self.table_widget.setItem(row, 3, QTableWidgetItem(rez))

            network = self.opn_network.conn.network.find_network(network_name)
            if network is None:
                subnet_details = ["Network not found"]
            else:
                subnet_details = []
                for subnet_id in network.subnet_ids:
                    try:
                        subnet = self.opn_network.conn.network.get_subnet(subnet_id)
                        if subnet.gateway_ip:
                            subnet_details.append(f"{subnet.name} (Gateway: {subnet.gateway_ip})")
                        else:
                            subnet_details.append(f"{subnet.name} (No Gateway IP)")
                    except Exception as e:
                        subnet_details.append(f"Subnet {subnet_id} not found")

            self.table_widget.setItem(row, 2, QTableWidgetItem(', '.join(subnet_details)))
            self.network_checkboxes.append(checkbox)

    def delete_checked_networks(self):
        checked_networks = []
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                network_name = self.table_widget.item(row, 1).text()
                checked_networks.append((row, network_name))

        if not checked_networks:
            QMessageBox.information(None, 'No Selection', 'No networks selected for deletion.')
            return

        for row, network_name in sorted(checked_networks, reverse=True):
            try:
                self.opn_network.delete_network(network_name)
                self.table_widget.removeRow(row)
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete network {network_name}: {e}')

        self.refresh_network_table()  # Refresh the table after deletion

    def delete_all_networks(self):
        if self.warning_box('networks'):
            try:
                networks = self.opn_network.conn.network.networks()
                for network in networks:
                    self.opn_network.conn.network.delete_network(network.id)
                self.refresh_network_table()
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete all networks: {e}')

    def create_network(self):
        dialog = CreateNetworkDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name, description, is_shared, admin_state, subnet_name, subnet_cidr = dialog.getInputs()
            try:
                self.opn_network.create_network(name, description, is_shared, admin_state, subnet_name, subnet_cidr)
                QMessageBox.information(None, 'Success', f'Network {name} created successfully.')
                self.refresh_network_table()  # Refresh the network list and table after creation
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to create network: {e}')


class CreateNetworkDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreateNetworkDialog, self).__init__(parent)
        self.setWindowTitle("Create Network")

        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit(self)
        self.description_edit = QtWidgets.QLineEdit(self)
        self.shared_check = QtWidgets.QCheckBox(self)
        self.admin_state_check = QtWidgets.QCheckBox(self)
        self.subnet_name_edit = QtWidgets.QLineEdit(self)
        self.subnet_cidr_edit = QtWidgets.QLineEdit(self)

        layout.addRow("Network Name:", self.name_edit)
        layout.addRow("Description:", self.description_edit)
        layout.addRow("Shared:", self.shared_check)
        layout.addRow("Admin State Up:", self.admin_state_check)
        layout.addRow("Subnet Name:", self.subnet_name_edit)
        layout.addRow("Subnet CIDR:", self.subnet_cidr_edit)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def getInputs(self):
        return (
            self.name_edit.text(),
            self.description_edit.text(),
            self.shared_check.isChecked(),
            self.admin_state_check.isChecked(),
            self.subnet_name_edit.text(),
            self.subnet_cidr_edit.text()
        )