from vk import VkUser
from yandex_disk import YaUploader
from google_drive import upload_photos_to_drive
import config

if __name__ == '__main__':
    vk_client = VkUser(config.VK_TOKEN, '5.131')
    uploader = YaUploader(config.YA_TOKEN)
    print(vk_client.get_albums('1785302'))
    print(vk_client.get_highest_res_profile_photos(user_id='1785302', count='5', album_id='178274560'))
    print(uploader.batch_upload_from_vk())
    print(upload_photos_to_drive())
