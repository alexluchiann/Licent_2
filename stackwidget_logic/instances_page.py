import contextlib
import os
import shutil
import io
import subprocess
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QCheckBox, QFileDialog, QWidget, QMessageBox, QDesktopWidget, QPlainTextEdit
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

    def populate_table(self):
        self.list_of_instances = self.openstack.list_All_VM()
        columns_headers = ['Check', 'Name', 'Operating System', 'IP Address', 'Flavor']
        self.table_widget.setRowCount(len(self.list_of_instances))
        self.table_widget.setColumnCount(len(columns_headers))
        self.table_widget.setHorizontalHeaderLabels(columns_headers)

        self.table_widget.setColumnWidth(0, 45)
        for col, header in enumerate(columns_headers):
            self.table_widget.setColumnWidth(col + 1, 350)

        for row in range(len(self.list_of_instances)):
            self.table_widget.setRowHeight(row, 40)

        for row, VM in enumerate(self.list_of_instances[::-1]):
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(
                str(self.ans_management.get_os_with_instance_id(VM.id))))
            private_ip, float_ip = self.openstack.get_instance_ips(VM.name)
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem("{} /{}".format(private_ip, float_ip)))
            flavor_name = self.openstack.get_instance_flavor(VM.name)
            flavor_info = next((flavor for flavor in self.ans_management.flavors_list if flavor[0] == flavor_name),
                               None)
            if flavor_info:
                flavor_text = "{} - vCPUs: {}, RAM: {}, Disk: {}".format(flavor_info[0], flavor_info[1], flavor_info[2],
                                                                         flavor_info[3])
            else:
                flavor_text = "Flavor not found"
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(flavor_text))

    def populate_table_2(self):
        columns_headers_2 = ['Check', 'Playbook name', 'Description']
        self.table_widget_2.setRowCount(0)
        self.table_widget_2.setColumnCount(len(columns_headers_2))
        self.table_widget_2.setHorizontalHeaderLabels(columns_headers_2)

        self.table_widget_2.setColumnWidth(0, 45)
        self.table_widget_2.setColumnWidth(1, 450)
        self.table_widget_2.setColumnWidth(2, 910)

        scripts_descriptions = self.ans_management.get_scripts_descriptions()
        scripts_dict = {name: desc for name, desc in scripts_descriptions}

        playbooks = self.ans_management.get_ansible_playbooks_files()

        for row, script_name in enumerate(playbooks):
            script_description = scripts_dict.get(script_name, "No description available")
            self.table_widget_2.insertRow(row)
            checkbox = QCheckBox()
            self.table_widget_2.setCellWidget(row, 0, checkbox)
            self.table_widget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(script_name)))
            self.table_widget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(script_description)))

    def delete_checked_lines_instances(self):
        rows_to_delete = [row for row in range(self.table_widget.rowCount())
                          if self.table_widget.cellWidget(row, 0).isChecked()]

        for row in sorted(rows_to_delete, reverse=True):
            instance_name = self.table_widget.item(row, 1).text()
            self.openstack.delete_VM(instance_name)
            self.table_widget.removeRow(row)
        self.refresh_instances_table()

    def delete_checked_lines_scripts(self):
        rows_to_delete = [row for row in range(self.table_widget_2.rowCount())
                          if self.table_widget_2.cellWidget(row, 0).isChecked()]

        for row in sorted(rows_to_delete, reverse=True):
            script_name = self.table_widget_2.item(row, 1).text()
            self.ans_management.delete_file_from_ansible_playbook(script_name)
            self.table_widget_2.removeRow(row)
        self.populate_combo_box()

    def delete_all_instances(self):
        if self.warning_box('instances'):
            rows_to_delete = []
            for row in range(self.table_widget.rowCount()):
                instance_name = self.table_widget.item(row, 1).text()
                print(f"Deleting instance: {instance_name}")
                try:
                    self.openstack.delete_VM(instance_name)
                    rows_to_delete.append(row)
                except Exception as e:
                    print(f"Error deleting instance {instance_name}: {e}")

            for row in sorted(rows_to_delete, reverse=True):
                self.table_widget.removeRow(row)

            print("All instances deleted successfully.")
        self.refresh_instances_table()

    def delete_all_scripts(self):
        if self.warning_box('scripts'):
            delete_rows = [row for row in range(self.table_widget_2.rowCount())
                           if self.table_widget_2.item(row, 1) is not None]

            for row in sorted(delete_rows, reverse=True):
                script_name = self.table_widget_2.item(row, 1).text()
                self.ans_management.delete_file_from_ansible_playbook(script_name)
                self.table_widget_2.removeRow(row)
            self.populate_combo_box()

    def add_ansible_scripts(self):
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
        file_dialog.setDirectory(os.path.expanduser('~'))
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt);;Python Files (*.py);;YAML Files (*.yml *.yaml)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            for file in file_names:
                if file.endswith(('.yml', '.yaml')):
                    # Prompt for script description
                    script_description, ok_desc = QtWidgets.QInputDialog.getText(
                        self.page_widget, 'Script Description', 'Enter the description of the script:')

                    if ok_desc and script_description:
                        shutil.copy(file, self.ans_management.get_right_path())

                        # Use the filename as the script name
                        script_name = os.path.basename(file)

                        # Write script name and description to the file
                        with open(os.path.join(self.ans_management.get_right_path(), 'scripts_descriptions.txt'),
                                  'a') as desc_file:
                            desc_file.write(f"{script_name}   {script_description}\n")

                        print(f"Script {script_name} added with description: {script_description}")

            return file_names
        return []

    def populate_combo_box(self):
        self.combo_box.clear()
        playbooks = self.ans_management.get_ansible_playbooks_files()
        self.combo_box.addItems(playbooks)

    def run_script(self):
        try:
            script_name = self.combo_box.currentText()
            playbooks_paths = self.ans_management.get_ansible_playbooks_files_path()
            target_script = next((script for script in playbooks_paths if os.path.basename(script) == script_name),
                                 None)

            if not target_script:
                QMessageBox.warning(self.page_widget, "Warning", "Selected script not found.")
                return

            target_instances_names = [self.table_widget.item(row, 1).text()
                                      for row in range(self.table_widget.rowCount())
                                      if self.table_widget.cellWidget(row, 0).isChecked()]

            if not target_instances_names:
                QMessageBox.warning(self.page_widget, "Warning",
                                    "No instances selected. Please select at least one instance.")
                return

            target_instances = [self.openstack.conn.compute.find_server(name) for name in target_instances_names]
            self.ans_management.rewrite_inventory_file(self.ans_management.get_inventory(), target_instances)

            success_instances = []
            failed_instances = []

            for instance in target_instances:
                floating_ip = self.ans_management.get_floating_ip_of_instance(instance.id)
                if not floating_ip:
                    failed_instances.append((instance.name, "No floating IP assigned"))
                    continue

                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    try:
                        self.ans_management.run_ansible_file(target_script, self.ans_management.get_inventory(),
                                                             self.ans_management.get_private_key_file())
                        captured_output = output_buffer.getvalue()
                        if "fatal" in captured_output or "failed" in captured_output:
                            failed_instances.append((instance.name, "Ansible script failed"))
                        else:
                            success_instances.append(instance.name)
                    except subprocess.CalledProcessError as e:
                        captured_output = output_buffer.getvalue()
                        failed_instances.append((instance.name, str(e)))

            self.ans_management.delete_file_content(self.ans_management.get_inventory())

            self.display_results(success_instances, failed_instances)

        except Exception as e:
            QMessageBox.critical(self.page_widget, "Error", f"An error occurred: {e}")

    def display_results(self, success_instances, failed_instances):
        if not failed_instances:
            result_msg = "All instances executed the Ansible script successfully."
        else:
            result_msg = "The Ansible script failed for the following instances:\n"
            for instance, reason in failed_instances:
                result_msg += f"{instance}: {reason}\n"

        msg_box = QMessageBox(self.page_widget)
        msg_box.setWindowTitle("Ansible Script Results")
        msg_box.setText(result_msg)
        msg_box.exec_()

    def refresh_instances_table(self):
        self.list_of_instances = self.openstack.list_All_VM()
        columns_headers = ['Check', 'Name', 'Operating System', 'IP Address', 'Flavor']
        self.table_widget.setRowCount(len(self.list_of_instances))
        self.table_widget.setColumnCount(len(columns_headers))
        self.table_widget.setHorizontalHeaderLabels(columns_headers)

        self.table_widget.setColumnWidth(0, 45)
        for col, header in enumerate(columns_headers):
            self.table_widget.setColumnWidth(col + 1, 350)

        for row in range(len(self.list_of_instances)):
            self.table_widget.setRowHeight(row, 40)

        for row, VM in enumerate(self.list_of_instances[::-1]):
            checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 0, checkbox)
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(VM.name)))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(
                str(self.ans_management.get_os_with_instance_id(VM.id))))
            private_ip, float_ip = self.openstack.get_instance_ips(VM.name)
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem("{} /{}".format(private_ip, float_ip)))
            flavor_name = self.openstack.get_instance_flavor(VM.name)
            flavor_info = next((flavor for flavor in self.ans_management.flavors_list if flavor[0] == flavor_name),
                               None)
            if flavor_info:
                flavor_text = "{} - vCPUs: {}, RAM: {}, Disk: {}".format(flavor_info[0], flavor_info[1], flavor_info[2],
                                                                         flavor_info[3])
            else:
                flavor_text = "Flavor not found"
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(flavor_text))
