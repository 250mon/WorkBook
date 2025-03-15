import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import PySide6.QtAsyncio as QtAsyncio
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
        self.setWindowTitle("QtAsyncio SQLAlchemy Example")
        
        layout = QVBoxLayout()
        
        self.text = QLabel("No user fetched yet.")
        layout.addWidget(self.text)
        
        async_trigger = QPushButton(text="Fetch User")
        async_trigger.clicked.connect(lambda: asyncio.ensure_future(self.fetch_user()))
        layout.addWidget(async_trigger)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.engine = create_async_engine("sqlite+aiosqlite:///example.db", echo=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
    
    async def fetch_user(self):
        async with self.async_session() as session:
            result = await session.execute(select(User).order_by(User.id))
            user = result.scalars().first()
            if user:
                self.text.setText(f"Fetched user: {user.name}")
            else:
                self.text.setText("No user found.")

async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(User.__table__.insert(), [{"name": "John Doe"}, {"name": "Jane Smith"}])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    
    async def run_app():
        await setup_db(main_window.engine)
        main_window.show()
        await QtAsyncio.run_forever()
    
    QtAsyncio.run(run_app())