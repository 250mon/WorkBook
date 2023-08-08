import sys
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QStyledItemDelegate, QComboBox,
    QTableView, QVBoxLayout, QPushButton, QApplication
)
from PySide6.QtCore import QModelIndex, Qt, QAbstractTableModel, QTime



class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_items = ["1", "2", "3"]

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            comboBox = QComboBox(parent)
            for text in self.type_items:
                comboBox.addItem(text, (index.row(), index.column()))
            return comboBox
        # no need to check for the other columns, as Qt automatically creates a
        # QLineEdit for string values and QTimeEdit for QTime values;
        return super().createEditor(parent, option, index)

    # no setEditorData() required


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def appendRowData(self, data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(data)
        self.endInsertRows()

    def data(self, index, role=Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._data[0])

    def flags(self, index):
        # allow editing of the index
        return super().flags(index) | Qt.ItemIsEditable


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        localWidget = QWidget()

        self.table = QTableView(localWidget)

        data = [["1", "Hi", QTime(2, 1)], ["2", "Hello", QTime(3, 0)]]

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.setItemDelegate(Delegate())

        self.add_row = QPushButton("Add Row", localWidget)
        self.add_row.clicked.connect(self.addRow)

        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                self.table.openPersistentEditor(index)

        layout_v = QVBoxLayout()
        layout_v.addWidget(self.table)
        layout_v.addWidget(self.add_row)
        localWidget.setLayout(layout_v)
        self.setCentralWidget(localWidget)

    def addRow(self):
        row = self.model.rowCount()

        new_row_data = ["3", "Howdy", QTime(9, 0)]
        self.model.appendRowData(new_row_data)

        for i in range(self.model.columnCount()):
            index = self.model.index(row, i)
            self.table.openPersistentEditor(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
