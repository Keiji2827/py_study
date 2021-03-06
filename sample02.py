import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.show()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.setBrush(Qt.yellow)
        painter.drawRect(10, 10, 100, 100)

        painter2 = QPainter(self)
        painter2.setPen(Qt.blue)
        painter2.setBrush(Qt.red)
        painter2.drawRect(110, 10, 100, 100)


def main():
    app = QApplication(sys.argv)
    w = Widget()
#    w.show()
#    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()
