def readfile(filename):
    """
        Читает все строки из файла и возвращает их как список.

        Параметры:
        filename (str): Путь к файлу, который необходимо прочитать.

        Возвращаемое значение:
        list: Список строк из файла.
    """
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines