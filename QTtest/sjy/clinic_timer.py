import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QProgressBar,
    QLabel,
    QPushButton,
    QShortcut
)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QKeySequence


class MyWindow(QMainWindow):
    # ALARM_TIME * 100 milliseconds total
    ALARM_TIME = 2500

    def __init__(self):
        super().__init__()
        self.set_time = self.ALARM_TIME
        self.initUI()

    def initUI(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, 0, 1500, 10)
        self.progress_bar.setTextVisible(False)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(self.set_time)
        self.slider.valueChanged.connect(self.changeSetTime)
        self.slider.setGeometry(0, 10, 250, 10)

        self.time_label = QLabel(f'Alarm time: {self.time_set_str()}', self)
        self.time_label.setGeometry(300, 10, 200, 12)
        self.start_btn = QPushButton('Start', self)
        self.start_btn.clicked.connect(self.start)
        self.start_btn.setGeometry(0, 20, 250, 20)
        self.reset_btn = QPushButton('Reset', self)
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setGeometry(250, 20, 250, 20)

        # Hide the window title and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 1500, 40)

        # Shortcuts
        # start/stop and reset
        self.start_sc = QShortcut(QKeySequence('S'), self)
        self.start_sc.activated.connect(self.start)
        self.reset_sc = QShortcut(QKeySequence('R'), self)
        self.reset_sc.activated.connect(self.reset)
        # show or hide widgets
        self.visible = True
        self.show_widgets_sc = QShortcut(QKeySequence('Ctrl+T'), self)
        self.show_widgets_sc.activated.connect(self.toggle_visible)
        # quit the application
        self.quit_sc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quit_sc.activated.connect(QApplication.instance().quit)

        self.timer = QBasicTimer()
        self.step = 0

    def time_set_str(self):
        delta = datetime.timedelta(milliseconds=(self.ALARM_TIME * 100))
        return str(delta)

    def toggle_visible(self):
        self.visible = not self.visible
        self.set_visible(self.visible)

    def set_visible(self, visible):
        self.slider.setVisible(visible)
        self.time_label.setVisible(visible)
        self.start_btn.setVisible(visible)
        self.reset_btn.setVisible(visible)
        if visible:
            self.setGeometry(0, 0, 1500, 40)
        else:
            self.setGeometry(0, 0, 1500, 10)

    def timerEvent(self, a0: 'QTimerEvent') -> None:

        if self.step >= 100:
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
            self.set_visible(False)

    def reset(self):
        if self.timer.isActive():
            # print('in run.. stopping')
            self.timer.stop()
        self.step = 0
        self.start_btn.setText('Start')
        self.progress_bar.setValue(0)
        self.slider.setEnabled(True)
        self.changeSetTime(100)

    def changeSetTime(self, val):
        self.set_time = val * self.ALARM_TIME // 100
        self.time_label.setText(f'Alarm time: {self.set_time}')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()