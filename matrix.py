import math
import numpy as np

def rotateZ(angle, obj):
    angle = np.sign(angle) * 0.01
    Z = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]
    for index, p in enumerate(obj.points):
        rotated = np.dot(Z, p)
        obj.points[index] = (rotated[0], rotated[1], rotated[2])

def rotateX(angle, obj):
    angle = np.sign(angle) * 0.01
    X = [
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
    for index, p in enumerate(obj.points):
        rotated = np.dot(X, p)
        obj.points[index] = (rotated[0], rotated[1], rotated[2])

def rotateY(angle, obj):
    angle = np.sign(angle) * 0.01
    Y = [
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]
    for index, p in enumerate(obj.points):
        rotated = np.dot(Y, p)
        obj.points[index] = (rotated[0], rotated[1], rotated[2])