import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout, QPushButton
)
from PySide6.QtCore import QStringListModel, Slot
from pandas_model2 import PandasModel
from textedit_delegate import TextEditDelegate
from item_window_with_mapper import ItemWindow


class MainWindow(QWidget):
    def __init__(self, model, type_model):
        super().__init__()
        self.model = model
        self.type_model = type_model

        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        # self.setGeometry(100, 100, 580, 300)
        self.resize(580, 300)
        self.setWindowTitle("Test View")
        self.setupMainWindow()
        self.show()

    def setupMainWindow(self):
        """Create and arrange widgets in the main window"""
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # set up delegate and apply it to the column
        self.model.set_editable_cols([1])
        delegate = TextEditDelegate(self.table_view)
        # delegate = LabelDelegate(view)
        self.table_view.setItemDelegateForColumn(1, delegate)

        # set up view
        # self.table_view.resize(550, 400)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        # manual column width setting should be done after setHorizontalHeader()
        self.table_view.resizeColumnsToContents()
        # view.setColumnWidth(1, 300)

        item_button = QPushButton('Item View')
        item_button.clicked.connect(self.display_item_view)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table_view)
        vbox.addWidget(item_button)
        self.setLayout(vbox)

    @Slot()
    def display_item_view(self):
        self.item_window = ItemWindow(self.model, self.type_model)
        self.item_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    type_names = ["Home", "Work", "Other"]
    type_model = QStringListModel(type_names)

    data_dict = {}
    data_dict['Names'] = ['Alice', 'Bob', 'Carol', 'Donald', 'Emma']
    data_dict['Addresses'] = [
        "<qt>123 Main Street<br/>Market Town</qt>",
        "<qt>PO Box 32<br/>Mail Handling Service"
        "<br/>Service City</qt>",
        "<qt>The Lighthouse<br/>Remote Island</qt>",
        "<qt>47338 Park Avenue<br/>Big City</qt>",
        "<qt>Research Station<br/>Base Camp<br/>Big Mountain</qt>"
    ]
    data_dict['Types'] = ["0", "1", "2", "0", "2"]
    test_df = pd.DataFrame(data_dict)

    model = PandasModel(test_df)
    window = MainWindow(model, type_model)

    sys.exit(app.exec())