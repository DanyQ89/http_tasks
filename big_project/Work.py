import sys

import PyQt5.uic
import requests
from PyQt5.Qt import QMainWindow, QApplication, QPixmap


def get_img(name_func, spn_func):
    url = 'http://geocode-maps.yandex.ru/1.x/'
    api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
    name = name_func
    params = {
        'apikey': api_key,
        'geocode': name,
        'format': 'json'
    }

    res = requests.get(url, params=params).json()
    coord_1, coord_2 = [float(i) for i in
                        res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()]

    url_map = 'http://static-maps.yandex.ru/1.x/'

    params_map = {
        'l': 'map',
        'll': f'{coord_1},{coord_2}',
        'spn': f'{spn_func},{spn_func}'
    }
    img = requests.get(url_map, params=params_map).content

    with open('img.txt', 'wb') as file:
        file.write(img)


class Map(QMainWindow):
    def __init__(self):
        super().__init__()

        PyQt5.uic.loadUi('map_ui.ui', self)
        self.initUI()
        self.spn = 0.05
        self.address = 'США Гарвард'
        self.main_button.clicked.connect(self.show_map)

    def show_map(self):
        try:
            self.spn = float(self.line_spn.text())
            print(1)
            self.address = self.address_text.toPlainText()
            print(2)
        except (ValueError, TypeError):
            pass
        print(self.spn, self.address)
        # get_img(self.address, self.spn)
        self.label_for_map.setPixmap(QPixmap('img.txt'))

    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
