import sys
import json
from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QAbstractListModel
from PySide6.QtGui import Qt
from PySide6.QtUiTools import QUiLoader


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

class MainWindow(QMainWindow):
    def __init__(self, ui):
        super().__init__()
        # self.setupUi(self)
        self.model = TodoModel()
        self.ui = ui
        self.initUi()

    def initUi(self):
        self.ui.todoView.setModel(self.model)
        self.ui.addButton.pressed.connect(self.add)
        self.ui.deleteButton.pressed.connect(self.delete)
        self.ui.completeButton.pressed.connect(self.complete)
        self.ui.show()

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.ui.todoEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.ui.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.ui.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.ui.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.ui.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.ui.todoView.clearSelection()
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
        self.ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = QUiLoader()
    ui = loader.load("todo_window.ui", None)
    window = MainWindow(ui)
    app.exec()
