d = {'lowerCorner': '37.602175 55.820572', 'upperCorner': '37.610386 55.825194'}


def func_coords(some_dict):
    some_dict = list(map(lambda x: [float(x[1].split()[0]), float(x[1].split()[1])], list(some_dict.items())))
    spn_1 = some_dict[1][0] - some_dict[0][0]
    spn_2 = some_dict[1][1] - some_dict[0][1]
    return str(round(spn_1, 5)), str(round(spn_2, 5))

# print(func_coords(d))
