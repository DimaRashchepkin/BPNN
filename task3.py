import os
import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"
print('Все вводимые данные должны быть в виде целых '
      'десятичных чисел(с точкой)')
lon = input("Введите долготу (от -179 до 179): ")
lat = input("Широту (от -80 до 80): ")
delta = input('Масштаб (от 0 до 90): ')
size = width, height = 600, 450
screen = pygame.display.set_mode(size)
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def request():
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "sat"
    }
    response = requests.get(api_server, params=params)
    if response:
        f = open("map.png", 'wb')
        f.write(response.content)
        f.close()
    else:
        print("Ошибка выполнения запроса:")
        print(api_server, params)
        print("Http статус:", response.status_code, "(", response.reason, ")")


running = True
request()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if -80 <= float(lat) + 0.1 * float(delta) <= 80:
                    lat = str(float(lat) + 0.1 * float(delta))
                    request()
            elif event.key == pygame.K_DOWN:
                if -80 <= float(lat) - 0.1 * float(delta) <= 80:
                    lat = str(float(lat) - 0.1 * float(delta))
                    request()
            elif event.key == pygame.K_LEFT:
                if -179 <= float(lon) - 0.1 * float(delta) <= 179:
                    lon = str(float(lon) - 0.1 * float(delta))
                    request()
            elif event.key == pygame.K_RIGHT:
                if -179 <= float(lon) + 0.1 * float(delta) <= 179:
                    lon = str(float(lon) + 0.1 * float(delta))
                    request()
            elif event.key == pygame.K_PAGEUP:
                if 0 < float(delta) / 1.8 < 90:
                    delta = str(float(delta) / 1.8)
                    request()
            elif event.key == pygame.K_PAGEDOWN:
                if 0 < float(delta) * 1.8 < 90:
                    delta = str(float(delta) * 1.8)
                    request()

    image = load_image('map.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()

os.remove('map.png')
pygame.quit()
