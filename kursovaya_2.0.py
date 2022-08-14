import requests
import json
from progress.bar import IncrementalBar

with open('token_VK.txt', 'r') as file_object:
    token_VK = file_object.read().strip()

with open('token_YA.txt', 'r') as file_object:
    token_YA = file_object.read().strip()


class VkProfileUpload:
    def __init__(self, token_vk, user_id, count):
        self.token_vk = token_vk
        self.user_id = user_id
        self.photos_info = []
        self.count = count

    def get_foto_data(self):
        api = requests.get("https://api.vk.com/method/photos.get",
                           params={
                               'owner_id': self.user_id,
                               'access_token': self.token_vk,
                               'offset': 0,
                               'count': self.count,
                               'photo_size': 0,
                               'extended': 1,
                               'v': 5.131,
                               'album_id': 'profile',

                           })

        for data in api.json()['response']['items']:

            photo_info = {
                'file_name': f"{data['likes']['count']}.png",
                'url': data['sizes'][-1]['url'],
                'size': data['sizes'][-1]['type']
            }

            for photo in self.photos_info:
                if photo['file_name'] == f"{data['likes']['count']}.png":
                    photo_info['file_name'] = f"{data['date']}.png"

            self.photos_info.append(photo_info)


class YaDiskUpload:
    def __init__(self, folder, token_ya):
        self.folder = folder
        self.token_ya = token_ya

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }

    def add_folder(self):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': f'/{self.folder}'}
        headers = self.get_headers()
        response = requests.put(upload_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка {self.folder} успешно создана на яндекс.диске.')
        elif response.status_code == 409:
            print(f'Папка {self.folder} уже существует на яндекс.диске.')

    def downloads_photos(self, url, path):

        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {'url': url, 'path': path}
        headers = self.get_headers()
        requests.post(upload_url, headers=headers, params=params)


user_id_input = input('введите id пользователя')
photos_count = input('введите колличество фото для загрузки:')

vk = VkProfileUpload(token_VK, user_id_input, photos_count)
ya = YaDiskUpload('vk', token_YA)
vk.get_foto_data()
ya.add_folder()

bar = IncrementalBar('photo', max=len(vk.photos_info))
for el in vk.photos_info:
    bar.next()
    ya.downloads_photos(el['url'], f"vk/{el['file_name']}")
bar.finish()
print("Фотографии успешно загружены")

json_file = []
for js in vk.photos_info:
    b = js.pop("url")
    json_file.append(js)

with open('json.json', 'w') as jsf:
    json.dump(json_file, jsf)
