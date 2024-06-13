import os
import shutil
from PyQt5.QtWidgets import QTableWidget, QCheckBox, QFileDialog, QWidget, QMessageBox, QDesktopWidget
from PyQt5 import QtWidgets

from ansible_management.ansible_management import ansible_management
from base_class import BaseClassGui


class InstancePage(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget, table_widget_2, combo_box):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.table_widget_2 = table_widget_2
        self.combo_box = combo_box
        self.ans_management = ansible_management()
        self.populate_combo_box()

    # Populate Tables
    def populate_table_2(self):
        columns_headers_2 = ['Check', 'Playbook name', 'Description']
        self.table_widget_2.setRowCount(len(self.ans_management.get_ansible_playbooks_files()))
        self.table_widget_2.setColumnCount(len(columns_headers_2))
        self.table_widget_2.setHorizontalHeaderLabels(columns_headers_2)

        self.table_widget_2.setColumnWidth(0, 45)
        self.table_widget_2.setColumnWidth(1, 450)
        self.table_widget_2.setColumnWidth(2, 910)
        for row in range(len(self.list_of_instances)):
            self.table_widget_2.setRowHeight(row, 40)

        for row in range(len(self.ans_management.get_ansible_playbooks_files())):
            checkbox = QCheckBox()
            self.table_widget_2.setCellWidget(row, 0, checkbox)
            self.table_widget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.ans_management.get_ansible_playbooks_files()[row])))

    # Delete from tables
    def delete_checked_lines_instnaces(self):
        rows_to_delete = []
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                rows_to_delete.append(row)

        for row in sorted(rows_to_delete, reverse=True):
            instance_name = self.table_widget.item(row, 1).text()
            self.openstack.delete_VM(instance_name)
            self.table_widget.removeRow(row)

    def delete_checked_lines_scripts(self):
        rows_to_delete = []
        for row in range(self.table_widget_2.rowCount()):
            checkbox = self.table_widget_2.cellWidget(row, 0)
            if checkbox.isChecked():
                rows_to_delete.append(row)

        for row in sorted(rows_to_delete, reverse=True):
            script_name = self.table_widget_2.item(row, 1).text()
            self.ans_management.delete_file_from_ansible_playbook(script_name)
            self.table_widget_2.removeRow(row)
        self.populate_combo_box()

    def delete_all_instnaces(self):
        resp = self.warning_box('instances')
        if resp is True:
            for row in range(self.table_widget.rowCount()):
                instance_name = self.table_widget.item(row, 1).text()
                self.openstack.delete_VM(instance_name)
                print(instance_name)
            self.table_widget.setRowCount(0)
        else:
            print("NU ai apasat pe nimic")
            return

    def delete_all_scripts(self):
        resp = self.warning_box('scripts')
        if resp is True:
            delete_rows = []
            for row in range(self.table_widget_2.rowCount()):
                item = self.table_widget_2.item(row, 1)
                if item is not None:
                    scripts_name = item.text()
                    delete_rows.append(row)
                    print(scripts_name)
                    self.ans_management.delete_file_from_ansible_playbook(scripts_name)
                else:
                    print(f"No script name found in row {row}")

            for row in sorted(delete_rows, reverse=True):
                self.table_widget_2.removeRow(row)

            self.table_widget.setRowCount(0)
        else:
            print("NU ai apasat pe nimic")
            return
        self.populate_combo_box()

    # Add Ansible Scripts
    def add_ansible_Scrips(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        temp_widget = QWidget()

        file_dialog = QFileDialog(temp_widget)
        file_dialog.setWindowTitle("Open Files or Project")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOptions(options)
        file_dialog.setViewMode(QFileDialog.Detail)

        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry(desktop.primaryScreen())
        dialog_rect = file_dialog.geometry()
        dialog_rect.moveCenter(screen_rect.center())
        file_dialog.setGeometry(dialog_rect)
        start_directory = os.path.expanduser('~')
        file_dialog.setDirectory(start_directory)

        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt);;Python Files (*.py);;YAML Files (*.yml *.yaml)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            print(f'Selected files or directories: {file_names}')
            if file_names is not None:
                for file in file_names:
                    if file.endswith(('.yml', '.yaml')):
                        shutil.copy(file, self.ans_management.get_right_path())
                        print(file)
                return file_names
        return []

    def populate_combo_box(self):
        self.combo_box.clear()
        for script in self.ans_management.get_ansible_playbooks_files():
            self.combo_box.addItem(script)

    def run_script(self):
        try:
            script_name = self.combo_box.currentText()
            target_script = None

            for script in self.ans_management.get_ansible_playbooks_files_path():
                if os.path.basename(script) == script_name:
                    target_script = script
                    break

            if not target_script:
                QMessageBox.warning(self.page_widget, "Warning", "Selected script not found.")
                return

            print(self.ans_management.get_inventory())
            target_instances_names = []
            for row in range(self.table_widget.rowCount()):
                checkbox = self.table_widget.cellWidget(row, 0)
                if checkbox.isChecked():
                    target_instances_names.append(self.table_widget.item(row, 1).text())

            if not target_instances_names:
                QMessageBox.warning(self.page_widget, "Warning", "No instances selected. Please select at least one instance.")
                return

            target_instances = []
            for name in target_instances_names:
                instance = self.openstack.conn.compute.find_server(name)
                if instance:
                    target_instances.append(instance)

            self.ans_management.rewrite_inventory_file(self.ans_management.get_inventory(), target_instances)
            result = self.ans_management.run_ansible_file(target_script, self.ans_management.get_inventory(), self.ans_management.get_private_key_file())
            self.display_ansible_output(result)
            self.ans_management.delete_file_content(self.ans_management.get_inventory())
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self.page_widget, "Error", f"An error occurred: {e}")

    def display_ansible_output(self, result):
        self.textBrowser_output.clear()
        if isinstance(result, str):
            self.textBrowser_output.append(result)
        else:
            for line in result.stdout:
                self.textBrowser_output.append(line)


# Example usage in your script
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = InstancePage(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
