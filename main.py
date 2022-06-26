from vk import VkUser
from yandex_disk import YaUploader

with open('vk_token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
with open('ya_token.txt', 'r') as file_object:
    ya_token = file_object.read().strip()

if __name__ == '__main__':
    vk_client = VkUser(vk_token, '5.131')
    uploader = YaUploader(ya_token)
    print(vk_client.get_highest_res_profile_photos('621696536', '5'))
    print(uploader.batch_upload_from_vk())
