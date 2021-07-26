import datetime
import requests

class VK_user:
    url = 'https://api.vk.com/method/'

    #инициализируем пользователя ВК
    def __init__(self, token, version):
        self.owner_id = input('Введите id пользователя Вконтакте: ')
        self.params = {'access_token': token, 'v': version}

    #получим общую информацию по фотографиям из ВК
    def get_inf_photos(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': self.owner_id,
            'album_id': "profile",
            'extended': 1,
            'photo_sizes': 0,
            'count': 5,
            'rev': 0
        }
        req = requests.get(get_photos_url,
                           params={**self.params, **get_photos_params}).json()
        return req['response']['items']

    #из полученного ответа выше вытаскиваем - количество лайков, которое будет названием для файла; и также юрл ссылку на файл
    def get_url_photos(self):
        urls = []
        names = []
        all_inf = self.get_inf_photos()
        for inf in all_inf:
            for count_likes in inf['likes'].items():
                if count_likes[0] == 'count':
                    if str(count_likes[1]) in names:
                        #переводим unixtime, которое юзают в ВК, в обычное время
                        date_unix = inf['date']
                        date = datetime.datetime.fromtimestamp(date_unix)
                        date = f'{date:%Y-%m-%d %H.%M.%S}'
                        names.append(f"{str(count_likes[1])} - {date}")
                    else:
                        names.append(f"{str(count_likes[1])}")
            for url in inf['sizes'][-1].items():
                if url[0] == 'url':
                    urls.append(url[1])
        #зипуем полученные списки имен и юрлов в общий словарь (имя : юрл)
        url_photos_dict = dict(zip(names, urls))
        return url_photos_dict

    #с помощью этой функции получим название размера фотографии, чтобы в будущем сформировать JSON по загруженным на Я.Диск файлам
    def get_size_photos(self):
        types = []
        all_inf = self.get_inf_photos()
        for inf in all_inf:
            for size in inf['sizes'][-1].items():
                if size[0] == 'type':
                    types.append(size[1])
        return types