import sys, csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QAbstractItemView,
    QVBoxLayout, QStyledItemDelegate, QStyleOptionViewItem,
    QSpinBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex, Qt, QAbstractItemModel


class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    def setEditorData(self,
                      editor: QSpinBox,
                      index: QModelIndex) -> None:
        value = int(index.data(Qt.EditRole))
        editor.setValue(value)

    def setModelData(self,
                     editor: QSpinBox,
                     model: QAbstractItemModel,
                     index: QModelIndex) -> None:
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self,
                             editor: QSpinBox,
                             option: QStyleOptionViewItem,
                             index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()


    def initializeUI(self):
        """Set up the application's GUI."""
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("SpindBox Delegate Example")
        self.setupMainWindow()
        self.loadCSVFile()
        self.show()

    def setupMainWindow(self):
        """Create and arrange widgets in the main window"""
        self.model = QStandardItemModel()

        self.table_view = QTableView()
        self.table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table_view.setModel(self.model)

        self.delegate = SpinBoxDelegate(self)
        self.table_view.setItemDelegate(self.delegate)

        # Set initial row and column values
        self.model.setRowCount(3)
        self.model.setColumnCount(4)

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def loadCSVFile(self):
        """Load header and rows from CSV file."""
        file_name = "files/numbers.csv"

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            self.model.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(csv.reader(csv_f)):
                items = [QStandardItem(item) for item in row]
                self.model.insertRow(i, items)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
