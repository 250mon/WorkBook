import sys, csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QAbstractItemView,
    QVBoxLayout, QStyledItemDelegate, QStyleOptionViewItem,
    QComboBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex, Qt, QAbstractItemModel


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.combo_box_items = ['1', '2', '3', '4', '5']

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        editor = QComboBox(parent)
        editor.addItems(self.combo_box_items)
        return editor

    def setEditorData(self,
                      editor: QComboBox,
                      index: QModelIndex) -> None:

        current_value = index.data(Qt.EditRole)
        idx = self.combo_box_items.index(current_value)
        editor.setCurrentIndex(idx)

        # combo_box_items = ['t1', 'a2', 'b5']
        # current_value = index.data(Qt.EditRole)
        # if current_value not in combo_box_items:
        #     values = [current_value] + combo_box_items
        #     editor.addItems(values)
        # else:
        #     idx = combo_box_items.index(current_value)
        #     editor.addItems(combo_box_items)
        #     editor.setCurrentIndex(idx)


    def setModelData(self,
                     editor: QComboBox,
                     model: QAbstractItemModel,
                     index: QModelIndex) -> None:
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self,
                             editor: QComboBox,
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
        self.setWindowTitle("ComboBox Delegate Example")
        self.setupMainWindow()
        self.loadCSVFile()
        self.show()

    def setupMainWindow(self):
        """Create and arrange widgets in the main window"""
        self.model = QStandardItemModel()

        table_view = QTableView()
        table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        table_view.setModel(self.model)

        delegate = ComboBoxDelegate(self)
        # table_view.setItemDelegate(delegate)
        table_view.setItemDelegateForColumn(1, delegate)

        # Set initial row and column values
        self.model.setRowCount(3)
        self.model.setColumnCount(4)

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(table_view)
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
