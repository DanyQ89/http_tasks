import sys

import PyQt5.uic
import requests
from PyQt5.Qt import QMainWindow, QApplication, QPixmap, QButtonGroup


def get_img(name_func, spn_func, map_func=None, coord_1_func=None, coord_2_func=None, metki_func=[]):
    if not coord_1_func or not coord_2_func:
        url = 'http://geocode-maps.yandex.ru/1.x/'
        api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
        params = {
            'apikey': api_key,
            'geocode': name_func,
            'format': 'json'
        }

        res = requests.get(url, params=params).json()
        coord_1, coord_2 = [float(i) for i in
                            res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                                'pos'].split()]
    else:
        coord_1 = coord_1_func
        coord_2 = coord_2_func
        
    m = f'{coord_1},{coord_2}'
    if m not in metki_func:
        metki_func.append(m)
        
    url_map = 'http://static-maps.yandex.ru/1.x/'

    params_map = {
        'l': map_func,
        'll': f'{coord_1},{coord_2}',
        'spn': f'{spn_func},{spn_func}',
        'pt': '~'.join(metki_func)
    }

    img = requests.get(url_map, params=params_map).content
    with open('img.txt', 'wb') as file:
        file.write(img)
    return (coord_1, coord_2, metki_func)


class Map(QMainWindow):
    def __init__(self):
        super().__init__()

        PyQt5.uic.loadUi('map_ui.ui', self)
        self.initUI()
        self.spn = 0.05
        self.address = 'США Гарвард'
        self.main_button.clicked.connect(self.show_map)
        self.coord_1 = None
        self.coord_2 = None
        self.map = 'map'
        self.radio_map.setChecked(True)
        self.radio_group_buttons = QButtonGroup(self.radio_group)
        self.metka_now = ''
        self.metki_all = []

        for i in [self.radio_hybrid, self.radio_map, self.radio_sputnik]:
            self.radio_group_buttons.addButton(i)

    def show_map(self):
        try:
            self.spn = float(self.line_spn.text())
            if not self.address_text.toPlainText().isnumeric():
                self.address = self.address_text.toPlainText()
        except (ValueError, TypeError):
            pass

        map_text = self.radio_group_buttons.checkedButton().text()
        if map_text == '':
            self.map = 'map'
        elif map_text == 'гибрид':
            self.map = 'hybrid'
        else:
            self.map = 'satellite'

        self.coord_1, self.coord_2, self.metki_all = get_img(self.address, self.spn, self.map, self.coord_1,
                                                             self.coord_2, metki_func=self.metki_all)

        self.label_for_map.setPixmap(QPixmap('img.txt'))

    def keyPressEvent(self, e):
        print(1)
        num = self.spn + 0
        if e.key() == 16777238:  # spn up
            if self.spn < 0.9:
                self.spn += 0.01
        elif e.key() == 16777239:  # spn down
            if self.spn > 0.00001:
                self.spn -= 0.01
        elif e.key() == 16777235:  # button up
            if self.coord_2 + num / 2 <= 90.0:
                self.coord_2 += num / 2
        elif e.key() == 16777237:  # button down
            if self.coord_2 - num / 2 >= -90.0:
                self.coord_2 -= num / 2
        elif e.key() == 'right_button':
            if self.coord_1 + num / 2 <= 180.0:
                self.coord_1 += num / 2
        elif e.key() == 'left_button':
            if self.coord_1 - num / 2 >= -180.0:
                self.coord_1 -= num / 2

        self.show_map()

    def initUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
