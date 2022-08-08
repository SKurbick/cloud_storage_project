import requests
from pprint import pprint

####  ПРОГРАММА ДЛЯ ПРОСМОТРА ВСЕХ ФОТОГРАФИЙ(АВАТАРОК) ПОЛЬЗОВАТЕЛЕЙ С ВКОНТАКТЕ + её определенные данные       #######
##########   СОХРАНЯЕМ ОТДЕЛЬНО В JSON ФОРМАТЕ В ЗАДАННОЙ ПЕРЕМЕННОЙ      ##############################################

vk_user_id = 184465493  # id пользователя, у которого будут читаться аватарки
with open('token_VK.txt', 'r') as file_object:#читаем токен с вк для дальнейшей работы
    token = file_object.read().strip()


def get_foto_data(offset=0, count=10):# в первом аргументе задана по умолчания время на итерацию, во втором:
                                                                            # колличество значений для чтения
    api = requests.get("https://api.vk.com/method/photos.get", # url c методом чтения фотографий
                       params={
                           'owner_id': vk_user_id, # ввели нашего пользователя
                           'access_token': token, #токен для аутентификации
                           'offset': offset,
                           'count': count,
                           'photo_size': 0,
                           'extended': 1, # 1 - в апи вк значит дополнительные данные по фото в ключе "extended"
                           'v': 5.131,
                           'album_id': 'profile', # выбираем значение "profile" - работа с аватарками

                       })
    photos_info = [] # список в который будем добавлять словари с данными по фото
    for data in api.json()['response']['items']:#обращаемся в json конкретно к определенным значениям, которые нам нужны
                                                        #а именно:

        photo_info = {
            'file_name': f"{data['likes']['count']}.png", # добавляя файл с фото мы именуем его с кол-ом лайков, которое набрало фото
            'url': data['sizes'][-1]['url'], #в текущий словарь добавляем конкретный максимальный размер из выбранного
            'size': data['sizes'][-1]['type'] #сохраняем данные с выбранным размером
        }

        for photo in photos_info: #этот цикл переименовывает фото, если вдруг колличество лайков совпадало и разных фото
            # что бы не было повторений в наименованиях, переименуем фото с повторяющимся названием,на название
            #                                                                                даты её добавления
            if photo['file_name'] == f"{data['likes']['count']}.png":
                photo_info['file_name'] = f"{data['date']}.png"

        photos_info.append(photo_info)

    pprint(photos_info)


get_foto_data()
