import sys

from PySide6.QtCore import QAbstractTableModel, QTime, QTimer, Qt, Slot
from PySide6.QtWidgets import QApplication, QTableView

"""PySide6 port of the widgets/tutorials/modelview/3_changingmodel example from Qt v6.x"""


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.timer_hit)
        self._timer.start()

    def rowCount(self, parent=None):
        return 2

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole and row == 0 and col == 0:
            return QTime.currentTime().toString()
        return None

    @Slot()
    def timer_hit(self):
        # we identify the top left cell
        top_left = self.createIndex(0, 0)
        # emit a signal to make the view reread identified data
        self.dataChanged.emit(top_left, top_left, [Qt.DisplayRole])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()
    sys.exit(app.exec())