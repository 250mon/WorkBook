import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QLineEdit
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette


class ScheduleSlot(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.initUI()

    def initUI(self):
        self.setFixedSize(QSize(100, 50))
        self.layout = QVBoxLayout()

        self.label = QLabel(self.time)
        self.textbox = QLineEdit(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textbox)
        self.setLayout(self.layout)

    def set_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(color))
        self.setAutoFillBackground(True)
        self.setPalette(palette)


class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.times = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]

        self.layout = QGridLayout()

        for col, day in enumerate(self.days):
            day_label = QLabel(day)
            self.layout.addWidget(day_label, 0, col + 1)

        for row, time in enumerate(self.times):
            time_label = QLabel(time)
            self.layout.addWidget(time_label, row + 1, 0)

        self.slots = {}
        for col, day in enumerate(self.days):
            for row, time in enumerate(self.times):
                slot = ScheduleSlot(time)
                self.slots[(day, time)] = slot
                self.layout.addWidget(slot, row + 1, col + 1)

        self.setLayout(self.layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weekly Schedule Manager')

        self.layout = QVBoxLayout()

        self.schedule_widget = ScheduleWidget()
        self.layout.addWidget(self.schedule_widget)

        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
