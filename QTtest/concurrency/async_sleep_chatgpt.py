import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class AsyncQApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.loop = asyncio.get_event_loop()
        self.count = 0

    async def exec(self):
        await self.loop.create_task(self.asyncio_loop())
        super().exec()

    async def asyncio_loop(self):
        label = self.activeWindow().findChild(QLabel, "myLabel")
        while True:
            label.setText(f"Updated text {self.count}")
            self.count += 1
            print(self.count)
            await asyncio.sleep(1)  # Update the label every 1 second

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Asyncio Example")
        self.resize(300, 200)

        label = QLabel("Initial text", self)
        label.setObjectName("myLabel")
        label.setGeometry(50, 50, 200, 50)

async def main():
    app = AsyncQApplication(sys.argv)
    window = MainWindow()
    window.show()
    await app.exec()

if __name__ == '__main__':
    asyncio.run(main())
