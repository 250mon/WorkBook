import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QSpinBox, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('QSpinBox', alignment=Qt.AlignmentFlag.AlignCenter)
        self.spinbox = QSpinBox(alignment=Qt.AlignmentFlag.AlignRight)
        self.spinbox.setMinimum(-10)
        self.spinbox.setMaximum(30)
        # self.spinbox.setRange(-10, 30)
        self.spinbox.setSingleStep(2)
        self.lbl2 = QLabel('0', alignment=Qt.AlignmentFlag.AlignCenter)
        self.reset_btn = QPushButton('Reset')

        self.spinbox.valueChanged.connect(self.value_changed)
        self.reset_btn.clicked.connect(self.reset_btn_clicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.spinbox)
        vbox.addWidget(self.lbl2)
        vbox.addStretch()
        vbox.addWidget(self.reset_btn)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()

        self.setLayout(hbox)

        self.setWindowTitle('QSpinBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def value_changed(self):
        self.lbl2.setText(str(self.spinbox.value()))

    def reset_btn_clicked(self):
        self.spinbox.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
