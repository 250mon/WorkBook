import sys
from enum import Enum
from PySide6.QtCore import (
    Qt, QSortFilterProxyModel, QAbstractItemModel, QRegularExpression
)
from PySide6.QtWidgets import (
    QTreeView, QCheckBox, QLineEdit, QLabel, QComboBox, QGroupBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QStyle, QApplication
)
from PySide6.QtGui import QColor, QPalette
from create_mail_model import create_mail_model


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
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.proxy_model = QSortFilterProxyModel()
        self.source_view = QTreeView()
        self.source_view.setRootIsDecorated(False)
        self.source_view.setAlternatingRowColors(True)

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

        self.filter_pattern_line_edit.textChanged.connect(self.filter_regular_expression_changed)
        self.filter_syntax_combobox.currentIndexChanged.connect(self.filter_regular_expression_changed)
        self.filter_column_combobox.currentIndexChanged.connect(self.filter_column_changed)
        self.filter_case_sensitivity_checkbox.toggled.connect(self.filter_regular_expression_changed)
        self.sort_case_sensitivity_checkbox.toggled.connect(self.sort_changed)

        self.source_groupbox = QGroupBox("Original Model")
        self.proxy_groupbox = QGroupBox("Sorted/Filtered Model")

        self.source_layout = QHBoxLayout()
        self.source_layout.addWidget(self.source_view)
        self.source_groupbox.setLayout(self.source_layout)

        self.proxy_layout = QGridLayout()
        self.proxy_layout.addWidget(self.proxy_view, 0, 0, 1, 3)
        self.proxy_layout.addWidget(self.filter_pattern_label, 1, 0)
        self.proxy_layout.addWidget(self.filter_pattern_line_edit, 1, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_syntax_label, 2, 0)
        self.proxy_layout.addWidget(self.filter_syntax_combobox, 2, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_column_label, 3, 0)
        self.proxy_layout.addWidget(self.filter_column_combobox, 3, 1, 1, 2)
        self.proxy_layout.addWidget(self.filter_case_sensitivity_checkbox, 4, 0, 1, 2)
        self.proxy_layout.addWidget(self.sort_case_sensitivity_checkbox, 4, 2)
        self.proxy_groupbox.setLayout(self.proxy_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.source_groupbox)
        self.main_layout.addWidget(self.proxy_groupbox)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self.proxy_view.sortByColumn(1, Qt.AscendingOrder)
        self.filter_column_combobox.setCurrentIndex(1)

        self.filter_pattern_line_edit.setText("Andy:Grace")
        self.filter_case_sensitivity_checkbox.setChecked(True)
        self.sort_case_sensitivity_checkbox.setChecked(True)

    def set_source_model(self, model: QAbstractItemModel):
        self.proxy_model.setSourceModel(model)
        self.source_view.setModel(model)

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
            set_text_color(self.filter_pattern_line_edit, Qt.white) #text_color(QStyle.standardPalette()))
        else:
            self.filter_pattern_line_edit.setToolTip(regular_expression.errorString())
            self.proxy_model.setFilterRegularExpression(QRegularExpression())
            set_text_color(self.filter_pattern_line_edit, Qt.red)

    def filter_column_changed(self):
        self.proxy_model.setFilterKeyColumn(self.filter_column_combobox.currentIndex())

    def sort_changed(self):
        self.proxy_model.setSortCaseSensitivity(
            Qt.CaseSensitive if self.sort_case_sensitivity_checkbox.isChecked() else Qt.CaseInsensitive)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FilterWidget()
    window.set_source_model(create_mail_model(window))
    window.show()
    app.exec()
