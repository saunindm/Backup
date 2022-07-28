from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from log_func import log_func
import json

# Первоначальная аутентификация настроена с помощью файла clients_secrets.json (содержит всю аутентификационную информацию
# приложения из API Google Console для доступа к Google Drive). При таком варианте программа каждый раз запрашивает
# веб-аутентификацию (логин и пароль Google аккаунта). Чтобы не вводить пароли каждый раз, в рабочем каталоге создан
# файл settings.yaml для сохранения всех учетных данных. С этим файлом вам все равно придется использовать браузер для
# завершения аутентификации в первый раз, и после этого файл credentials.json будет сгенерирован в рабочем каталоге с
# При его наличии LocalWebserverAuth() сгенерирует в рабочем каталоге файл credentials.json с токеном, и завершает
# автоматическую аутентификацию без пользовательского ввода.


gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # метод GoogleAuth, который устанавливает локальный веб-сервер для автоматического получения
# токена из файла credentials.json от пользователя и его самостоятельной авторизации
drive = GoogleDrive(gauth)
BASE_PATH = os.getcwd()
PHOTOS_CATALOG_PATH = 'vk_photos'
LOGS_FILE_NAME = 'logs.txt'


def upload_photos_to_drive():
    with open("photos_downloaded.json", 'r', encoding='utf-8') as f:
        files_list = json.load(f)
    for x in files_list:
        f = drive.CreateFile({'title': x['file_name'], 'parents': [{'id': '1Hrxny2LpCHqm2X7w-coRx5KoipqdzRnR'}]})  # id папки в Google Drive, куда загружаются фото
        f.SetContentFile(os.path.join(PHOTOS_CATALOG_PATH, x['file_name']))
        f.Upload()
        res = f"File {x['file_name']} | uploaded to Google drive to G:Мой Диск\\Neto_photos"
        print(res)
        log_func(LOGS_FILE_NAME, res)
    return f'File {LOGS_FILE_NAME} updated.\n'
