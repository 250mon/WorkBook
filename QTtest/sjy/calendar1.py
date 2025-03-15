import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect, QDate

class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGridVisible(True)
        self.setMinimumSize(1000, 800)  # Increase the calendar size
        self.bar_colors = {}

    # Store the bar colors for the given date and trigger a widget update
    def set_bar_colors(self, date, colors1, colors2, colors3, colors4, colors5, colors6):
        self.bar_colors[date] = (colors1, colors2, colors3, colors4, colors5, colors6)
        self.update()

    # Override paintCell to draw custom bars in each cell
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        if date.month() == self.monthShown():
            bar_height = 8
            num_segments1 = 8  # Number of segments for the first and fourth bars
            num_segments2 = 8  # Number of segments for the second and fifth bars
            num_segments3 = 6  # Number of segments for the third and sixth bars

            segment_width = rect.width() // max(num_segments1, num_segments2, num_segments3)  # Ensure all bars have the same segment width

            # Draw the date in the top-left corner of the cell
            painter.drawText(rect.left() + 5, rect.top() + 15, date.toString("dd"))

            if date in self.bar_colors:
                colors1, colors2, colors3, colors4, colors5, colors6 = self.bar_colors[date]
            else:
                colors1 = [QColor(100, 150, 200) for _ in range(num_segments1)]
                colors2 = [QColor(200, 100, 150) for _ in range(num_segments2)]
                colors3 = [QColor(150, 200, 100) for _ in range(num_segments3)]
                colors4 = [QColor(200, 150, 100) for _ in range(num_segments1)]
                colors5 = [QColor(100, 200, 150) for _ in range(num_segments2)]
                colors6 = [QColor(150, 100, 200) for _ in range(num_segments3)]

            # Draw the first set of bars
            for i in range(num_segments1):
                bar1_rect = QRect(rect.left() + i * segment_width, rect.top() + 25, segment_width - 1, bar_height)
                painter.setBrush(colors1[i])
                painter.drawRect(bar1_rect)

            for i in range(num_segments2):
                bar2_rect = QRect(rect.left() + i * segment_width, rect.top() + 40, segment_width - 1, bar_height)
                painter.setBrush(colors2[i])
                painter.drawRect(bar2_rect)

            for i in range(num_segments3):
                bar3_rect = QRect(rect.left() + i * segment_width, rect.top() + 55, segment_width - 1, bar_height)
                painter.setBrush(colors3[i])
                painter.drawRect(bar3_rect)

            # Draw the second set of bars
            for i in range(num_segments1):
                bar4_rect = QRect(rect.left() + i * segment_width, rect.top() + 75, segment_width - 1, bar_height)
                painter.setBrush(colors4[i])
                painter.drawRect(bar4_rect)

            for i in range(num_segments2):
                bar5_rect = QRect(rect.left() + i * segment_width, rect.top() + 90, segment_width - 1, bar_height)
                painter.setBrush(colors5[i])
                painter.drawRect(bar5_rect)

            for i in range(num_segments3):
                bar6_rect = QRect(rect.left() + i * segment_width, rect.top() + 105, segment_width - 1, bar_height)
                painter.setBrush(colors6[i])
                painter.drawRect(bar6_rect)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Initialize the main window and layout
    def initUI(self):
        self.setWindowTitle('Calendar with Segmented Time Bars')
        self.setGeometry(100, 100, 1200, 900)  # Increase the window size

        layout = QVBoxLayout()

        self.calendar = CalendarWidget(self)
        layout.addWidget(self.calendar)

        self.setLayout(layout)

        # Example of setting colors for a specific date
        date = QDate.currentDate()
        colors1 = [QColor(255, 0, 0) if i % 2 == 0 else QColor(0, 255, 0) for i in range(8)]
        colors2 = [QColor(0, 0, 255) if i % 2 == 0 else QColor(255, 255, 0) for i in range(8)]
        colors3 = [QColor(255, 0, 255) if i % 2 == 0 else QColor(0, 255, 255) for i in range(6)]
        colors4 = [QColor(0, 128, 128) if i % 2 == 0 else QColor(128, 0, 128) for i in range(8)]
        colors5 = [QColor(128, 128, 0) if i % 2 == 0 else QColor(128, 128, 255) for i in range(8)]
        colors6 = [QColor(255, 128, 0) if i % 2 == 0 else QColor(128, 255, 128) for i in range(6)]
        self.calendar.set_bar_colors(date, colors1, colors2, colors3, colors4, colors5, colors6)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
