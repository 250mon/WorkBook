import sys
from typing import List
from PySide6.QtWidgets import (
    QApplication, QWidget, QComboBox,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QDataWidgetMapper, QGridLayout
)
from PySide6.QtCore import Qt, QAbstractItemModel, QStringListModel
from PySide6.QtGui import QCloseEvent, QStandardItem, QStandardItemModel


class ItemWindow(QWidget):
    def __init__(self,
                 model: QAbstractItemModel,
                 type_model: QStringListModel,
                 parent=None):
        super().__init__(parent)
        self.model = model

        self.nameLabel = QLabel("Name:")
        self.nameLineEdit = QLineEdit()

        self.addressLabel = QLabel("Address:")
        self.addressTextEdit = QTextEdit()

        self.typeLabel = QLabel("Type:")
        self.typeComboBox = QComboBox()
        self.typeComboBox.setModel(type_model)

        self.nextButton = QPushButton("&Next")
        self.previousButton = QPushButton("&Previous")

        self.okButton = QPushButton("&Ok")
        self.cancelButton = QPushButton("&Cancel")

        self.nameLabel.setBuddy(self.nameLineEdit)
        self.addressLabel.setBuddy(self.addressTextEdit)
        self.typeLabel.setBuddy(self.typeComboBox)

        self.addMapper()

        self.save_flag = False

        self.initializeUI()

    def addMapper(self):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.nameLineEdit, 0)
        self.mapper.addMapping(self.addressTextEdit, 1)
        self.mapper.addMapping(self.typeComboBox, 2, b'currentIndex')

        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)
        self.mapper.currentIndexChanged.connect(self.updateButtons)

        self.okButton.clicked.connect(self.ok_clicked)
        self.cancelButton.clicked.connect(self.cancel_clicked)

        self.mapper.toFirst()

    def updateButtons(self, row):
        self.previousButton.setEnabled(row > 0)
        self.nextButton.setEnabled(row < self.model.rowCount() - 1)

    def ok_clicked(self):
        self.save_flag = True
        self.close()

    def cancel_clicked(self):
        self.save_flag = False
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.save_flag:
            pass
        else:
            pass
        super().closeEvent(event)

    def initializeUI(self):
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.okButton, Qt.AlignTop)
        vbox1.addWidget(self.cancelButton)
        vbox1.addStretch()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.previousButton)
        hbox1.addWidget(self.nextButton)

        gridbox = QGridLayout()
        gridbox.addWidget(self.nameLabel, 0, 0, 1, 1)
        gridbox.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        gridbox.addWidget(self.addressLabel, 1, 0, 1, 1)
        gridbox.addWidget(self.addressTextEdit, 1, 1, 1, 1)
        gridbox.addLayout(vbox1, 1, 2, 1, 1)
        gridbox.addWidget(self.typeLabel, 2, 0, 1, 1, Qt.AlignTop)
        gridbox.addWidget(self.typeComboBox, 2, 1, 1, 1)
        gridbox.addLayout(hbox1, 3, 1, 1, 1)

        self.setLayout(gridbox)
        self.setWindowTitle("Address Book")

def setupModels():
    items = ["Home", "Work", "Other"]
    type_model = QStringListModel(items)

    model = QStandardItemModel(5, 3)
    names = ['Alice', 'Bob', 'Carol', 'Donald', 'Emma']
    addresses = [
        "<qt>123 Main Street<br/>Market Town</qt>",
        "<qt>PO Box 32<br/>Mail Handling Service"
        "<br/>Service City</qt>",
        "<qt>The Lighthouse<br/>Remote Island</qt>",
        "<qt>47338 Park Avenue<br/>Big City</qt>",
        "<qt>Research Station<br/>Base Camp<br/>Big Mountain</qt>"
    ]
    types = ["0", "1", "2", "0", "2"]

    for row in range(5):
        item = QStandardItem(names[row])
        model.setItem(row, 0, item)
        item = QStandardItem(addresses[row])
        model.setItem(row, 1, item)
        item = QStandardItem(types[row])
        model.setItem(row, 2, item)

    return model, type_model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model, type_model =  setupModels()
    window = ItemWindow(model, type_model)
    window.show()
    sys.exit(app.exec())