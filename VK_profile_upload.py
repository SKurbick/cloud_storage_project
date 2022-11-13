import requests


class VKProfileUpload:
    def __init__(self, token_vk, user_id=1, count=3):
        self.token_vk = token_vk
        self.user_id = user_id
        self.count = count
        self.photos_info = []  # основные данные

    def get_photos_data(self):
        api = requests.get(f"https://api.vk.com/method/photos.get",

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

        status_code = api.status_code
        for data in api.json()['response']['items']:

            photo_info = {
                'file_name': f"{data['likes']['count']}.png",
                'url': data['sizes'][-1]['url'],
                'size': data['sizes'][-1]['type'],
            }
            for photo in self.photos_info:
                if photo['file_name'] == f"{data['likes']['count']}.png":
                    photo_info['file_name'] = f"{data['date']}.png"

            self.photos_info.append(photo_info)
        return status_code  # для unittest проверки


