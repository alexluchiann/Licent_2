from PyQt5.QtCore import pyqtSignal

from base_class import BaseClassGui

class InstancePage(BaseClassGui):

    def __init__(self, stackedWidget, page_widget, button_widget, table_widget):
        super().__init__(stackedWidget, page_widget, button_widget, table_widget)
        self.scripts =

    def populate_table(self):
        self.clean_table()
        self.table_widget.setRowCount(len(self.list_of_instances))
        self.table_widget.setColumnCount(len(self.columns_headers))
        self.table_widget.setHorizontalHeaderLabels(self.columns_headers)
    def delete_checked_lines_instnaces(self):
        pass


    def delete_checked_lines_instnaces(self):
        rows_to_delete=[]
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                rows_to_delete.append(row)

        for row in sorted(rows_to_delete,reverse=True):
            instance_name=self.table_widget.item(row,1).text()
            self.openstack.delete_VM(instance_name)
            self.table_widget.removeRow(row)



