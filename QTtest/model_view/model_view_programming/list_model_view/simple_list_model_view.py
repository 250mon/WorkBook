import sys
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QApplication, QListView, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


class MyListModel(QAbstractListModel):
    def __init__(self, *args, data_df=pd.DataFrame(), **kwargs):
        super(MyListModel, self).__init__(*args, **kwargs)
        self.data_df = data_df

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> object:
        if role == Qt.DisplayRole:
            data_row = self.data_df.values[index.row()]
            text = f"{data_row[1]} {data_row[2]}:\t\t{data_row[0]} "
            return text

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.data_df.shape[0]


class MyListWidget(QWidget):
    def __init__(self, data_df: pd.DataFrame, parent=None):
        super().__init__()
        self.parent = parent
        self.model = MyListModel()
        self.initUi()
        self.load(data_df)

    def initUi(self):
        self.setWindowTitle("My List View")
        self.list_view = QListView()

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.pressed.connect(self.delete)

        self.okButton = QPushButton("OK")
        self.okButton.pressed.connect(self.save)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.pressed.connect(self.terminate)

        hbox = QHBoxLayout()
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list_view)
        vbox.addWidget(self.deleteButton)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(600, 800)

    def delete(self):
        indexes = self.list_view.selectedIndexes()
        if indexes:
            int_indexes = [index.row() for index in indexes]
            # Remove the item and refresh.
            self.model.data_df.drop(pd.Index(int_indexes), inplace=True)
            self.model.data_df.reset_index(inplace=True, drop=True)
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.list_view.clearSelection()

    def load(self, data_df=None):
        if data_df is not None:
            data_df.reset_index(inplace=True, drop=True)
            self.model.data_df = data_df
        self.list_view.setModel(self.model)
        self.model.layoutChanged.emit()

    def save(self):
        # save routine
        self.close()

    def terminate(self):
        self.model.data_df = pd.DataFrame()
        self.close()


if __name__ == "__main__":
    raw_data = {'col0': [1, 2, 3, 4],
                'col1': [10, 20, 30, 40],
                'col2': [1000, 2000, 3000, 4000]}
    data = pd.DataFrame(raw_data)

    app = QApplication(sys.argv)
    window = MyListWidget(data)
    window.show()
    app.exec()
