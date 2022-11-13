from token_file import token_YA, token_vk_app
from VK_profile_upload import VKProfileUpload
from YandexDisk import YandexDisk
from progress.bar import IncrementalBar
import json


def save_photos_in_cloud(user_id_input, photos_count, folder):
    json_files_photos = []
    vk = VKProfileUpload(token_vk=token_vk_app, user_id=user_id_input, count=photos_count)
    ya = YandexDisk(token_ya=token_YA, folder=folder)
    vk.get_photos_data()
    ya.create_folder()
    bar = IncrementalBar('photo', max=len(vk.photos_info))
    for elem in vk.photos_info:
        bar.next()
        ya.downloads_photos(elem['url'], f"{folder}/{elem['file_name']}")
        elem.pop("url")
        json_files_photos.append(elem)
    bar.finish()
    print("Фотографии успешно загружены")
    with open('json.json', 'w') as jsf:
        json.dump(json_files_photos, jsf)


if __name__ == '__main__':
    user_id_input = 1
    photos_count = 3
    folder = "the_folder"
    save_photos_in_cloud(user_id_input, photos_count, folder)
