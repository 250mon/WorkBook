import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class ItemModel(QStandardItemModel):
    def __init__(self, df: pd.DataFrame, parent=None):
        super().__init__(df.shape[0], df.shape[1], parent)
        self._dataframe: pd.DataFrame = df
        self.conv_df_to_model()

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = ...) -> str or None:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])


    def conv_df_to_model(self):
        for row in self._dataframe.itertuples():
            print(row.Index)
            print(row.names)
            self.setItem(row.Index, 0, QStandardItem(row.names))
            self.setItem(row.Index, 1, QStandardItem(row.addresses))
            self.setItem(row.Index, 2, QStandardItem(row.types))


if __name__ == '__main__':
    app = QApplication(sys.argv)

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

    item_model = ItemModel(test_df)

    table_view = QTableView()
    table_view.setModel(item_model)
    table_view.show()

    sys.exit(app.exec())
