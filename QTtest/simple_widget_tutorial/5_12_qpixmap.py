import sys, io
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image, ImageQt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # show an image
        pixmap = QPixmap('../assets/landscape.png')
        pixmap = pixmap.scaled(pixmap.width()//2, pixmap.height()//2)
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)

        # caption
        lbl_caption = QLabel('Width: ' + str(pixmap.width()) + ', Height: '
                          + str(pixmap.height()))
        lbl_caption.setAlignment(Qt.AlignCenter)

        # show a pillow image
        # method 1
        pil_img = Image.open('../assets/landscape.png')
        pil_img_rgba = pil_img.convert("RGBA")
        data = pil_img_rgba.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img_rgba.width, pil_img_rgba.height, QImage.Format_RGBA8888)
        pil_pixmap = QPixmap.fromImage(qimg)
        pil_pixmap = pil_pixmap.scaled(pil_pixmap.width()//2, pil_pixmap.height()//2)
        lbl_pil_img = QLabel()
        lbl_pil_img.setPixmap(pil_pixmap)

        # method 2
        # Convert Pillow image to bytes-like object
        image_bytes = io.BytesIO()
        pil_img.save(image_bytes, format='PNG')  # Choose appropriate format here
        image_bytes.seek(0)
        # Create QPixmap and load image data from bytes
        pil_pixmap2 = QPixmap()
        pil_pixmap2.loadFromData(image_bytes.getvalue())
        pil_pixmap2 = pil_pixmap2.scaled(pil_pixmap2.width()//2, pil_pixmap2.height()//2)
        lbl_pil_img2 = QLabel()
        lbl_pil_img2.setPixmap(pil_pixmap2)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_caption)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_pil_img)
        hbox.addWidget(lbl_pil_img2)

        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
