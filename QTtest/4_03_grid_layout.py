import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel,
    QLineEdit, QTextEdit
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Title:'),  0, 0, 1, 1)
        grid.addWidget(QLabel('Author:'), 1, 0, 1, 1)
        grid.addWidget(QLabel('Review:'), 2, 0, 1, 1)

        grid.addWidget(QLineEdit(), 0, 1, 1, 1)
        grid.addWidget(QLineEdit(), 1, 1, 1, 1)
        grid.addWidget(QTextEdit(), 2, 1, 1, 1)

        # grid.setColumnMinimumWidth(0, 20)
        # grid.setColumnMinimumWidth(1, 20)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 10)

        # grid.setRowMinimumHeight(0, 20)
        # grid.setRowMinimumHeight(1, 20)
        # grid.setRowMinimumHeight(2, 10)
        grid.setRowStretch(0, 10)
        grid.setRowStretch(1, 5)
        grid.setRowStretch(2, 5)

        self.setWindowTitle('QGridLayout')
        # self.setGeometry(300, 300, 500, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
