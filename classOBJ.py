from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor


class OBJ:
    """
        Класс для работы с объектами в формате OBJ.

        Атрибуты:
        ID (int): Статический счетчик, используемый для генерации уникальных имен объектов.
        paintColor (QColor): Цвет объекта, который можно изменить.
        points (list): Список точек объекта в формате [x, y, z].
        pointsIndex (list): Список индексов точек для построения полигонов.
        normals (list): Список нормалей вершин.
        textures (list): Список текстурных координат.
        polygons (list): Список полигонов, каждый из которых представлен координатами QPointF.
        name (str): Уникальное имя объекта, сформированное из имени файла и идентификатора.

        Методы:
        __init__(filename): Конструктор класса, который инициализирует объект и загружает данные из файла.
        setSelectedColor(): Устанавливает цвет объекта в синий (выбранное состояние).
        setUnselectedColor(): Устанавливает цвет объекта в черный (невыбранное состояние).
        getOBJ(filename): Читает данные из файла OBJ и загружает их в атрибуты объекта.
        createPolygon(pointing, w, h): Создает полигон из индексов вершин с заданными параметрами масштабирования.
        rescalePolygon(w, h): Масштабирует все полигоны объекта в соответствии с заданными размерами.
    """
    ID = 0

    def __init__(self, filename=None):
        """
            Инициализирует объект на основе данных из файла формата OBJ.

            Параметры:
            filename (str): Путь к файлу OBJ, который необходимо прочитать и обработать.

            Атрибуты:
            paintColor (QColor): Цвет объекта, по умолчанию черный.
            points (list): Список точек объекта.
            pointsIndex (list): Индексы точек для построения полигонов.
            normals (list): Список нормалей вершин.
            textures (list): Список текстурных координат.
            polygons (list): Список полигонов, представленных в виде координат QPointF.
            name (str): Уникальное имя объекта, созданное из имени файла и идентификатора.
        """
        super().__init__()
        self.paintColor = Qt.GlobalColor.black
        self.polyColor = Qt.GlobalColor.yellow
        self.points = []
        self.pointsIndex = []
        self.normals = []
        self.textures = []
        self.polygons = []
        self.getOBJ(filename)
        if filename:
            self.getOBJ(filename)
            self.name = f"{filename.split('.')[0].split('/')[-1]}{OBJ.ID}"
            OBJ.ID += 1
        else:
            self.name = f"OBJ{OBJ.ID}"
            OBJ.ID += 1

    def setSelectedColor(self):
        """ Устанавливает цвет объекта в синий (выбранный объект). """
        self.paintColor = Qt.GlobalColor.red

    def setUnselectedColor(self):
        """ Устанавливает цвет объекта в черный (не выбранный объект). """
        self.paintColor = Qt.GlobalColor.black

    def getOBJ(self, filename):
        """
            Читает файл OBJ и загружает данные в объект.

            Параметры:
            filename (str): Путь к файлу OBJ.
        """
        if filename is not None:
            with open(filename) as f:
                lines = f.readlines()
            for line in lines:
                if line[0] == 'v' and line[1] == ' ':
                    a, x, y, z = line.split()
                    self.points.append([-float(x), -float(y), -float(z)])
                if line[0] == 'v' and line[1] == 'n':
                    a, x, y, z = line.split()
                    self.normals.append([float(x), float(y), float(z)])
                if line[0] == 'v' and line[1] == 't':
                    coords = []
                    a = line.split()
                    for xyz in a:
                        if xyz != 'vt':
                            coords.append(float(xyz))
                    self.textures.append(coords)
                if line[0] == 'f':
                    pointind = []
                    a = line.split()
                    for xyz in a:
                        if xyz != 'f':
                            num = xyz.split('/')
                            pointind.append(int(num[0]) - 1)
                    self.pointsIndex.append(pointind)
                    self.polygons.append(self.createPolygon(pointind, 1, 1))

    def createPolygon(self, pointind, w, h):
        """
            Создает полигон на основе индексов точек и размеров.

            Параметры:
            pointing (list): Список индексов точек.
            w (float): Ширина масштабирования.
            h (float): Высота масштабирования.

            Возвращает:
            polygon: Список полигонов.
         """
        polygon = []
        z_buffer = []
        for i in range(len(pointind)):
            polygon.append(QPointF((self.points[pointind[i]][0] + 1.) * w, (self.points[pointind[i]][1] + 1.) * h))
            z_buffer.append(self.points[pointind[i]][2])
        return [polygon, z_buffer]

    def rescalePolygon(self, w, h):
        """
            Масштабирует все полигоны объекта согласно заданным размерам.

            Параметры:
            w (float): Новая ширина масштабирования.
            h (float): Новая высота масштабирования.
        """
        self.polygons = []
        for point in self.pointsIndex:
            self.polygons.append(self.createPolygon(point, w, h))

    def calculate_average_z(self, z):
        """Вычисляет среднее значение Z для полигонов"""
        return sum([vertex for vertex in z]) / len(z)

    def color_to_dictionary(self, color):
        """Преобразует QColor в словарь."""
        return {
            'red': color.red(),
            'green': color.green(),
            'blue': color.blue(),
            'alpha': color.alpha()
        }

    def dictionary_to_color(self, color_dict):
        """Создает QColor из словаря."""
        return QColor(color_dict['red'], color_dict['green'], color_dict['blue'], color_dict['alpha'])
