import json
import requests
import time
from tqdm import tqdm


def get_photos(owner_id, token_vk, version=5.131, album_id='profile', extended='1',
               url='https://api.vk.com/method/photos.get'):
    params = {
        'access_token': token_vk,
        'owner_id': owner_id,
        'album_id': album_id,
        'extended': extended,
        'v': version
    }
    res = requests.get(url, params=params)
    response = json.loads(res.text)
    file_names_and_sizes = []
    print('Получаем фотографии:')
    for item in tqdm(response['response']['items']):
        for size in item['sizes']:
            if size['type'] == 'z':
                file_names_and_sizes.append(
                    {'filename': str(item['id']) + str(item['likes']['count']) + str(item['date']) + '.jpg',
                     'size': 'z', 'url': size['url']})
        time.sleep(1)
    with open('data.json', 'w') as f:
        json.dump(file_names_and_sizes, f, indent='\t')
    return file_names_and_sizes


def upload_photos(token_ya_disk, file_names_and_sizes, url='https://cloud-api.yandex.net/v1/disk/resources/upload',
                  path='VK_Photos_Backup'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(token_ya_disk)
    }
    params = {
        'path': path
    }
    print('Отправляем фотографии:')
    res = requests.put('https://cloud-api.yandex.net/v1/disk/resources/', headers=headers, params=params)
    folder = json.loads(res.text)
    for photo in tqdm(file_names_and_sizes):
        params_for_put = {
            'path': path + '/' + photo['filename'],
            'url': photo['url']
        }
        result = requests.post(url, headers=headers, params=params_for_put)
        time.sleep(1)


owner_id = input('Введите ID пользователя: ')
token_vk = input('Введите токен для аутентификации VK: ')
token_ya_disk = input('Введите токен для аутентификации Ya_Disk: ')
# owner_id = '705300120'
# with open('token_VK.txt', 'r') as f:
#     token_VK = f.read().strip()
# with open('token_Ya_Disk.txt', 'r') as f:
#     token_ya_disk = f.read().strip()
file_names_and_sizes = get_photos(owner_id, token_vk)
upload_photos(token_ya_disk, file_names_and_sizes)
