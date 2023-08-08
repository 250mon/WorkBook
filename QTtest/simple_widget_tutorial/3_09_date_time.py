import sys
from datetime import datetime, date
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QDate, QLocale


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.qdate = QDate.currentDate()
        self.initUI()

    def initUI(self):
        locale = QLocale()
        self.statusBar().showMessage(locale.toString(self.qdate, QLocale.FormatType.LongFormat))

        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())