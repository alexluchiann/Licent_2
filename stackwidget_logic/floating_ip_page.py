from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QMessageBox

from stackwidget_logic.base_class import BaseClassGui
from env.instance import OpenstackConnect

class FloatingIPPage(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.opn_network = OpenstackConnect()

    def populate_floating_ip_table(self):
        column_headers = ['Check', 'Floating IP Address', 'Fixed IP Address']
        floating_ips = [ip for ip in self.opn_network.conn.network.ips()]

        self.table_widget.setRowCount(len(floating_ips))
        self.table_widget.setColumnCount(len(column_headers))
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        self.table_widget.setColumnWidth(0, 45)
        self.table_widget.setColumnWidth(1, 650)
        self.table_widget.setColumnWidth(2, 650)

        self.floating_ip_checkboxes = []

        for row, ip in enumerate(floating_ips):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(ip.floating_ip_address))
            self.table_widget.setItem(row, 2, QTableWidgetItem(ip.fixed_ip_address or 'None'))
            self.floating_ip_checkboxes.append(checkbox)

    def refresh_floating_ip_table(self):
        floating_ips = [ip for ip in self.opn_network.list_floating_ips()]

        self.table_widget.setRowCount(len(floating_ips))
        self.table_widget.setColumnCount(3)
        self.floating_ip_checkboxes.clear()

        for row, ip in enumerate(floating_ips):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(ip.floating_ip_address))
            self.table_widget.setItem(row, 2, QTableWidgetItem(ip.fixed_ip_address or 'None'))
            self.floating_ip_checkboxes.append(checkbox)

    def delete_checked_floating_ips(self):
        checked_floating_ips = []
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                floating_ip_address = self.table_widget.item(row, 1).text()
                checked_floating_ips.append((row, floating_ip_address))

        if not checked_floating_ips:
            QMessageBox.information(None, 'No Selection', 'No floating IPs selected for deletion.')
            return

        for row, floating_ip_address in sorted(checked_floating_ips, reverse=True):
            try:
                floating_ip = self.opn_network.conn.network.find_ip(floating_ip_address)
                if floating_ip:
                    self.opn_network.conn.network.delete_ip(floating_ip)
                self.table_widget.removeRow(row)
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete floating IP {floating_ip_address}: {e}')

        self.refresh_floating_ip_table()  # Refresh the table after deletion

    def delete_all_floating_ips(self):
        if self.warning_box('floating IPs'):
            try:
                floating_ips = self.opn_network.list_floating_ips()
                for ip in floating_ips:
                    self.opn_network.conn.network.delete_ip(ip)
                self.refresh_floating_ip_table()
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete all floating IPs: {e}')

    def create_floating_ip(self):
        dialog = CreateFloatingIPDialog(self.opn_network)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            network_name = dialog.getInputs()
            try:
                self.opn_network.create_floating_ip(network_name)
                QMessageBox.information(None, 'Success', f'Floating IP created successfully.')
                self.refresh_floating_ip_table()  # Refresh the floating IP list and table after creation
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to create floating IP: {e}')


class CreateFloatingIPDialog(QtWidgets.QDialog):
    def __init__(self, opn_network, parent=None):
        super(CreateFloatingIPDialog, self).__init__(parent)
        self.setWindowTitle("Create Floating IP")
        self.opn_network = opn_network

        layout = QtWidgets.QFormLayout(self)

        self.network_combo = QtWidgets.QComboBox(self)
        self.populate_networks()


        layout.addRow("Network:", self.network_combo)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def populate_networks(self):
        external_networks = self.opn_network.conn.network.ips()
        for network in external_networks:
            self.network_combo.addItem(network.name, network.id)

    def getInputs(self):
        return self.network_combo.currentData()