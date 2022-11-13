import requests


class YandexDisk:
    def __init__(self, token_ya, folder):
        self.folder = folder
        self.token_ya = token_ya

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }

    def create_folder(self):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': f'/{self.folder}'}
        headers = self.get_headers()
        response = requests.put(upload_url, headers=headers, params=params)
        create_folder_status_code = response.status_code
        if create_folder_status_code == 201:
            print(f"Folder {self.folder} successfully created on Yandex Disk")

        elif create_folder_status_code == 409:
            print(f"The folder {self.folder} already exists on Yandex Disk")

        return create_folder_status_code

    def downloads_photos(self, url, path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {'url': url, 'path': path}
        headers = self.get_headers()
        requests.post(upload_url, headers=headers, params=params)


