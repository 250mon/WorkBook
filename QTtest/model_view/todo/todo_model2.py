import sys
import json
from PySide6 import QtGui
from PySide6.QtWidgets import (
    QWidget, QApplication, QListView, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import QAbstractListModel
from PySide6.QtGui import Qt


tick = QtGui.QColor('green')

class TodoModel(QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.todos[index.row()]
            return text

        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick
    def rowCount(self, index):
        return len(self.todos)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        self.model = TodoModel()
        self.load()
        self.initUi()

    def initUi(self):
        self.todoView = QListView(self)
        self.todoView.setModel(self.model)

        self.todoEdit = QLineEdit()
        self.addButton = QPushButton("Add Todo")
        self.addButton.pressed.connect(self.add)

        hbox = QHBoxLayout()
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton = QPushButton("Complete")
        self.completeButton.pressed.connect(self.complete)

        hbox.addWidget(self.deleteButton)
        hbox.addWidget(self.completeButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.todoView)
        vbox.addWidget(self.todoEdit)
        vbox.addWidget(self.addButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open("data.json", "r") as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open("data.json", "w") as f:
            data = json.dump(self.model.todos, f)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
