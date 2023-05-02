import sys
import time
from PySide6.QtCore import Qt, QObject, QThread, pyqtSignal
from PySide6.QtWidgets import (
    QApplication,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class frmMain(QWidget):
    def __init__(self):
        super().__init__()
        self.btStart = QPushButton('Start')
        self.btStop = QPushButton('Stop')
        self.counter = QSpinBox()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btStart)
        self.layout.addWidget(self.btStop)
        self.layout.addWidget(self.counter)
        self.setLayout(self.layout)
        self.btStart.clicked.connect(self.start_thread)
        self.btStop.clicked.connect(self.stop_thread)

    def stop_thread(self):
        self.th.stop()

    def loopfunction(self, x):
        self.counter.setValue(x)

    def start_thread(self):
        self.th = thread(2)
        self.th.loop.connect(self.loopfunction)
        self.th.setTerminationEnabled(True)
        self.th.start()

class thread(QThread):
    loop = pyqtSignal(int)

    def __init__(self, x):
        QThread.__init__(self)
        self.x = x

    def run(self):
        for i in range(100):
            self.x = i
            self.loop.emit(self.x)
            print(i)
            time.sleep(1)

    def stop(self):
        self.terminate()


app = QApplication(sys.argv)
win = frmMain()

win.show()
sys.exit(app.exec())