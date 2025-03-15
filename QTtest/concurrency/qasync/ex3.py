import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QObject
import qasync
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, select

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qasync SQLAlchemy Example")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        
        self.btn_create = QPushButton("Create User")
        self.btn_create.clicked.connect(self.create_user)
        layout.addWidget(self.btn_create)

        self.btn_fetch = QPushButton("Fetch Users")
        self.btn_fetch.clicked.connect(self.fetch_users)
        layout.addWidget(self.btn_fetch)

        self.label = QLabel("No users fetched yet")
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    async def init_db(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///example.db", echo=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @qasync.asyncSlot()
    async def create_user(self):
        async with self.async_session() as session:
            new_user = User(name="John Doe")
            session.add(new_user)
            await session.commit()
        self.label.setText("User created")

    @qasync.asyncSlot()
    async def fetch_users(self):
        async with self.async_session() as session:
            result = await session.execute(select(User.name))
            users = result.scalars().all()
        self.label.setText(f"Users: {', '.join(users)}")

async def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    await window.init_db()
    window.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())