import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        self.center()
        self.show()

    def center(self):
        # qr stores the info about the window size, position..
        qr = self.frameGeometry()
        # find out the center of the screen
        cp = QDesktopWidget().availableGeometry().center()
        # set the position of qr to cp
        qr.moveCenter(cp)
        # move the window to a new qr
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())