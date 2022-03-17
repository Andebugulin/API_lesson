import requests
from api import *
import sys
from PIL import Image
import pprint
from io import BytesIO

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]

# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")













api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_api_server = "https://search-maps.yandex.ru/v1/"
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "type": "biz"
}


response_2 = requests.get(search_api_server, params=search_params)
if not response_2:
    # ...
    pass

# Преобразуем ответ в json-объект
json_response_2 = response_2.json()

organization = json_response_2["features"][0]

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
delta = sizes(response)

api_key = "..."
zap = "https://api.routing.yandex.net/v2/route"
params_z = {
    "apikey": api_key,
    "waypoints": ','.join([toponym_longitude, toponym_lattitude]) + '|' + org_point
}
resp = requests.get(zap, params=params_z)
print(resp)
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(delta),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt":org_point + '~' + ",".join([toponym_longitude, toponym_lattitude])

}

map_api_server = "http://static-maps.yandex.ru/1.x/"

response_3 = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response_3.content)).show()
