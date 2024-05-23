import matrix
import json
from classOBJ import OBJ

class Scene():
    """
        Класс для управления сценой.

        Атрибуты:
        listOfOBJ (list): Список всех объектов на сцене.
        listOfNames (list): Список имен всех объектов на сцене.
        selectedOBJs (list): Список текущих выбранных объектов.

        Методы:
        getOBJnames(): Обновляет список имен на основе текущих объектов в сцене.
        addOBJ(obj): Добавляет объект в сцену.
        removeOBJ(objname): Удаляет объект по его имени.
        setCurrentOBJ(objname): Устанавливает объект как текущий выбранный.
        unselectOBJ(objname): Снимает выбор с объекта.
        addCurrentOBJ(objname): Добавляет объект в список выбранных.
        objRotateX(obj, angle): Вращает выбранные объекты вокруг оси X.
        objRotateY(obj, angle): Вращает выбранные объекты вокруг оси Y.
        objRotateZ(obj, angle): Вращает выбранные объекты вокруг оси Z.
        objScale(obj, coefficient): Масштабирует выбранные объекты.
        objMove(obj, coefficient_x, coefficient_y): Перемещает выбранные объекты.
    """

    def __init__(self):
        """ Инициализирует новый экземпляр класса Scene. """
        super(Scene, self).__init__()
        self.listOfOBJ = []
        self.listOfNames = []
        self.selectedOBJs = []
        self.getOBJnames()

    def getOBJnames(self):
        """ Обновляет список имен объектов в сцене. """
        self.listOfNames = []
        for obj in self.listOfOBJ:
            self.listOfNames.append(obj.name)

    def addOBJ(self, obj):
        """ Добавляет объект в сцену и обновляет список имен. """
        self.listOfOBJ.append(obj)
        self.getOBJnames()

    def removeOBJ(self, objname):
        """ Удаляет объект по его имени из сцены и обновляет список имен. """
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.listOfOBJ.remove(obj)
        self.getOBJnames()

    def setCurrentOBJ(self, objname):
        """ Устанавливает указанный объект как текущий выбранный и изменяет его цвет. """
        self.selectedOBJs = []
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.selectedOBJs.append(obj)
                obj.setSelectedColor()
        self.getOBJnames()

    def unselectOBJ(self, objname):
        """ Снимает выбор с указанного объекта и возвращает его цвет в исходное состояние. """
        for obj in self.selectedOBJs:
            if obj.name == objname:
                self.selectedOBJs.remove(obj)
                obj.setUnselectedColor()
        self.getOBJnames()

    def addCurrentOBJ(self, objname):
        """ Добавляет объект в список выбранных без изменения текущего выбора. """
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.selectedOBJs.append(obj)
        self.getOBJnames()

    def objRotateX(self, obj, angle):
        """ Вращает все выбранные объекты вокруг оси X на указанный угол. """
        for obj in self.selectedOBJs:
            matrix.rotateX(angle, obj)

    def objRotateY(self, obj, angle):
        """ Вращает все выбранные объекты вокруг оси Y на указанный угол. """
        for obj in self.selectedOBJs:
            matrix.rotateY(angle, obj)

    def objRotateZ(self, obj, angle):
        """ Вращает все выбранные объекты вокруг оси Z на указанный угол. """
        for obj in self.selectedOBJs:
            matrix.rotateZ(angle, obj)

    def objScale(self, obj, coefficient):
        """ Масштабирует все выбранные объекты на указанный коэффициент. """
        for obj in self.selectedOBJs:
            matrix.scale(coefficient, obj)

    def objMove(self, obj, coefficient_x, coefficient_y):
        """ Перемещает все выбранные объекты на указанные коэффициенты по осям X и Y. """
        for obj in self.selectedOBJs:
            matrix.move(coefficient_x, coefficient_y, obj)

    def saveScene(self, filename):
        scene_data = []
        for obj in self.listOfOBJ:
            obj_data = {
                'name': obj.name,
                'points': obj.points,
                'pointsIndex': obj.pointsIndex
            }
            scene_data.append(obj_data)

        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(scene_data, f, indent=4)

    def loadScene(self, filename):
        with open(filename, 'r') as f:
            scene_data = json.load(f)

        self.listOfOBJ = []
        for obj_data in scene_data:
            obj = OBJ()
            obj.name = obj_data['name']
            obj.points = obj_data['points']
            obj.pointsIndex = obj_data['pointsIndex']
            self.addOBJ(obj)
        self.getOBJnames()