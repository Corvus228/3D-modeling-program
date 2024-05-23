import os, sys
from classListWidget import ListWidget
from classWidget import Widget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction,\
                            QGridLayout, QFileDialog


class MainWindow(QMainWindow):
    """
       Главное окно приложения для управления и визуализации 3D объектов.

       Атрибуты:
           LMB (bool): Состояние левой кнопки мыши.
           RMB (bool): Состояние правой кнопки мыши.
           MMB (bool): Состояние средней кнопки мыши.
           mouseCoordinates (list): Текущие координаты мыши.

       Методы:
           mouseMoveEvent(e): Обрабатывает движение мыши для вращения и перемещения объектов.
           mousePressEvent(e): Обрабатывает нажатие кнопок мыши, устанавливая начальные координаты и состояние кнопок.
           mouseReleaseEvent(e): Обрабатывает отпускание кнопок мыши, сбрасывая состояние кнопок.
           wheelEvent(e): Обрабатывает события колеса мыши для масштабирования объектов.
    """
    def __init__(self):
        """ Инициализирует главное окно приложения, устанавливает его размеры и располагает элементы интерфейса."""
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

        openfile = QAction("&Open...", self.file_menu)
        openfile.triggered.connect(lambda checked: self.openFile())
        self.file_menu.addAction(openfile)

        scenesave = QAction("&Save scene...", self.file_menu)
        scenesave.triggered.connect(lambda checked: self.saveSceneAsFile())
        self.file_menu.addAction(scenesave)

        self.window.setLayout(self.grid)
        self.setCentralWidget(self.window)

    def openFile(self):
        f = QFileDialog.getOpenFileName()
        path, extension = os.path.splitext(f[0])
        if extension == '.obj':
            self.widget.createOBJ(f"OBJ/{os.path.basename(f[0])}")
        elif extension == '.json':
            self.list.scene.loadScene(f[0])
            self.list.updateList()
        else:
            # Add exception later
            pass

    def saveSceneAsFile(self):
        f = QFileDialog.getSaveFileName()[0]
        self.list.scene.saveScene(f)

    def mouseMoveEvent(self, e):
        """ Обрабатывает перемещение мыши, используя изменение координат для вращения или перемещения объектов."""
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
        """ Обрабатывает события нажатия кнопок мыши, устанавливая начальные координаты и состояние кнопок. """
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
        """ Обрабатывает события отпускания кнопок мыши, сбрасывая состояние кнопок. """
        self.LMB = False
        self.RMB = False
        self.MMB = False

    def wheelEvent(self, e):
        """ Обрабатывает события колеса мыши для масштабирования выбранных объектов. """
        if self.widget.scene.listOfOBJ:
            x = e.angleDelta().y() // 120
            self.widget.scene.objScale(self.widget.scene.selectedOBJs, pow(2, x))
            self.widget.update()



def main():
    """ Инициализация и запуск главного окна приложения."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
