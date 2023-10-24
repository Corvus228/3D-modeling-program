import sys, random
import numpy as np

from PyQt6.QtCore import Qt, QRect, QPointF,QSize
from PyQt6.QtGui import QAction, QColor,  QPainter, QPainterPath, QPen, QFont
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QWidget, QLineEdit, QToolBar, QVBoxLayout, QHBoxLayout, QStackedLayout, QPushButton

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 500, 500)

        self.window = QMainWindow()

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        widget = Widget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        button_action = QAction("&Draw OBJ", self)
        button_action.triggered.connect(lambda: widget.setFilename("C:/Users/Пользователь/Desktop/негр.obj"))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)


class Widget(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

    filename = 0
    def setFilename(self, file):
        self.filename = file
        self.update()
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        if self.filename != 0:
            self.drawObjFromFile(qp, self.filename)
        qp.end()

    # def paint(self, x0, y0, x1, y1, color):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawLine(qp, x0, y0, x1, y1, color)
    #     qp.end()

    def drawLine(self, qp, x1, y1, x2, y2, color):
        qp.setPen(color)

        steep = False
        if abs(x1 - x2) < abs(y1 - y2):
            x1, x2, y1, y2 = y1, y2, x1, x2
            steep = True

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1

        derror2 = abs(dy)*2
        error2 = 0
        y = y1

        for x in range(x1, x2+1):
            if steep:
                qp.drawPoint(y, x)
            else:
                qp.drawPoint(x, y)
            error2 += derror2

            if error2 > dx:
                if y2 > y1:
                    y += 1
                else:
                    y -= 1
                error2 -= dx * 2

    def drawObjFromFile(self, qp, filename):
        f = open(filename)
        lines = f.readlines()
        f.close()
        points = []
        w = self.width() / 2
        h = self.height() / 2
        for line in lines:
            if line[0] == 'v' and line[1] == ' ':
                a, point_x, point_y, point_z = line.split()
                points.append([-float(point_x), -float(point_y), -float(point_z)])
            if line[0] == 'f':
                a = line.split()
                x = a[1].split('/')
                y = a[2].split('/')
                z = a[3].split('/')
                for i in range(1, 4):
                    v0 = a[i]
                    v1 = a[(i % 3) + 1]
                    v0 = v0.split('/')
                    v1 = v1.split('/')
                    f0 = int(v0[0])
                    f1 = int(v1[0])
                    x0 = int((points[f0 - 1][0] + 1.) * w)
                    y0 = int((points[f0 - 1][1] + 1.) * h)
                    x1 = int((points[f1 - 1][0] + 1.) * w)
                    y1 = int((points[f1 - 1][1] + 1.) * h)
                    self.drawLine(qp, x0, y0, x1, y1, Qt.GlobalColor.red)
                    #print('(',x0, ',', y0, '), ', '(', x1, ',', y1, ')', '\n')

window = MainWindow()
window.show()

app.exec()