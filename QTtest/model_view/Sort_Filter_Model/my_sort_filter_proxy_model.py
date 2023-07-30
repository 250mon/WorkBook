from PySide6.QtCore import (
    QSortFilterProxyModel, QDate, QModelIndex, Qt,
    QMetaType, QRegularExpression, QAbstractItemModel
)
from PySide6.QtWidgets import (
    QTreeView, QCheckBox, QLineEdit, QLabel, QComboBox, QGroupBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QDateEdit,
    QApplication
)
from PySide6.QtWidgets import QTreeView, QGroupBox, QVBoxLayout
from create_mail_model import create_mail_model
from basic_sort_filter_model import FilterWidget



class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.minDate = QDate()
        self.maxDate = QDate()

    def lessThan(self, left: QModelIndex, right: QModelIndex):
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        if left_data.userType() == QMetaType.QDateTime:
            return left_data.toDateTime() < right_data.toDateTime()
        else:
            email_pattern = QRegularExpression("[\\w\\.]*@[\\w\\.]*")
            left_string = left_data.toString()
            if left.column() == 1:
                match = email_pattern.match(left_string)
                if match.hasMatch():
                    left_string = match.captured(0)

            right_string = right_data.toString()
            if right.column() == 1:
                match = email_pattern.match(right_string)
                if match.hasMatch():
                    right_string = match.captured(0)
            return left_string < right_string

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        index0 = self.sourceModel().index(source_row, 0, source_parent)
        index1 = self.sourceModel().index(source_row, 1, source_parent)
        index2 = self.sourceModel().index(source_row, 2, source_parent)
        return (self.sourceModel().data(index0).toString().contains(self.filterRegularExpression())
                or self.sourceModel().data(index1).toString().contains(self.filterRegularExpression())
                or self.data_in_range(self.sourceModel().data(index2).toDate()))

    def data_in_range(self, date: QDate) -> bool:
        return ((not self.minDate.isValid() or date > self.minDate)
                and (not self.maxDate.isValid() or date < self.maxDate))

    def set_filter_minimum_date(self, date):
        self.minDate = date
        self.invalidateFilter()

    def set_filter_maximum_date(self, date):
        self.maxDate = date
        self.invalidateFilter()

    def filter_minimum_date(self) -> QDate:
        return self.minDate

    def filter_maximum_date(self) -> QDate:
        return self.maxDate


class MainWindow(QWidget):
    def __init__(self):
        self.initUI()

    def initUI(self):
        self.proxy_model = MySortFilterProxyModel(self)
        self.source_view = QTreeView()
        self.source_view.setRootIsDecorated(False)
        self.source_view.setAlternatingRowColors(True)

        self.source_layout = QVBoxLayout(self)
        self.source_layout.addWidget(self.source_view)
        self.source_group_box = QGroupBox("Original Model")
        self.source_group_box.setLayout(self.source_layout)

        self.filter_widget = FilterWidget()
        self.filter_widget.setText("Grace|Sports")
        self.filter_widget.filterChanged.connect(self.text_filter_changed)
        self.filter_pattern_label = QLabel("Filter pattern:")
        self.filter_pattern_label.setBuddy(self.filter_widget)

        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate(1970, 1, 1))
        self.from_label = QLabel("From:")
        self.from_label.setBuddy(self.from_date_edit)
        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate(2099, 12, 31))
        self.to_label = QLabel("To:")
        self.to_label.setBuddy(self.to_date_edit)
        self.filter_widget.textChanged.connect(self.text_filter_changed)
        self.from_date_edit.dateChanged.connect(self.date_filter_changed)
        self.to_date_edit.dateChanged.connect(self.date_filter_changed)

        self.proxy_view = QTreeView()
        self.proxy_view.setRootIsDecorated(False)
        self.proxy_view.setAlternatingRowColors(True)
        self.proxy_view.setModel(self.proxy_model)
        self.proxy_view.setSortingEnabled(True)
        self.proxy_view.sortByColumn(1, Qt.AscendingOrder)

        self.proxy_layout = QGridLayout()
        self.proxy_layout.addWidget(self.proxy_view, 0, 0, 1, 3)
        self.proxy_layout.addWidget(self.filter_pattern_label, 1, 0)
        self.proxy_layout.addWidget(self.filter_widget, 1, 1)
        self.proxy_layout.addWidget(self.from_label, 3, 0)
        self.proxy_layout.addWidget(self.from_date_edit, 3, 1, 1, 2)
        self.proxy_layout.addWidget(self.to_label, 4, 0)
        self.proxy_layout.addWidget(self.to_date_edit, 4, 1, 1, 2)

        self.proxy_group_box = QGroupBox("Sorted/Filtered Model")
        self.proxy_group_box.setLayout(self.proxy_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.source_group_box)
        self.main_layout.addWidget(self.proxy_group_box)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Custom Sort/Filter Model")
        self.resize(500, 450)

    def setSourceModel(self, model: QAbstractItemModel):
        self.proxy_model.setSourceModel(model)
        self.source_view.setModel(model)

        for i in range(self.proxy_model.columnCount()):
            self.proxy_view.resizeColumnToContents(i)
        for i in range(model.columnCount()):
            self.source_view.resizeColumnToContents(i)

    def textFilterChanged(self):
        s = self.filter_widget.patternSyntax()
        pattern = self.filter_widget.text()

        if s == FilterWidget.Wildcard:
            pattern = QRegularExpression.wildcardToRegularExpression(pattern)
        elif s == FilterWidget.FixedString:
            pattern = QRegularExpression.escape(pattern)
        else:

        QRegularExpression.PatternOptions
        options = QRegularExpression.NoPatternOption
        if filterWidget.caseSensitivity() == Qt.CaseInsensitive:
            options |= QRegularExpression.CaseInsensitiveOption
        regularExpression = QRegularExpression(pattern, options)
        proxyModel.setFilterRegularExpression(regularExpression)