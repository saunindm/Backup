from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from log_func import log_func
import json

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
BASE_PATH = os.getcwd()
PHOTOS_CATALOG_PATH = 'vk_photos'
LOGS_FILE_NAME = 'logs.txt'


def upload_photos_to_drive():
    with open("photos_downloaded.json", 'r', encoding='utf-8') as f:
        files_list = json.load(f)
    for x in files_list:
        f = drive.CreateFile({'title': x['file_name'], 'parents': [{'id': '1Hrxny2LpCHqm2X7w-coRx5KoipqdzRnR'}]})
        f.SetContentFile(os.path.join(PHOTOS_CATALOG_PATH, x['file_name']))
        f.Upload()
        res = f"File {x['file_name']} | uploaded to Google drive to G:Мой Диск\\Neto_photos"
        print(res)
        log_func(LOGS_FILE_NAME, res)
    return f'File {LOGS_FILE_NAME} updated.\n'
