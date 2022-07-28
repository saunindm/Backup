import requests
import os
from datetime import datetime
import json
from log_func import log_func

BASE_PATH = os.getcwd()
PHOTOS_DIR_NAME = 'vk_photos'
FULL_PATH = os.path.join(BASE_PATH, PHOTOS_DIR_NAME)
LOGS_FILE_NAME = 'logs.txt'


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_albums(self, owner_id):
        info_albums_dict = {}
        get_albums_url = self.url + 'photos.getAlbums'
        get_albums_params = {
            'owner_id': owner_id,
        }
        res = requests.get(get_albums_url, params={**self.params, **get_albums_params}).json()
        data = res['response']['items']
        for album in data:
            info_albums_dict[album['title']] = album['id']
        return info_albums_dict

    def get_highest_res_profile_photos(self, user_id=None, count=None, album_id='profile'):
        '''Метод для скачивания фото с профиля пользователя VK в максимальном размере.
        Для названий фотографий используется количество лайков, если количество лайков одинаково, то добавляется дата загрузки.
        Метод создает json-файл с информацией по скачанным фото и записывает лог скачивания в logs.txt.
        '''
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': user_id,
            'album_id': album_id,
            'count': count,
            'extended': 1
        }
        response = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        photos_data = response['response']['items']
        photos_list = []
        photo_dict = {}
        for photo in photos_data:
            photo_dict['file_name'] = f"{photo['likes']['count']}.jpg"
            photo_dict['size'] = photo['sizes'][-1]['type']
            photo_dict['url'] = photo['sizes'][-1]['url']
            photo_dict['date'] = datetime.utcfromtimestamp(int(photo['date'])).strftime('%Y-%m-%d')
            photo_dict['likes'] = photo['likes']['count']
            photos_list.append(photo_dict)
            photo_dict = {}
        with open("photos_downloaded.json", 'w', encoding='utf-8') as f:
            json.dump(photos_list, f, ensure_ascii=False, indent=4)
        file_names_list = []
        for photo in photos_list:
            response = requests.get(photo['url'])
            if f"{photo['file_name']}" not in file_names_list:
                file_name = f"{photo['likes']}.jpg"
            else:
                file_name = f"{photo['likes']}-{photo['date']}.jpg"
            file_names_list.append(file_name)
            with open(os.path.join(FULL_PATH, file_name), 'wb') as f:
                f.write(response.content)
            if response.status_code == 200:
                res = f"File {file_name} | downloaded from VK to folder {FULL_PATH}"
                print(res)
                print(log_func(LOGS_FILE_NAME, res))
        return f'Download completed.\n' \
               f'File photos_downloaded.json created.\n' \
               f'File {LOGS_FILE_NAME} created.\n'
