import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QRadioButton, QHBoxLayout,
    QGroupBox, QGridLayout
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        groupbox = QGroupBox('Select One:')
        rbtn1 = QRadioButton('First Button', self)
        rbtn2 = QRadioButton(self)
        rbtn2.setText('Second Button')
        rbtn1.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addWidget(rbtn1)
        hbox.addWidget(rbtn2)
        groupbox.setLayout(hbox)

        grid = QGridLayout()
        grid.addWidget(groupbox, 0, 0)
        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QRadioButton')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())