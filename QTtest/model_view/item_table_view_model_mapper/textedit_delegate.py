from PySide6.QtWidgets import QWidget, QStyledItemDelegate,\
    QStyleOptionViewItem, QTextEdit
from PySide6.QtCore import QModelIndex, Qt, QAbstractItemModel


class TextEditDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        editor = QTextEdit(parent)
        editor.setAcceptRichText(True)
        return editor

    def setEditorData(self,
                      editor: QTextEdit,
                      index: QModelIndex) -> None:
        value = index.data(Qt.EditRole)
        editor.setText(value)

    def setModelData(self,
                     editor: QTextEdit,
                     model: QAbstractItemModel,
                     index: QModelIndex) -> None:
        value = editor.toPlainText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self,
                             editor: QTextEdit,
                             option: QStyleOptionViewItem,
                             index: QModelIndex) -> None:
        editor.setGeometry(option.rect)