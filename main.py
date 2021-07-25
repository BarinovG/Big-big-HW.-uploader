import json
import datetime
import requests
from tqdm import tqdm
from pprint import pprint

class VK_user:
    url = 'https://api.vk.com/method/'

    def __init__(self, token,version):
        self.params = {
            'access_token': token,
            'v' : version
        }

    def get_inf_photos(self, owner_id):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id' : owner_id,
            'album_id' : "profile",
            'extended' : 1,
            'photo_sizes' : 'z',
            'count' : 5,
            'rev' : 0
        }
        req = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return req['response']['items']

    def get_url_photos(self, owner_id):
        urls = []
        names = []
        all_inf = self.get_inf_photos(owner_id)
        for inf in all_inf:
            for count_likes in inf['likes'].items():
                if count_likes[0] == 'count':
                    if str(count_likes[1]) in names:
                        date_unix = inf['date']
                        date = datetime.datetime.fromtimestamp(date_unix)
                        date = f'{date:%Y-%m-%d %H.%M.%S}'
                        names.append(f"{str(count_likes[1])} - {date}")
                    else:
                        names.append(f"{str(count_likes[1])}")
            for url in inf['sizes'][-1].items():
                if url[0] == 'url':
                    urls.append(url[1])
        url_photos_dict = dict(zip(names, urls))
        return url_photos_dict

    def get_size_photos(self, owner_id):
        types = []
        all_inf = self.get_inf_photos(owner_id)
        for inf in all_inf:
            for size in inf['sizes'][-1].items():
                if size[0] == 'type':
                    types.append(size[1])
        return types

class Yandex_user():
    uri = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.token = YAtoken

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def newfolder(self):
        folderName = str(input('Введите название папки для сохранения фотографий на Яндекс Диске: '))
        newfolder_url = self.uri + 'v1/disk/resources'
        headers = self.get_headers()
        params = {"path": folderName, "overwrite": "true"}
        response = requests.put(newfolder_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка с именем "{folderName}" создана.')
        return folderName

    def upload_by_url(self, name_url_dict,folderName, photo_type):
        data = {}
        upload_url = self.uri + 'v1/disk/resources/upload'
        headers = self.get_headers()
        for vk_name, vk_url in tqdm(name_url_dict.items()):
            params = {"path": str(folderName) + '/' + str(vk_name) + '.jpg', "url" : vk_url, "overwrite": "true"}
            response = requests.post(upload_url, headers=headers, params=params)
            if response.status_code == 202:
                data['file_name'] = [vk_name]
                for type in photo_type:
                    data['size'] = [type]
                with open("data_file.json", "a") as f:
                    json.dump(data, f)
                    print(f'Информация о загрузке {vk_name}.jpg добавлена в json')
        pprint(response.json())
        return response.json()

if __name__ == '__main__':

    with open('api_vk.txt', encoding='utf-8') as f:
        VKtoken = f.read()
    with open('yaToken.txt', encoding='utf-8') as f:
        YAtoken = f.read()
    Im_ya = Yandex_user(YAtoken)
    Im_VK = VK_user(VKtoken, '5.131')
    Im_ya.upload_by_url(Im_VK.get_url_photos(''), Im_ya.newfolder(), Im_VK.get_size_photos(''))


