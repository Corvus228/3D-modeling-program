import os, sys, time
from classOBJ import OBJ
from classListWidget import ListWidget

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QListWidget, QListWidgetItem, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LMB = False
        self.RMB = False
        self.MMB = False
        self.mouseCoordinates = []

        self.setGeometry(0, 0, 1000, 1000)
        self.setMouseTracking(True)
        self.window = QWidget()

        self.grid = QGridLayout()

        self.list = ListWidget()
        self.widget = Widget(self.list)
        self.list.getChild(self.widget)

        self.grid.addWidget(self.widget, 0, 0)
        self.grid.addWidget(self.list, 0, 1)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")

        self.window.setLayout(self.grid)
        self.setCentralWidget(self.window)

        for file in os.listdir("OBJ"):
            action = QAction(f"Add {file}", self)
            action.triggered.connect(lambda checked, f=file: self.widget.createOBJ(f"OBJ/{f}"))
            self.file_menu.addAction(action)

    def mouseMoveEvent(self, e):
        if self.widget.scene.listOfOBJ:
            x = int(e.x())
            y = int(e.y())
            amplitude = [self.mouseCoordinates[0] - x, self.mouseCoordinates[1] - y]
            self.mouseCoordinates = [int(e.x()), int(e.y())]
            self.setWindowTitle(f"Mouse Coordinates: ({x}, {y})")

            if self.LMB:
                self.widget.scene.objRotateX(self.widget.scene.selectedOBJs, amplitude[1])
                self.widget.scene.objRotateY(self.widget.scene.selectedOBJs, amplitude[0])
                self.widget.update()
            if self.RMB:
                self.widget.scene.objMove(self.widget.scene.selectedOBJs, amplitude[0], amplitude[1])
                self.widget.update()

    def mousePressEvent(self, e):
        self.mouseCoordinates = [int(e.x()), int(e.y())]

        if e.button() == Qt.LeftButton:
            self.LMB = True

        elif e.button() == Qt.RightButton:
            self.RMB = True

        elif e.button() == Qt.MiddleButton:
            self.MMB = True

        # while self.LMB:
        #     #self.widget.rotateX(0.1)
        #     self.widget.rotateY(10)
        #     time.sleep(0.01)
    def mouseReleaseEvent(self, e):
        self.LMB = False
        self.RMB = False
        self.MMB = False

    def wheelEvent(self, e):
        if self.widget.scene.listOfOBJ:
            x = e.angleDelta().y() // 120
            self.widget.scene.objScale(self.widget.scene.selectedOBJs, pow(2, x))
            self.widget.update()

class Widget(QWidget):
    def __init__(self, list):
        super().__init__()
        self.filename = 0
        self.obj = 0
        self.setMinimumSize(1000, 600)
        self.list = list
        self.scene = list.scene

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        w = self.width() / 2
        h = self.height() / 2
        if w > h:
            w = h
        if h > w:
            h = w
        if self.scene.listOfOBJ:
            for obj in self.scene.listOfOBJ:
                obj.rescalePolygon(w, h)
                self.paintOBJ(qp, obj, obj.paintColor)
        qp.end()

    def createOBJ(self, filename):
        self.scene.addOBJ(OBJ(filename))
        self.list.updateList()
        self.update()

    def paintOBJ(self, qp, obj, color):
        qp.setPen(color)
        #qp.setBrush(QBrush(Qt.GlobalColor.red))
        for poly in obj.polygons:
            qp.drawPolygon(poly)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
