import sys
from enum import Enum
from PySide6.QtCore import (
    QSortFilterProxyModel, QDate, QModelIndex, Qt, QDateTime,
    QRegularExpression, QAbstractItemModel
)
from PySide6.QtWidgets import (
    QTreeView, QCheckBox, QLineEdit, QLabel, QComboBox, QGroupBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QDateEdit,
    QApplication
)
from PySide6.QtWidgets import QTreeView, QGroupBox, QVBoxLayout
from PySide6.QtGui import QColor, QPalette
from create_mail_model import create_mail_model
from basic_sort_filter_model import MainWindow


class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.minDate = QDate()
        self.maxDate = QDate()

    def lessThan(self, left: QModelIndex, right: QModelIndex):
        left_data: str or QDateTime = self.sourceModel().data(left)
        right_data: str or QDateTime = self.sourceModel().data(right)

        if isinstance(left_data, QDateTime):
            return left_data.toDateTime() < right_data.toDateTime()
        else:
            email_pattern = QRegularExpression("[\\w\\.]*@[\\w\\.]*")
            if left.column() == 1:
                match = email_pattern.match(left_data)
                if match.hasMatch():
                    left_data = match.captured(0)

            if right.column() == 1:
                match = email_pattern.match(right_data)
                if match.hasMatch():
                    right_data = match.captured(0)
            return left_data < right_data

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        index0 = self.sourceModel().index(source_row, 0, source_parent)
        index1 = self.sourceModel().index(source_row, 1, source_parent)
        index2 = self.sourceModel().index(source_row, 2, source_parent)

        result1 = self.filterRegularExpression().match(self.sourceModel().data(index0)).hasMatch()
        result2 = self.filterRegularExpression().match(self.sourceModel().data(index1)).hasMatch()
        result3 = self.data_in_range(self.sourceModel().data(index2).qdate())
        result = (result1 or result2) and result3

        return result

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


def text_color(_palette: QPalette) -> QColor:
    return _palette.color(QPalette.Active, QPalette.Text)


def set_text_color(w: QWidget, c: QColor):
    palette = w.palette()
    if text_color(palette) != c:
        palette.setColor(QPalette.Active, QPalette.Text, c)
        w.setPalette(palette)


class Syntax(Enum):
    RegularExpression = 1
    WildCard = 2
    FixedString = 3


