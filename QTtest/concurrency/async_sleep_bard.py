import sys
import asyncio
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout
)


class MyThread(QThread):
    """A thread that performs an asynchronous task."""

    finished = Signal()

    def __init__(self):
        super().__init__()
        self._task = None

    def run(self):
        """Performs the asynchronous task."""
        self._task = asyncio.run(self._do_work())
        self._task.add_done_callback(self._on_task_finished)

    async def _do_work(self):
        """An asynchronous task that simulates some work."""
        await asyncio.sleep(2)

    def _on_task_finished(self, task):
        """Called when the asynchronous task is finished."""
        self.finished.emit()


class MyWidget(QWidget):
    """A widget that displays the results of an asynchronous task."""

    def __init__(self):
        super().__init__()

        self._thread = MyThread()
        self._thread.finished.connect(self._on_thread_finished)

        self._button = QPushButton("Start")
        self._button.clicked.connect(self._start_task)

        self._label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self._button)
        layout.addWidget(self._label)

        self.setLayout(layout)

    def _start_task(self):
        """Starts the asynchronous task."""
        self._thread.start()

    def _on_thread_finished(self):
        """Called when the asynchronous task is finished."""
        self._label.setText("Task finished")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
