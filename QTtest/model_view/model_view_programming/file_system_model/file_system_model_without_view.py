import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileSystemModel, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QDir, QModelIndex


class FileSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model.directoryLoaded.connect(self.onDirectoryLoaded)

    def onDirectoryLoaded(self, directory):
        parentIndex: QModelIndex = self.model.index(directory)
        numRows = self.model.rowCount((parentIndex))
        for row in range(numRows):
            index = self.model.index(row, 0, parentIndex)
            text = str(self.model.data(index, Qt.DisplayRole))

            # Display the text in a widget
            label = QLabel(text, self)
            self.layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSystem()
    window.show()
    app.exec()