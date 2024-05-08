import math
import numpy as np


def rotateZ(angle, obj):
    """
        Поворачивает объект вокруг оси Z на заданный угол.

        Параметры:
        angle (float): Угол поворота в радианах.
        obj (объект): Объект, который будет повернут.

        Возвращаемое значение:
        None: Функция напрямую изменяет объект `obj`, модифицируя его атрибут `points`.
    """
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
    """
        Поворачивает объект вокруг оси X на заданный угол.

        Параметры:
        angle (float): Угол поворота в радианах.
        obj (объект): Объект, который будет повернут.

        Возвращаемое значение:
        None: Функция напрямую изменяет объект `obj`, модифицируя его атрибут `points`.
    """
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
    """
        Поворачивает объект вокруг оси Y на заданный угол.

        Параметры:
        angle (float): Угол поворота в радианах.
        obj (объект): Объект, который будет повернут.

        Возвращаемое значение:
        None: Функция напрямую изменяет объект `obj`, модифицируя его атрибут `points`.
    """
    angle = np.sign(angle) * 0.01
    Y = [
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]
    for index, p in enumerate(obj.points):
        rotated = np.dot(Y, p)
        obj.points[index] = (rotated[0], rotated[1], rotated[2])


def scale(coefficient, obj):
    """
        Масштабирует все точки объекта на заданный коэффициент.

        Параметры:
        coefficient (float): Коэффициент масштабирования. Значение больше 1 увеличивает объект,
                         значение меньше 1 уменьшает объект, значение равное 1 оставляет размер объекта неизменным.
        obj (объект): Объект, который будет масштабирован.

        Возвращаемое значение:
        None: Функция напрямую изменяет объект `obj`, модифицируя его атрибут `points`.
    """
    scale = [
        [coefficient, 0, 0],
        [0, coefficient, 0],
        [0, 0, coefficient]
    ]
    for index, p in enumerate(obj.points):
        scaled = np.dot(scale, p)
        obj.points[index] = (scaled[0], scaled[1], scaled[2])


def move(coefficient_x, coefficient_y, obj):
    """
       Смещает все точки объекта на заданные коэффициенты по осям X и Y.

       Параметры:
       coefficient_x (float): Коэффициент смещения по оси X. Знак определяет направление смещения.
       coefficient_y (float): Коэффициент смещения по оси Y. Знак определяет направление смещения.
       obj (объект): Объект, который будет смещен.

       Возвращаемое значение:
       None: Функция напрямую изменяет объект `obj`, модифицируя его атрибут `points`.
    """
    coefficient_x = np.sign(coefficient_x) * 0.005
    coefficient_y = np.sign(coefficient_y) * 0.005
    for index, p in enumerate(obj.points):
        obj.points[index] = (p[0] - coefficient_x, p[1] - coefficient_y, p[2])
