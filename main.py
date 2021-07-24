import requests
from pprint import pprint
import datetime
from tqdm import tqdm

with open('api_vk.txt', encoding='utf-8') as f:
    VKtoken = f.read()

with open('yaToken.txt', encoding='utf-8') as f:
    YAtoken = f.read()

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
        # pprint(url_photos_dict)
        return url_photos_dict

Im_VK = VK_user(VKtoken, '5.131')

# pprint(Im_VK.get_inf_photos('17335094'))
# Im_VK.get_url_photos('552934290')

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
        response.raise_for_status()
        if response.status_code == 201:
            print(f'Папка с именем "{folderName}" создана. Начинаем копирование фотографий с вашего ВК')
        return folderName

    def upload_by_url(self, name_url_dict,folderName):
        upload_url = self.uri + 'v1/disk/resources/upload'
        headers = self.get_headers()
        for vk_name, vk_url in name_url_dict.items():
            params = {"path": str(folderName) + '/' + str(vk_name) + '.jpg', "url" : vk_url, "overwrite": "true"}
            response = requests.post(upload_url, headers=headers, params=params)
            if response.status_code == 202:
                print(f'Фотография "{vk_name}".jpg загружена.')
        print(response.json())
        return response.json()


Im_ya = Yandex_user(YAtoken)

Im_ya.upload_by_url(Im_VK.get_url_photos('552934290'), Im_ya.newfolder())


# if __name__ == '__main__':
#     mylist = []
#     for i in tqdm(mylist):
#         time.sleep(1)

