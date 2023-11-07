from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os


class widgetIMG(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250,130)
        self.path = None

    def paintEvent(self, event):
        # Create a QPainter to draw on the widget
        painter = QPainter(self)


        # Set the pen for drawing the border
        pen = QPen(QColor(255, 182, 182))  # Set the border color (black)
        pen.setWidth(2)  # Set the border width
        painter.setPen(pen)

        # Draw the border around the widget's boundaries
        painter.drawRect(self.rect())

        if self.path is not None:
            image = QPixmap(self.path)
            painter.drawPixmap(self.rect(), image)

    def setPath(self,path):
        self.path = path
        self.update()

