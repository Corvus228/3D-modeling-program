import filereader
from PyQt5.QtCore import Qt, QPointF


class OBJ():
    ID = 0

    def __init__(self, filename):
        super().__init__()
        self.paintColor = Qt.GlobalColor.black
        self.points = []
        self.pointsIndex = []
        self.normals = []
        self.textures = []
        self.polygons = []
        self.getOBJ(filename)
        self.name = (f"{filename.split('.')[0].split('/')[1]}{OBJ.ID}")
        OBJ.ID += 1

    def setSelectedColor(self):
        self.paintColor = Qt.GlobalColor.blue

    def setUnselectedColor(self):
        self.paintColor = Qt.GlobalColor.black

    def getOBJ(self, filename):
        lines = filereader.readfile(filename)
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
        polygon = []
        for i in range(len(pointind)):
            polygon.append(QPointF((self.points[pointind[i]][0] + 1.) * w, (self.points[pointind[i]][1] + 1.) * h))
        return polygon

    def rescalePolygon(self, w, h):
        self.polygons = []
        for point in self.pointsIndex:
            self.polygons.append(self.createPolygon(point, w, h))