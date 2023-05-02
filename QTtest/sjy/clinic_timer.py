import sys
import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QProgressBar,
    QLabel,
    QPushButton,
    QLineEdit,
    QDialog,
    QVBoxLayout
)
from PySide6.QtCore import Qt, QBasicTimer, Signal
from PySide6.QtGui import QKeySequence, QIntValidator, QShortcut


class CustomDialog(QDialog):

    pt_id_entered_sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__()

        self.main = parent
        self.id = None

        self.setWindowTitle("환자 ID 입력")

        self.pt_id_le = QLineEdit(self)
        self.pt_id_le.show()
        self.pt_id_le.setValidator(QIntValidator())
        self.pt_id_le.returnPressed.connect(self.pt_id_entered)
        self.pt_id_entered_sig[str].connect(parent.pt_id_lbl.setText)
        self.pt_id_entered_sig.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pt_id_le)
        self.setLayout(self.layout)

    def pt_id_entered(self):
        self.id = self.pt_id_le.text()
        self.pt_id_entered_sig.emit(self.id)

class MyWindow(QMainWindow):
    # ALARM_TIME * 100 milliseconds total
    ALARM_TIME = 2500

    def __init__(self):
        super().__init__()
        self.alarm_time = self.ALARM_TIME
        self.initUI()

    def initUI(self):
        self.pt_id_lbl = QLabel('ID', self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.pt_id_lbl.setGeometry(0, 0, 100, 10)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 0, 1500, 10)
        self.progress_bar.setTextVisible(False)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setValue(self.alarm_time)
        self.slider.valueChanged.connect(self.set_alarm_time_percent)
        self.slider.setGeometry(0, 10, 250, 10)

        self.time_label = QLabel(f'Alarm time: {self.time_set_str()}', self)
        self.time_label.setGeometry(300, 10, 200, 12)

        self.pt_id_btn = QPushButton('Pt_ID', self)
        # self.pt_id_btn.clicked.connect(CustomDialog().exec)
        self.pt_id_btn.clicked.connect(self.show_dialog)
        self.pt_id_btn.setGeometry(0, 20, 250, 20)

        self.start_btn = QPushButton('Start', self)
        self.start_btn.clicked.connect(self.start)
        self.start_btn.setGeometry(250, 20, 250, 20)

        self.restart_btn = QPushButton('Restart', self)
        self.restart_btn.clicked.connect(self.restart)
        self.restart_btn.setGeometry(500, 20, 250, 20)

        # Hide the window title and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 1500, 40)

        # Shortcuts
        # start/stop and restart
        self.id_sc = QShortcut(QKeySequence('I'), self)
        self.id_sc.activated.connect(self.show_dialog)
        self.id_sc.activated.connect(self.reset)
        self.start_sc = QShortcut(QKeySequence('S'), self)
        self.start_sc.activated.connect(self.start)
        self.restart_sc = QShortcut(QKeySequence('R'), self)
        self.restart_sc.activated.connect(self.restart)
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
        self.restart_btn.setVisible(visible)
        if visible:
            self.setGeometry(0, 0, 1500, 40)
        else:
            self.setGeometry(0, 0, 1500, 10)

    def show_dialog(self):
        dlg = CustomDialog(self)
        if dlg.exec():
            print('success')
        else:
            print('cancel')

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
            # print(f'{self.alarm_time}s starting')
            self.timer.start(self.alarm_time, self)
            self.slider.setEnabled(False)
            self.start_btn.setText('Stop')
            self.set_visible(False)

    def restart(self):
        self.reset()
        self.start()

    def reset(self):
        if self.timer.isActive():
            # print('in run.. stopping')
            self.timer.stop()
        self.step = 0
        self.start_btn.setText('Start')
        self.progress_bar.setValue(0)
        self.set_alarm_time_percent(100)

    def set_alarm_time_percent(self, val):
        self.alarm_time = val * self.ALARM_TIME // 100
        self.time_label.setText(f'Alarm time: {self.alarm_time}')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()