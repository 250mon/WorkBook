import sys

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication, QTableView

"""PySide6 port of the widgets/tutorials/modelview/4_headers example from Qt v6.x"""


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent=None):
        return 2

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row() + 1
            column = index.column() + 1
            return f"Row{row}, Column{column}"
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ["first", "second", "third"][section]
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()
    sys.exit(app.exec())