import sys
from datetime import date, datetime
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QDateEdit, QVBoxLayout
from PySide6.QtCore import QDate, Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('QDateEdit')

        dateedit = QDateEdit(self)
        dateedit.setDate(QDate.currentDate())
        dateedit.setMinimumDate(QDate(1900, 1, 1))
        dateedit.setMaximumDate(QDate(2100, 12, 31))
        # dateedit.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        dateedit.dateChanged.connect(self.showDate)

        date = dateedit.date()
        self.lbl2 = QLabel()
        # default format is Qt.TextDate: “Sat May 20 1995”
        self.lbl2.setText(date.toString(format=Qt.ISODate))

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(dateedit)
        vbox.addWidget(self.lbl2)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QDateEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDate(self, q_date: QDate):
        print(f'date:{q_date} type:{type(q_date)}')
        q_date_str = q_date.toString(format=Qt.ISODate)
        self.lbl2.setText(q_date_str)

        print('Converting to python date')
        # py_date = datetime.strptime(q_date_str, "%Y-%m-%d")
        # py_date = py_date.date()

        py_date = q_date.toPython()
        print(f'pydate:{py_date} type:{type(py_date)}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
