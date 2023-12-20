import sys
from PySide6.QtCore import (
    QCoreApplication, QMetaObject, QRect, Qt, QAbstractTableModel,
    QModelIndex, QEvent
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QComboBox,
    QStatusBar, QTableView, QWidget, QItemDelegate
)

from PySide6 import QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(942, 787)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(70, 60, 781, 591))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 942, 22))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = ['one', 'two', 'three']

    def setItems(self, items):
        self.items = items

    def createEditor(self, widget, option, index):
        editor = QComboBox(widget)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor: QComboBox, index: QModelIndex):
        value = index.model().data(index, Qt.EditRole)
        if value:
            editor.setCurrentIndex(int(value))

    def setModelData(self, editor: QComboBox, model, index: QModelIndex):
        model.setData(index, editor.currentIndex(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        text = self.items[index.row()]
        option.text = text
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ItemViewItem, option, painter)


class CheckBoxDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column
     to which it's applied.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter,
                       option,
                       option.rect,
                       Qt.Unchecked if int(index.data()) == 0 else Qt.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable.
        Otherwise do nothing.
        '''
        if index.flags() != Qt.ItemIsEditable:
            return False

        if (event.type() == QEvent.MouseButtonRelease and
                event.button() == Qt.LeftButton):
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True
        return False

    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, Qt.EditRole)


class ExampleTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(ExampleTableModel, self).__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        try:
            return len(self._data[0])
        except:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                val = self._data[index.row()][index.column()]
                return str(val)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return f'Col {section}'

            if orientation == Qt.Vertical:
                return f'Row {section}'

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            if role==Qt.EditRole:
                self._data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.ItemIsEnabled

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        for n in range(count):
            self._data.insert(row + n, [None] * len(self._data[0]))

        self.endInsertRows()
        return True

    def insertColumns(self, column, count, parent=QModelIndex()):
        self.beginInsertColumns(QModelIndex(), column, column + count - 1)

        for r in range(len(self._data)):
            for c in range(count):
                self._data[r].insert(column + c, None)

        self.endInsertColumns()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)

        del self._data[row:row+count]

        self.endRemoveRows()
        return True

    def removeColumns(self, column, count, parent=QModelIndex()):
        self.beginRemoveColumns(QModelIndex(), column, column + count - 1)

        for r in range(len(self._data)):
            del self._data[r][column:column+count]

        self.endRemoveColumns()
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = ExampleTableModel([['0, 0', 0, 'one'],
                                        ['1, 0', 1, 'two'],
                                        ['2, 0', 1, 'three']])


        # when using multiple delegates, self is
        self.d1 = CheckBoxDelegate()
        self.d2 = ComboBoxDelegate()
        # HERE IS THE PROBLEM - I can comment either one of the two following lines and the script runs as expected.
        # but I cannot run both lines:
        self.ui.tableView.setItemDelegateForColumn(1, self.d1)
        self.ui.tableView.setItemDelegateForColumn(2, self.d2)

        self.ui.tableView.setModel(self.model)



if __name__ == '__main__':
    app = QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec())