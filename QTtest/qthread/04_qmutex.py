import logging
import random
import sys
from time import sleep

from PySide6.QtCore import QMutex, QObject, QThread, pyqtSignal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format="%(message)s", level=logging.INFO)

balance = 100.00
mutex = QMutex()


class AccountManager(QObject):
    finished = pyqtSignal()
    updateBalance = pyqtSignal()

    def withdraw(self, person, amount):
        logging.info(f"{person} wants to withdraw ${amount:,.2f}...")
        global balance
        mutex.lock()
        if balance - amount >= 0:
            sleep(1)
            balance -= amount
            logging.info(f"-${amount:,.2f} accepted")
        else:
            logging.info(f"-${amount:,.2f} rejected")
        logging.info(f"===Balance===: ${balance:.2f}")
        self.updateBalance.emit()
        mutex.unlock()
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.threads = []

    def setupUi(self):
        self.setWindowTitle("Account Manager")
        self.resize(200, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        button = QPushButton("Withdraw Money!")
        button.clicked.connect(self.startThreads)
        self.balanceLabel = QLabel(f"Current Balance: ${balance:,.2f}")

        layout = QVBoxLayout()
        layout.addWidget(self.balanceLabel)
        layout.addWidget(button)
        self.centralWidget.setLayout(layout)

    def createThread(self, person, amount):
        thread = QThread()
        worker = AccountManager()
        worker.moveToThread(thread)
        thread.started.connect(lambda: worker.withdraw(person, amount))
        worker.updateBalance.connect(self.updataBalance)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        return thread

    def updataBalance(self):
        self.balanceLabel.setText(f"Current Balance: ${balance:,.2f}")

    def startThreads(self):
        self.threads.clear()
        people = {
            "Alice": random.randint(100, 10000) / 100,
            "Bob": random.randint(100, 10000) / 100,
        }
        self.threads = [
            self.createThread(person, amount) for person, amount in people.items()
        ]
        for thread in self.threads:
            thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
