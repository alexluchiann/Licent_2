from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QMessageBox

from stackwidget_logic.base_class import BaseClassGui
from env.group_security import security_groups_operations

class SecurityGroupPage(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.sec_groups_op = security_groups_operations()

    def populate_security_group_table(self):
        column_headers = ['Check', 'Security Group Name', 'Description']
        security_groups = [sg for sg in self.sec_groups_op.list_all_security_groups()]

        self.table_widget.setRowCount(len(security_groups))
        self.table_widget.setColumnCount(len(column_headers))
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        self.table_widget.setColumnWidth(0, 45)
        self.table_widget.setColumnWidth(1, 550)
        self.table_widget.setColumnWidth(2, 550)

        self.security_group_checkboxes = []

        for row, security_group in enumerate(security_groups):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(security_group.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(security_group.description or 'None'))
            self.security_group_checkboxes.append(checkbox)

    def refresh_security_group_table(self):
        self.sec_groups_op.network_list = list(self.sec_groups_op.conn.network.networks())
        security_groups = [sg for sg in self.sec_groups_op.list_all_security_groups()]

        self.table_widget.setRowCount(len(security_groups))
        self.table_widget.setColumnCount(3)
        self.security_group_checkboxes.clear()

        for row, security_group in enumerate(security_groups):
            self.table_widget.setRowHeight(row, 40)
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QTableWidgetItem(security_group.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(security_group.description or 'None'))
            self.security_group_checkboxes.append(checkbox)

    def delete_checked_security_groups(self):
        checked_security_groups = []
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                security_group_name = self.table_widget.item(row, 1).text()
                checked_security_groups.append((row, security_group_name))

        if not checked_security_groups:
            QMessageBox.information(None, 'No Selection', 'No security groups selected for deletion.')
            return

        for row, security_group_name in sorted(checked_security_groups, reverse=True):
            try:
                self.sec_groups_op.delete_security_groups(security_group_name)
                self.table_widget.removeRow(row)
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete security group {security_group_name}: {e}')

        self.refresh_security_group_table()  # Refresh the table after deletion

    def delete_all_security_groups(self):
        if self.warning_box('security groups'):
            try:
                security_groups = self.sec_groups_op.list_all_security_groups()
                for security_group in security_groups:
                    self.sec_groups_op.conn.network.delete_security_group(security_group.id)
                self.refresh_security_group_table()
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to delete all security groups: {e}')

    def create_security_group(self):
        dialog = CreateSecurityGroupDialog(self.sec_groups_op)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name, description = dialog.getInputs()
            try:
                self.sec_groups_op.create_security_groups(name, description)
                QMessageBox.information(None, 'Success', f'Security group {name} created successfully.')
                self.refresh_security_group_table()  # Refresh the security group list and table after creation
            except Exception as e:
                QMessageBox.critical(None, 'Error', f'Failed to create security group: {e}')


class CreateSecurityGroupDialog(QtWidgets.QDialog):
    def __init__(self, sec_groups_op, parent=None):
        super(CreateSecurityGroupDialog, self).__init__(parent)
        self.setWindowTitle("Create Security Group")
        self.sec_groups_op = sec_groups_op

        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit(self)
        self.description_edit = QtWidgets.QLineEdit(self)

        layout.addRow("Security Group Name:", self.name_edit)
        layout.addRow("Description:", self.description_edit)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def getInputs(self):
        return (
            self.name_edit.text(),
            self.description_edit.text()
        )
