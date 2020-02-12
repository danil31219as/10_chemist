from coordinates import get_coor
from scale import set_spn
import requests
from io import BytesIO
from PIL import Image


def set_centr(coor_1, coor_2):
    x1, y1 = coor_1
    x2, y2 = coor_2
    return [str((x1 + x2) / 2), str((y1 + y2) / 2)]


address_ll = ','.join(get_coor(input()).split())
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
addresses = []
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
json_response = response.json()
min_x = None
max_x = None
min_y = None
max_y = None
for i in range(10):
    organization = json_response["features"][i]
    time_of_work = organization["properties"]["CompanyMetaData"]
    if 'Hours' in time_of_work:
        time_of_work = time_of_work['Hours']['text']
        if 'круглосуточно' in time_of_work.lower():
            color = 'pm2gnm'
        else:
            color = 'pm2blm'
    else:
        color = 'pm2grm'
    point = organization["geometry"]["coordinates"]
    x, y = map(float, point)
    if not min_x or x < min_x:
        min_x = x
    if not max_x or x > max_x:
        max_x = x
    if not min_y or y < min_y:
        min_y = y
    if not max_y or y > max_y:
        max_y = y
    org_point = "{0},{1}".format(point[0], point[1])
    addresses.append([org_point, color])
map_params = {
    "ll": ','.join(set_centr((min_x, min_y), (max_x, max_y))),
    "spn": ",".join(set_spn(str(min_x) + ',' + str(min_y),
                            str(max_x + 0.0002) + ',' + str(max_y + 0.0002))),
    "l": "map",
    "pt": '~'.join([','.join(elem) for elem in addresses])
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
if response:
    Image.open(BytesIO(
        response.content)).show()
else:
    print("Http статус:", response.status_code, "(", response.reason, ")")