class FilterWidget(QWidget):
    def __init__(self, proxy_model: QSortFilterProxyModel):
        super().__init__()
        self.proxy_model = proxy_model
        self.initUI()

    def initUI(self):
        self.proxy_view = QTreeView()
        self.proxy_view.setRootIsDecorated(False)
        self.proxy_view.setAlternatingRowColors(True)
        self.proxy_view.setModel(self.proxy_model)
        self.proxy_view.setSortingEnabled(True)

        self.sort_case_sensitivity_checkbox = QCheckBox("Case sensitive sorting")
        self.filter_case_sensitivity_checkbox = QCheckBox("Case sensitive filter")

        self.filter_pattern_line_edit = QLineEdit()
        self.filter_pattern_line_edit.setClearButtonEnabled(True)
        self.filter_pattern_label = QLabel("&Filter pattern:")
        self.filter_pattern_label.setBuddy(self.filter_pattern_line_edit)

        self.filter_syntax_combobox = QComboBox()
        self.filter_syntax_combobox.addItem("Regular expression", Syntax.RegularExpression)
        self.filter_syntax_combobox.addItem("Wildcard", Syntax.WildCard)
        self.filter_syntax_combobox.addItem("Fixed string", Syntax.FixedString)
        self.filter_syntax_label = QLabel("Filter &syntax:")
        self.filter_syntax_label.setBuddy(self.filter_syntax_combobox)

        self.filter_column_combobox = QComboBox()
        self.filter_column_combobox.addItem("Subject")
        self.filter_column_combobox.addItem("Sender")
        self.filter_column_combobox.addItem("Date")
        self.filter_column_label = QLabel("Filter &column:")
        self.filter_column_label.setBuddy(self.filter_column_combobox)

        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate(1970, 1, 1))
        self.from_label = QLabel("From:")
        self.from_label.setBuddy(self.from_date_edit)

        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate(2099, 12, 31))
        self.to_label = QLabel("To:")
        self.to_label.setBuddy(self.to_date_edit)

        self.filter_pattern_line_edit.textChanged.connect(self.filter_regular_expression_changed)
        self.filter_syntax_combobox.currentIndexChanged.connect(self.filter_regular_expression_changed)
        self.filter_column_combobox.currentIndexChanged.connect(self.filter_column_changed)
        self.filter_case_sensitivity_checkbox.toggled.connect(self.filter_regular_expression_changed)
        self.sort_case_sensitivity_checkbox.toggled.connect(self.sort_changed)
        self.from_date_edit.dateChanged.connect(self.date_filter_changed)
        self.to_date_edit.dateChanged.connect(self.date_filter_changed)


        self.proxy_groupbox = QGroupBox("Sorted/Filtered Model")
        self.proxy_layout = QGridLayout(self)
        self.proxy_layout.addWidget(self.proxy_view, 0, 0, 1, 3)
        self.proxy_layout.addWidget(self.filter_pattern_label, 1, 0)
        self.proxy_layout.addWidget(self.filter_pattern_line_edit, 1, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_syntax_label, 2, 0)
        self.proxy_layout.addWidget(self.filter_syntax_combobox, 2, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_column_label, 3, 0)
        self.proxy_layout.addWidget(self.filter_column_combobox, 3, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_case_sensitivity_checkbox, 4, 0, 1, 2)
        self.proxy_layout.addWidget(self.sort_case_sensitivity_checkbox, 4, 2)
        self.proxy_layout.addWidget(self.from_label, 5, 0)
        self.proxy_layout.addWidget(self.from_date_edit, 5, 1, 1, 2)
        self.proxy_layout.addWidget(self.to_label, 6, 0)
        self.proxy_layout.addWidget(self.to_date_edit, 6, 1, 1, 2)
        self.proxy_groupbox.setLayout(self.proxy_layout)

        self.filter_layout = QVBoxLayout()
        self.filter_layout.addWidget(self.proxy_groupbox)

        self.setLayout(self.filter_layout)

        self.proxy_view.sortByColumn(1, Qt.AscendingOrder)
        self.filter_column_combobox.setCurrentIndex(1)

        self.filter_pattern_line_edit.setText("Andy:Grace")
        self.filter_case_sensitivity_checkbox.setChecked(True)
        self.sort_case_sensitivity_checkbox.setChecked(True)

    def set_source_model(self, model: QAbstractItemModel):
        self.proxy_model.setSourceModel(model)

    def filter_regular_expression_changed(self):
        s = self.filter_syntax_combobox.itemData(int(self.filter_syntax_combobox.currentIndex()))
        pattern = self.filter_pattern_line_edit.text()
        if s == Syntax.WildCard:
            pattern = QRegularExpression.wildcardToRegularExpression(pattern)
        elif s == Syntax.FixedString:
            pattern = QRegularExpression.escape(pattern)
        else:
            pass

        options: QRegularExpression.PatternOption = QRegularExpression.NoPatternOption
        if not self.filter_case_sensitivity_checkbox.isChecked():
            options |= QRegularExpression.CaseInsensitiveOption

        regular_expression = QRegularExpression(pattern, options)
        if regular_expression.isValid():
            self.filter_pattern_line_edit.setToolTip('')
            self.proxy_model.setFilterRegularExpression(regular_expression)
            set_text_color(self.filter_pattern_line_edit, Qt.black)
        else:
            self.filter_pattern_line_edit.setToolTip(regular_expression.errorString())
            self.proxy_model.setFilterRegularExpression(QRegularExpression())
            set_text_color(self.filter_pattern_line_edit, Qt.red)

    def filter_column_changed(self):
        # it is not affecting the filter result because the model's filterAcceptRow
        # takes a priority
        self.proxy_model.setFilterKeyColumn(self.filter_column_combobox.currentIndex())

    def sort_changed(self):
        self.proxy_model.setSortCaseSensitivity(
            Qt.CaseSensitive if self.sort_case_sensitivity_checkbox.isChecked() else Qt.CaseInsensitive)

    def date_filter_changed(self):
        self.proxy_model.set_filter_maximum_date(self.from_date_edit.date())
        self.proxy_model.set_filter_maximum_date(self.to_date_edit.date())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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

        self.filter_widget = FilterWidget(self.proxy_model)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.source_group_box)
        self.main_layout.addWidget(self.filter_widget)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Custom Sort/Filter Model")
        self.resize(500, 800)

    def set_source_model(self, model: QAbstractItemModel):
        self.proxy_model.setSourceModel(model)
        self.source_view.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.set_source_model(create_mail_model(window))
    window.show()
    app.exec()
