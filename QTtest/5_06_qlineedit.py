import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from PyQt5.QtGui import QIntValidator


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.move(60, 40)

        self.qle = QLineEdit(self)
        self.qle.setPlaceholderText("환자 ID")
        self.qle.setValidator(QIntValidator())
        self.qle.move(60, 100)
        # qle.textChanged[str].connect(self.onChanged)
        self.qle.returnPressed.connect(self.onEntered)

        self.setWindowTitle('QLineEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def onEntered(self):
        self.lbl.setText(self.qle.text())
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())