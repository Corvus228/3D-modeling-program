def readfile(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines