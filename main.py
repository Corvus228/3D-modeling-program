import sys, random, matrix
from classOBJ import OBJ

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QPainter, QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LMB = False
        self.RMB = False
        self.MMB = False
        self.mouseCoordinates = []

        self.setGeometry(300, 300, 500, 500)
        self.setMouseTracking(True)
        self.window = QMainWindow()

        self.widget = Widget()
        self.setCentralWidget(self.widget)

        button_action = QAction("&Draw Робот", self)
        button_action.triggered.connect(lambda: self.widget.setOBJ("Робот.obj"))

        button_action1 = QAction("&Draw Параллелепипед", self)
        button_action1.triggered.connect(lambda: self.widget.setOBJ("Параллелепипед.obj"))

        button_action2 = QAction("&Draw Голова", self)
        button_action2.triggered.connect(lambda: self.widget.setOBJ("Голова.obj"))

        button_action3 = QAction("&Move", self)
        button_action3.triggered.connect(lambda: self.widget.move(100, 100))

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.file_menu.addAction(button_action)
        self.file_menu.addAction(button_action1)
        self.file_menu.addAction(button_action2)
        self.file_menu.addAction(button_action3)
        # self.timer = QTimer
        # self.timer.setInterval(100000)#

    def mouseMoveEvent(self, e):
        x = int(e.position().x())
        y = int(e.position().y())
        amplitude = [self.mouseCoordinates[0] - x, self.mouseCoordinates[1] - y]
        self.mouseCoordinates = [int(e.position().x()), int(e.position().y())]

        self.setWindowTitle(f"Mouse Coordinates: ({x}, {y})")
        if self.LMB:
            self.widget.rotateX(amplitude[1])
            self.widget.rotateY(amplitude[0])

    def mousePressEvent(self, e):
        self.mouseCoordinates = [int(e.position().x()), int(e.position().y())]

        if e.button() == Qt.MouseButton.LeftButton:
            self.LMB = True

        elif e.button() == Qt.MouseButton.RightButton:
            self.RMB = True

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.MMB = True

    def mouseReleaseEvent(self, e):
        self.LMB = False
        self.RMB = False
        self.MMB = False

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = 0
        self.obj = 0

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        w = self.width() / 2
        h = self.height() / 2
        if(w > h):
            w = h
        if (h > w):
            h = w
        if self.obj != 0:
            self.obj.rescalePolygon(w, h)
            self.paintOBJ(qp, self.obj)
        qp.end()

    def setOBJ(self, filename):
        self.obj = OBJ(filename)
        self.repaint()

    def paintOBJ(self, qp, obj):
        qp.setPen(Qt.GlobalColor.red)
        #qp.setBrush(QBrush(QColor(255, 255, 255, 255)))
        for poly in obj.polygons:
            qp.drawPolygon(poly)

    def rotateX(self, angle):
        matrix.rotateX(angle, self.obj)
        self.repaint()

    def rotateY(self, angle):
        matrix.rotateY(angle, self.obj)
        self.repaint()

    def rotateZ(self, angle):
        matrix.rotateZ(angle, self.obj)
        self.repaint()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()