import sys
import pandas as pd
from typing import List
from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QStringListModel
from textedit_delegate import TextEditDelegate
from item_window_with_mapper import ItemWindow
from label_delegate import LabelDelegate


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.editable_cols = []
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole) -> str or None:
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        # for widget mapper
        elif role == Qt.EditRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole) -> str or None:
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None

    def flags(self, index: QModelIndex):
        if index.column() in self.editable_cols:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        # return Qt.NoItemFlags

    def set_editable_cols(self, cols: List):
        self.editable_cols = cols

    def setData(self,
                index: QModelIndex,
                value: str,
                role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self._dataframe.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    type_names = ["Home", "Work", "Other"]
    type_model = QStringListModel(type_names)

    data_dict = {}
    data_dict['names'] = ['Alice', 'Bob', 'Carol', 'Donald', 'Emma']
    data_dict['addresses'] = [
        "<qt>123 Main Street<br/>Market Town</qt>",
        "<qt>PO Box 32<br/>Mail Handling Service"
        "<br/>Service City</qt>",
        "<qt>The Lighthouse<br/>Remote Island</qt>",
        "<qt>47338 Park Avenue<br/>Big City</qt>",
        "<qt>Research Station<br/>Base Camp<br/>Big Mountain</qt>"
    ]
    data_dict['types'] = ["0", "1", "2", "0", "2"]
    test_df = pd.DataFrame(data_dict)
    model = PandasModel(test_df)

    view = QTableView()
    view.setModel(model)

    # set up delegate and apply it to the column
    model.set_editable_cols([1])
    delegate = TextEditDelegate(view)
    # delegate = LabelDelegate(view)
    view.setItemDelegateForColumn(1, delegate)

    # set up view
    view.resize(550, 400)
    view.horizontalHeader().setStretchLastSection(True)
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
    # manual column width setting should be done after setHorizontalHeader()
    view.resizeColumnsToContents()
    # view.setColumnWidth(1, 300)

    view.show()
    item_window = ItemWindow(model, type_model)

    app.exec()
