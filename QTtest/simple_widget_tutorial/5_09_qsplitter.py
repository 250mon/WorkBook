import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame, QSplitter
from PySide6.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        top = QFrame()
        top.setFrameShape(QFrame.Box)
        midleft = QFrame()
        midleft.setFrameShape(QFrame.StyledPanel)
        midright = QFrame()
        midright.setFrameShape(QFrame.Panel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.WinPanel)
        bottom.setFrameShadow(QFrame.Sunken)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(midleft)
        splitter1.addWidget(midright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(top)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setWindowTitle('QSplitter')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
