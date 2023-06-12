# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import (Qt, QEvent, QObject, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow,
                               QPushButton, QVBoxLayout, QHBoxLayout, QWidget)

import asyncio
import signal
import sys

class MainWindow(QMainWindow):

    start_signal = Signal(int, int)
    done_signal = Signal(int)

    def __init__(self):
        super().__init__()

        self.count_5sec = 0
        self.count_2sec = 0
        self.id = 0

        widget = QWidget()
        self.setCentralWidget(widget)
        vbox = QVBoxLayout(widget)
        hbox = QHBoxLayout(widget)

        self.text = QLabel("5 sec wait counts: 0")
        vbox.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.text2 = QLabel("2 sec wait counts: 0")
        vbox.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignCenter)

        async_trigger = QPushButton(text="wait 5 seconds")
        async_trigger.clicked.connect(lambda: self.async_start(5))
        hbox.addWidget(async_trigger)

        async_trigger2 = QPushButton(text="wait 2 seconds")
        async_trigger2.clicked.connect(lambda: self.async_start(2))
        hbox.addWidget(async_trigger2)

        vbox.addLayout(hbox)
        self.resize(500, 200)


    @Slot(int)
    def async_start(self, wait_time):
        self.start_signal.emit(wait_time, self.id)
        self.id += 1

    async def set_text(self, wait_time, id):
        await asyncio.sleep(wait_time)
        if wait_time == 5:
            self.count_5sec += 1
            self.text.setText(f"5 sec wait counts: {self.count_5sec}")
        else:
            self.count_2sec += 1
            self.text2.setText(f"2 sec wait counts: {self.count_2sec}")
        self.done_signal.emit(wait_time, id)


class AsyncHelper(QObject):

    class ReenterQtObject(QObject):
        """ This is a QObject to which an event will be posted, allowing
            asyncio to resume when the event is handled. event.fn() is
            the next entry point of the asyncio event loop. """
        def event(self, event):
            if event.type() == QEvent.Type.User + 1:
                event.fn()
                return True
            return False

    class ReenterQtEvent(QEvent):
        """ This is the QEvent that will be handled by the ReenterQtObject.
            self.fn is the next entry point of the asyncio event loop. """
        def __init__(self, fn):
            super().__init__(QEvent.Type(QEvent.Type.User + 1))
            self.fn = fn

    def __init__(self, worker, entry):
        super().__init__()
        self.reenter_qt = self.ReenterQtObject()
        self.entry = entry
        self.loop = asyncio.new_event_loop()
        self.done = {}

        self.worker = worker
        if hasattr(self.worker, "start_signal") and isinstance(self.worker.start_signal, Signal):
            self.worker.start_signal.connect(self.on_worker_started)
        if hasattr(self.worker, "done_signal") and isinstance(self.worker.done_signal, Signal):
            self.worker.done_signal.connect(self.on_worker_done)

    @Slot(int, int)
    def on_worker_started(self, wait_time, id):
        """ To use asyncio and Qt together, one must run the asyncio
            event loop as a "guest" inside the Qt "host" event loop. """
        if not self.entry:
            raise Exception("No entry point for the asyncio event loop was set.")
        asyncio.set_event_loop(self.loop)
        # self.loop.create_task(self.entry(wait_time))
        self.loop.create_task(self.entry(wait_time, id))
        self.loop.call_soon(lambda: self.next_guest_run_schedule(id))
        self.done[id] = False  # Set this explicitly as we might want to restart the guest run.
        self.loop.run_forever()

    @Slot(int)
    def on_worker_done(self, id):
        """ When all our current asyncio tasks are finished, we must end
            the "guest run" lest we enter a quasi idle loop of switching
            back and forth between the asyncio and Qt loops. We can
            launch a new guest run by calling launch_guest_run() again. """
        self.done[id] = True

    def continue_loop(self, id):
        """ This function is called by an event posted to the Qt event
            loop to continue the asyncio event loop. """
        if not self.done[id]:
            self.loop.call_soon(lambda: self.next_guest_run_schedule(id))
            if not self.loop.is_running():
                self.loop.run_forever()

    def next_guest_run_schedule(self, id):
        """ This function serves to pause and re-schedule the guest
            (asyncio) event loop inside the host (Qt) event loop. It is
            registered in asyncio as a callback to be called at the next
            iteration of the event loop. When this function runs, it
            first stops the asyncio event loop, then by posting an event
            on the Qt event loop, it both relinquishes to Qt's event
            loop and also schedules the asyncio event loop to run again.
            Upon handling this event, a function will be called that
            resumes the asyncio event loop. """
        self.loop.stop()
        QApplication.postEvent(self.reenter_qt, self.ReenterQtEvent(self.continue_loop(id)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    async_helper = AsyncHelper(main_window, main_window.set_text)

    main_window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec()