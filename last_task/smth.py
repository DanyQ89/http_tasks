# эта игра сделана по принципу произовльного введения городов, координаты которых будут 
# высвечиваться на экране. После того, как пользователь угадывает город, ему нужно будет нажать на
# кнопку своей мыши (для начала игры также потребуется нажать на кнопку мыши) 


import os
import pprint
import sys
import math
import requests
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 450))


# py Test.py Москва, ул. Ак. Королева, 12

def get_coords(name):
    # toponym_to_find = " ".join(sys.argv[1:])
    toponym_to_find = name
    api_key = '40d1649f-0493-4b70-98ba-98533de7710b'

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": api_key,
        "geocode": toponym_to_find,
        "format": "json",
        'kind': 'district'
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"].replace(' ', ',')

    # toponym_coodrinates = '37.606281,55.822883'
    return toponym_coodrinates
    # search_api_server = "https://search-maps.yandex.ru/v1/"


def show_img(coords):
    url = f'http://static-maps.yandex.ru/1.x/'

    params = {
        'll': coords,
        'spn': '0.005,0.005',
        'l': 'map'
    }
    a = requests.get(url, params=params)

    map_file = 'map.png'
    with open(map_file, 'wb') as file:
        file.write(a.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


names_of_cities = ['Сан-Диего', 'Токио', 'Хабаровск']
running = True


def func():
    ind = input('Введите город или слово НЕТ, если не хотите играть:\n')
    if not ind.isdigit():
        if ind == 'НЕТ':
            running = False
    show_img(get_coords(ind))


func()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            func()
# os.remove(map_file)
pygame.quit()
