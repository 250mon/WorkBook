import sys
import asyncio
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout

# Thi code NOT working

class AsyncQApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.loop = asyncio.new_event_loop()

    def exec(self):
        self.loop.run_until_complete(self.asyncio_loop())
        super().exec()

    async def asyncio_loop(self):
        while True:
            await asyncio.sleep(1)  # Update the label every 1 second
            label = self.activeWindow().findChild(QLabel, "myLabel")
            if label is not None:
                label.setText(f"Updated text")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Asyncio Example")
        self.resize(300, 200)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.q_label = QLabel("Initial text", self)
        self.q_label.setObjectName("myLabel")
        # self.q_label.setGeometry(50, 50, 200, 50)
        layout.addWidget(self.q_label, alignment=Qt.AlignmentFlag.AlignCenter)



if __name__ == '__main__':
    app = AsyncQApplication(sys.argv)
    # app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
