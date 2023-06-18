import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QDataWidgetMapper, QGridLayout, QComboBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QStringListModel


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupModel()

        self.nameLabel = QLabel("Na&me:")
        self.nameEdit = QLineEdit()
        self.addressLabel = QLabel("&Address:")
        self.addressEdit = QTextEdit()
        self.typeLabel = QLabel("&Type:")
        self.typeComboBox = QComboBox()

        self.nextButton = QPushButton("&Next")
        self.previousButton = QPushButton("&Previous")
        self.newButton = QPushButton("&New")

        self.nameLabel.setBuddy(self.nameEdit)
        self.addressLabel.setBuddy(self.addressEdit)
        self.typeLabel.setBuddy(self.typeComboBox)

        self.typeComboBox.setModel(self.typeModel)

        self.addMapper()
        self.initializeUI()


    def setupModel(self):
        items = ["Home", "Work", "Other"]
        self.typeModel = QStringListModel(items)

        self.model = QStandardItemModel(5, 3, self)
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
            self.model.setItem(row, 0, item)
            item = QStandardItem(addresses[row])
            self.model.setItem(row, 1, item)
            item = QStandardItem(types[row])
            self.model.setItem(row, 2, item)


    def addMapper(self):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.nameEdit, 0)
        self.mapper.addMapping(self.addressEdit, 1)
        self.mapper.addMapping(self.typeComboBox, 2, b'currentIndex')

        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)
        self.newButton.clicked.connect(self.mapper.toNext)
        self.mapper.currentIndexChanged.connect(self.updateButtons)

    def updateButtons(self, row):
        self.previousButton.setEnabled(row > 0)
        self.nextButton.setEnabled(row < self.model.rowCount() - 1)

    def initializeUI(self):
        layout = QGridLayout()
        layout.addWidget(self.nameLabel, 0, 0, 1, 1)
        layout.addWidget(self.nameEdit, 0, 1, 1, 1)
        layout.addWidget(self.previousButton, 0, 2, 1, 1)
        layout.addWidget(self.addressLabel, 1, 0, 1, 1)
        layout.addWidget(self.addressEdit, 1, 1, 2, 1)
        layout.addWidget(self.nextButton, 1, 2, 1, 1)
        layout.addWidget(self.typeLabel, 3, 0, 1, 1)
        layout.addWidget(self.typeComboBox, 3, 1, 1, 1)
        layout.addWidget(self.newButton, 2, 2, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Combo Widget Mapper")
        self.mapper.toFirst()

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
