import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QProgressBar,
    QLabel,
    QPushButton
)
from PyQt5.QtCore import Qt, QBasicTimer


class MyWindow(QMainWindow):
    ALARM_TIME = 5000

    def __init__(self):
        super().__init__()
        self.set_time = self.ALARM_TIME
        self.initUI()

    def initUI(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, 10, 500, 5)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(self.set_time)
        self.slider.valueChanged.connect(self.changeSetTime)
        self.slider.setGeometry(0, 20, 250, 10)

        self.time_label = QLabel(f'Alarm time:{self.ALARM_TIME}', self)
        self.time_label.setGeometry(300, 20, 200, 12)
        self.start_btn = QPushButton('Start', self)
        self.start_btn.clicked.connect(self.start)
        self.start_btn.setGeometry(0, 35, 250, 20)
        self.reset_btn = QPushButton('Reset', self)
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setGeometry(250, 35, 250, 20)

        # Hide the window title and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(20, 20, 500, 60)

        self.timer = QBasicTimer()
        self.step = 0

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        if self.step >= self.set_time:
            self.timer.stop()
            self.start_btn.setText('Finished')
            return
        self.step = self.step + 1
        self.progress_bar.setValue(self.step)

    def start(self):
        if self.timer.isActive():
            # print('stopping')
            self.timer.stop()
            self.start_btn.setText('Start')
        else:
            # print(f'{self.set_time}s starting')
            self.timer.start(self.set_time, self)
            self.slider.setEnabled(False)
            self.start_btn.setText('Stop')

    def reset(self):
        if self.timer.isActive():
            # print('in run.. resetting')
            self.timer.stop()
            self.step = 0
            self.start_btn.setText('Start')
        # print('resetting ...')
        self.progress_bar.setValue(0)
        self.slider.setEnabled(True)
        self.changeSetTime(100)

    def changeSetTime(self, val):
        self.set_time = int(val * self.ALARM_TIME / 100)
        self.time_label.setText(f'Alarm time:{self.set_time}')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()