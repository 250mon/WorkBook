from PySide6.QtWidgets import QWidget, QStyledItemDelegate,\
    QStyleOptionViewItem, QLabel
from PySide6.QtCore import QModelIndex, Qt


class LabelDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        editor = QLabel(parent)
        return editor

    def setEditorData(self,
                      editor: QLabel,
                      index: QModelIndex) -> None:
        value = index.data(Qt.DisplayRole)
        editor.setText(value)

    def updateEditorGeometry(self,
                             editor: QLabel,
                             option: QStyleOptionViewItem,
                             index: QModelIndex) -> None:
        editor.setGeometry(option.rect)