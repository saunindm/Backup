import requests
import os
import json
from log_func import log_func


BASE_PATH = os.getcwd()
PHOTOS_DIR_NAME = 'vk_photos'
FULL_PATH = os.path.join(BASE_PATH, PHOTOS_DIR_NAME)
LOGS_FILE_NAME = 'logs.txt'


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload_from_vk(self, file_path: str, file_name: str):
        '''Метод для загрузки фото на Я.Диск и записи лога загрузки в logs.txt.
        '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {
            'path': file_path,
            'overwrite': "true"
        }
        local_file_path = 'vk_photos'
        file_name = os.path.join(local_file_path, file_name)
        response = requests.get(upload_url, headers=headers, params=params)
        href = response.json().get('href', "")
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        file_name = file_name[10:]
        if response.status_code == 201:
            res = f"File {file_name} | uploaded to Yandex.Disk to folder D:\YandexDisk\{file_path}"
            print(res)
            log_func(LOGS_FILE_NAME, res)

    def batch_upload_from_vk(self):
        '''Метод для пакетной загрузки фото на Я.Диск.
        Метод создает json-файл с информацией по загруженным фото.
        '''
        with open("photos_downloaded.json", 'r', encoding='utf-8') as f:
            photos = json.load(f)
            for photo in photos:
                file_path = f"Netology\VK_photos\{photo['file_name']}"
                self.upload_from_vk(file_path, f"{photo['file_name']}")
            print('Upload completed.')
        with open("photos_saved.json", 'w', encoding='utf-8') as f:
            json.dump(photos, f, ensure_ascii=False, indent=4)
        return f'File "photos_saved.json created.\n' \
               f'File {LOGS_FILE_NAME} updated.\n'
