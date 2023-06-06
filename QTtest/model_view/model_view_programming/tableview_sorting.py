import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

data = np.random.random((10, 3))*10 -9

app = QtWidgets.QApplication([''])


class SimpleModel(QtCore.QAbstractTableModel):

    headers = 'Col 1', 'Col 2', 'Col 3'

    def __init__(self, *args, **kwargs):
        super(SimpleModel, self).__init__(*args, **kwargs)
        table.setSortingEnabled(True)
        self.order = np.arange(data.shape[0])
        self.layoutChanged.emit()

    def rowCount(self, index=None):
        return 10

    def columnCount(self, index=None):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            col = index.column()
            row = index.row()
            return str(data[self.order[row], col])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole :
            if orientation == QtCore.Qt.Horizontal :
                return self.headers[section]
            elif orientation == QtCore.Qt.Vertical :
                return section
        return None

class SortProxyModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left_index, right_index):
        left_var = self.sourceModel().data(left_index)
        right_var = self.sourceModel().data(right_index)
        return float(left_var) < float(right_var)


table = QtWidgets.QTableView()
model = SimpleModel()
proxy = SortProxyModel()
proxy.setSourceModel(model)
table.setModel(proxy)
table.show()

# sort by row index
cornerButton = table.findChild(QtWidgets.QAbstractButton)
cornerButton.clicked.connect(lambda: proxy.sort(-1))

app.exec_()