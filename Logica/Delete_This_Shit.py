import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from your_design import Ui_MainWindow  # Import the generated UI file

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to their respective functions
        self.ui.button1.clicked.connect(lambda: self.display_table(0))
        self.ui.button2.clicked.connect(lambda: self.display_table(1))
        self.ui.button3.clicked.connect(lambda: self.display_table(2))

        # Setup initial table views
        self.setup_tables()

    def setup_tables(self):
        # Table 1 setup
        table1 = QTableWidget(5, 3)  # Example table with 5 rows and 3 columns
        for i in range(5):
            for j in range(3):
                table1.setItem(i, j, QTableWidgetItem(f"Item {i+1}-{j+1}"))
        self.ui.stackedWidget.addWidget(table1)

        # Table 2 setup
        table2 = QTableWidget(3, 2)
        for i in range(3):
            for j in range(2):
                table2.setItem(i, j, QTableWidgetItem(f"Item {i+1}-{j+1}"))
        self.ui.stackedWidget.addWidget(table2)

        # Table 3 setup
        table3 = QTableWidget(4, 4)
        for i in range(4):
            for j in range(4):
                table3.setItem(i, j, QTableWidgetItem(f"Item {i+1}-{j+1}"))
        self.ui.stackedWidget.addWidget(table3)

    def display_table(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
