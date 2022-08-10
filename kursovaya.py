import requests
from pprint import pprint

vk_user_id = 1
with open('token_VK.txt', 'r') as file_object:
    token_VK = file_object.read().strip()

with open('token_YA.txt', 'r') as file_object:
    token_YA = file_object.read().strip()


class VK_and_YA_upload_files:
    def __init__(self, token_vk, token_ya, vk_user_id):

        self.token_vk = token_vk
        self.token_ya = token_ya
        self.photos_info = []
        self.vk_user_id = vk_user_id

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }

    def get_foto_data(self):
        api = requests.get("https://api.vk.com/method/photos.get",
                           params={
                               'owner_id': self.vk_user_id,
                               'access_token': self.token_vk,
                               'offset': 0,
                               'count': 2,
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
        # pprint(self.photos_info)

    def folder(self):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.folder = 'vk'
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
        response = requests.post(upload_url, headers=headers, params=params)
        print(response.status_code)


vk = VK_and_YA_upload_files(token_VK, token_YA, 1)
vk.folder()
vk.get_foto_data()

# vk.new_download()
for i in vk.photos_info:
    vk.downloads_photos(i['url'], f"vk/{i['file_name']}")
