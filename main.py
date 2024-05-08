import os, sys, time
from classOBJ import OBJ
from classListWidget import ListWidget

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QListWidget, QListWidgetItem, QGridLayout

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

        self.window.setLayout(self.grid)
        self.setCentralWidget(self.window)

        for file in os.listdir("OBJ"):
            action = QAction(f"Add {file}", self)
            action.triggered.connect(lambda checked, f=file: self.widget.createOBJ(f"OBJ/{f}"))
            self.file_menu.addAction(action)

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

class Widget(QWidget):
    """
        Виджет для отображения и взаимодействия с 3D объектами.

        Атрибуты:
            filename (str): Путь к файлу последнего загруженного объекта.
            obj (OBJ): Последний добавленный объект на сцену.
            list (ListWidget): Список, связанный с виджетом, для отображения и обновления списка объектов.
            scene (Scene): Сцена, к которой привязан виджет, содержащая объекты, управляемые через виджет.

        Методы:
           paintEvent(e): Рисует объекты на виджете, учитывая текущий масштаб и положение объектов.
           createOBJ(filename): Добавляет новый объект на сцену и обновляет список объектов.
           paintOBJ(qp, obj, color): Рисует один объект с заданным цветом.
    """
    def __init__(self, list):
        """ Инициализирует виджет, устанавливает размеры и привязывает сцену для взаимодействия с объектами. """
        super().__init__()
        self.filename = 0
        self.obj = 0
        self.setMinimumSize(1000, 600)
        self.list = list
        self.scene = list.scene

    def paintEvent(self, e):
        """ Обрабатывает событие отрисовки, рисуя все объекты на сцене с учетом текущего масштаба и положения. """
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
        """
            Создает и добавляет новый OBJ объект из указанного файла в сцену.

            Параметры:
                filename (str): Путь к файлу OBJ для загрузки.
        """
        self.scene.addOBJ(OBJ(filename))
        self.list.updateList()
        self.update()

    def paintOBJ(self, qp, obj, color):
        """
            Рисует один объект, используя QPainter, с заданным цветом.

            Параметры:
                qp (QPainter): Объект QPainter для рисования.
                obj (OBJ): Объект для отрисовки.
                color (QColor): Цвет пера для рисования объекта.
        """
        qp.setPen(color)
        #qp.setBrush(QBrush(Qt.GlobalColor.red))
        for poly in obj.polygons:
            qp.drawPolygon(poly)

def main():
    """ Инициализация и запуск главного окна приложения."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
