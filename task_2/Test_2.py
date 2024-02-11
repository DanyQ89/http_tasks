d = {'lowerCorner': '37.602175 55.820572', 'upperCorner': '37.610386 55.825194'}


def func_coords(some_dict):
    some_dict = list(map(lambda x: [float(x[1].split()[0]), float(x[1].split()[1])], list(some_dict.items())))
    spn_1 = some_dict[1][0] - some_dict[0][0]
    spn_2 = some_dict[1][1] - some_dict[0][1]
    return str(round(spn_1, 5)), str(round(spn_2, 5))


# print(func_coords(d))
import math
def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return round(distance)


# print(lonlat_distance((37.6222, 55.7566), (37.6589, 55.7583)))

