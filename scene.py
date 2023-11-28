import matrix
class Scene():
    def __init__(self):
        super(Scene, self).__init__()
        self.listOfOBJ = []
        self.listOfNames = []
        self.selectedOBJs = []
        self.getobjnames()

    def getobjnames(self):
        self.listOfNames = []
        for obj in self.listOfOBJ:
            self.listOfNames.append(obj.name)

    def addOBJ(self, obj):
        self.listOfOBJ.append(obj)
        self.getobjnames()

    def removeOBJ(self, objname):
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.listOfOBJ.remove(obj)
        self.getobjnames()

    def setCurrentOBJ(self, objname):
        self.selectedOBJs = []
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.selectedOBJs.append(obj)
                obj.setSelectedColor()
        self.getobjnames()

    def unselectOBJ(self, objname):
        for obj in self.selectedOBJs:
            if obj.name == objname:
                self.selectedOBJs.remove(obj)
                obj.setUnselectedColor()
        self.getobjnames()

    def addCurrentOBJ(self, objname):
        for obj in self.listOfOBJ:
            if obj.name == objname:
                self.selectedOBJs.append(obj)
        self.getobjnames()

    def objRotateX(self, obj, angle):
        for obj in self.selectedOBJs:
            matrix.rotateX(angle, obj)

    def objRotateY(self, obj, angle):
        for obj in self.selectedOBJs:
            matrix.rotateY(angle, obj)

    def objRotateZ(self, obj, angle):
        for obj in self.selectedOBJs:
            matrix.rotateZ(angle, obj)

    def objScale(self, obj, coefficient):
        for obj in self.selectedOBJs:
            matrix.scale(coefficient, obj)

    def objMove(self, obj, coefficient_x, coefficient_y):
        for obj in self.selectedOBJs:
            matrix.move(coefficient_x, coefficient_y, obj)

