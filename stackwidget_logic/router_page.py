from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QMessageBox, QComboBox

from stackwidget_logic.base_class import BaseClassGui
from env.networks_class import openstack_network_operations

class Router_page(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.opn_network = openstack_network_operations()

    def populate_router_table(self):
        column_headers = ['Check', 'Router Name', 'External Network']
        routers = [router.name for router in self.opn_network.list_routers()]

        self.table_widget.setRowCount(len(routers))
        self.table_widget.setColumnCount(len(column_headers))
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        self.table_widget.setColumnWidth(0, 45)
        self.table_widget.setColumnWidth(1, 650)
        self.table_widget.setColumnWidth(2, 650)

        self.router_checkboxes = []

        for row, router_name in enumerate(routers):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(router_name))

            router = self.opn_network.conn.network.find_router(router_name)
            external_network = router.external_gateway_info['network_id'] if router and router.external_gateway_info else 'None'

            self.table_widget.setItem(row, 2, QTableWidgetItem(external_network))
            self.router_checkboxes.append(checkbox)

    def refresh_router_table(self):
        self.opn_network.network_list = list(self.opn_network.conn.network.networks())
        routers = [router.name for router in self.opn_network.list_routers()]

        self.table_widget.setRowCount(len(routers))
        self.table_widget.setColumnCount(3)
        self.router_checkboxes.clear()

        for row, router_name in enumerate(routers):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(router_name))

            router = self.opn_network.conn.network.find_router(router_name)
            external_network = router.external_gateway_info['network_id'] if router and router.external_gateway_info else 'None'

            self.table_widget.setItem(row, 2, QTableWidgetItem(external_network))
            self.router_checkboxes.append(checkbox)

    def delete_checked_routers(self):
        checked_routers = []
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                router_name = self.table_widget.item(row, 1).text()
                checked_routers.append((row, router_name))

        if not checked_routers:
            QMessageBox.information(None, 'No Selection', 'No routers selected for deletion.')
            return

        for row, router_name in sorted(checked_routers, reverse=True):
            try:
                self.opn_network.delete_router(router_name)
                self.table_widget.removeRow(row)
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete router {router_name}: {e}')

        self.refresh_router_table()

    def delete_all_routers(self):
        if self.warning_box('routers'):
            try:
                routers = self.opn_network.list_routers()
                for router in routers:
                    self.opn_network.conn.network.delete_router(router.id)
                self.refresh_router_table()
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete all routers: {e}')

    def create_router(self):
        dialog = CreateRouterDialog(self.opn_network)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name, external_network_id = dialog.getInputs()
            try:
                self.opn_network.create_router(name, external_network_id)
                QMessageBox.information(None, 'Success', f'Router {name} created successfully.')
                self.refresh_router_table()  # Refresh the router list and table after creation
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to create router: {e}')


class CreateRouterDialog(QtWidgets.QDialog):
    def __init__(self, opn_network, parent=None):
        super(CreateRouterDialog, self).__init__(parent)
        self.setWindowTitle("Create Router")
        self.opn_network = opn_network

        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit(self)
        self.external_network_id_combo = QComboBox(self)
        self.populate_external_networks()

        layout.addRow("Router Name:", self.name_edit)
        layout.addRow("External Network ID:", self.external_network_id_combo)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def populate_external_networks(self):
        external_networks = self.opn_network.list_external_netwroks()
        for network in external_networks:
            self.external_network_id_combo.addItem(network.name, network.id)

    def getInputs(self):
        return (
            self.name_edit.text(),
            self.external_network_id_combo.currentData()
        )
