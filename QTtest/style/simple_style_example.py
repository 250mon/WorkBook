import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

if __name__ == "__main__":
    app = QApplication()
    title = QLabel("Title")
    title.setAlignment(Qt.AlignCenter)
    title.setObjectName("title")

    w = QLabel("This is a placeholder text")
    w.setAlignment(Qt.AlignCenter)
    w.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)

    vbox = QVBoxLayout()
    vbox.addWidget(title)
    vbox.addWidget(w)
    main = QWidget()
    main.setLayout(vbox)
    main.show()

    with open("simple_style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())