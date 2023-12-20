import sys, csv
from PySide6.QtWidgets import (QApplication, QWidget,
                               QListView, QAbstractItemView, QVBoxLayout)
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtCore import QStringListModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("List View Example")
        self.setupMainWindow()
        self.show()

    def setupMainWindow(self):
        numbers = ["one", "Two", "Three", "Four", "Five"]
        list_model = QStringListModel(numbers)
        # list_model.setStringList(numbers)

        list_view = QListView()
        list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        list_view.setModel(list_model)

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(list_view)
        self.setLayout(main_v_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
