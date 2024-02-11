import pprint
import sys
import math
import requests
from Test_2 import lonlat_distance
import pygame
# py Test.py Москва, ул. Ак. Королева, 12


toponym_to_find = " ".join(sys.argv[1:])
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

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"].replace(' ', ',')


# toponym_coodrinates = '37.606281,55.822883'

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key_2 = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
search_api_server_params = {
    'apikey': api_key_2,
    'text': 'аптека',
    'lang': 'ru_RU',
    'll': toponym_coodrinates,
    'type': 'biz'
}


res = requests.get(search_api_server, params=search_api_server_params).json()
need = res['features'][0]['properties']['CompanyMetaData']

coords_of_apteka = res['features'][0]['geometry']['coordinates']
name_of_apteka = need['Categories'][0]['name']
time_of_apteka = need['Hours']['Availabilities']
distance_to_apteka = lonlat_distance(list(map(float, toponym_coodrinates.split(','))) , coords_of_apteka)

# print(coords_of_apteka, name_of_apteka, time_of_apteka, distance_to_apteka)

pygame.init()
screen = pygame.display.set_mode((1500, 500))

font = pygame.font.Font(None, 21)

need_t = [name_of_apteka, ' '.join(map(str, coords_of_apteka)), str(time_of_apteka), str(distance_to_apteka)]
y = 0
for i in need_t:
    text = font.render(i, True, 'white')
    screen.blit(text, (0, y))
    y += 35

pygame.display.flip()

while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

