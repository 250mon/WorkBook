import sys, csv
from PySide6.QtWidgets import (QApplication, QWidget,
                             QTableView, QAbstractItemView, QVBoxLayout)
from PySide6.QtGui import (QStandardItemModel, QStandardItem)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()


    def initializeUI(self):
        """Set up the application's GUI."""
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("Model and View Example")
        self.setupMainWindow()
        self.loadCSVFile()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
