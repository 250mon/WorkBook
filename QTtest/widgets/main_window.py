from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QLabel, QDockWidget
)
from PySide6.QtCore import Qt
import sys


class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()
        lbl = QLabel("Another Window")

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)

        self.setLayout(vbox)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupMainWindow()

    def setupMainWindow(self):
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.label1 = QLabel("Hello World")
        self.label2 = QLabel("God bless you")

        dock_widget1 = QDockWidget("Dock Widget1", self)
        dock_widget1.setAllowedAreas(Qt.TopDockWidgetArea)
        dock_widget1.setWidget(self.label1)
        self.addDockWidget(Qt.TopDockWidgetArea, dock_widget1)

        dock_widget2 = QDockWidget("Dock Widget2", self)
        # dock_widget2.setAllowedAreas(Qt.LeftDockWidgetArea |
        #                              Qt.RightDockWidgetArea)
        dock_widget2.setWidget(self.label2)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget2)

        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w = AnotherWindow()
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
