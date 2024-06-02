from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from classOBJ import OBJ


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
        qp.setRenderHint(QPainter.Antialiasing)
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
                self.paintOBJ(qp, obj, obj.paintColor, obj.polyColor)
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

    def paintOBJ(self, qp, obj, color, polyColor):
        """
            Рисует один объект, используя QPainter, с заданным цветом.

            Параметры:
                qp (QPainter): Объект QPainter для рисования.
                obj (OBJ): Объект для отрисовки.
                color (QColor): Цвет пера для рисования объекта.
        """
        sorted_polygons = sorted(obj.polygons, key=lambda item: item[1], reverse=True)
        qp.setPen(color)
        qp.setBrush(polyColor)

        for poly, z in sorted_polygons:
            qp.drawPolygon(poly)
