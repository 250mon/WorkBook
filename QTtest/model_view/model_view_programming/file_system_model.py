import sys
from PySide6.QtWidgets import (
    QApplication, QSplitter, QFileSystemModel, QTreeView,
    QListView
)
from PySide6.QtCore import QDir


app = QApplication (sys.argv)
splitter = QSplitter()
model = QFileSystemModel()
model.setRootPath(QDir.currentPath())

tree_view = QTreeView(splitter)
tree_view.setModel(model)
tree_view.setRootIndex(model.index(QDir.currentPath()))

list_view = QListView(splitter)
list_view.setModel(model)
list_view.setRootIndex(model.index(QDir.currentPath()))

splitter.setWindowTitle("Two views onto the same file system model")
splitter.show()
app.exec()