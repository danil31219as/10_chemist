def set_spn(coor_1, coor_2):
    x1, y1 = map(float, coor_1.split(','))
    x2, y2 = map(float, coor_2.split(','))
    return [str(abs(x2 - x1)), str(abs(y2 - y1))]