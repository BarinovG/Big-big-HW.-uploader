import json
import requests
from tqdm import tqdm
from pprint import pprint

class Yandex_user():
    uri = 'https://cloud-api.yandex.net/'

    def __init__(self):
        self.token = input('Введите ваш яндекс токен: ')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    # Создаём папку с нужным нам именем на Я.Диске
    def newfolder(self):
        folderName = str(
            input(
                'Введите название папки для сохранения фотографий на Яндекс Диске: '
            ))
        newfolder_url = self.uri + 'v1/disk/resources'
        headers = self.get_headers()
        params = {"path": folderName, "overwrite": "true"}
        response = requests.put(newfolder_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка с именем "{folderName}" создана.')
        return folderName

    # Производим загрузку файлов на Я.Диск. В параметрах ([Словарь полученный из ВК, с данными для загрузки][Имя папки, в которую будут загружены фото])
    def upload_by_url(self, name_url_dict=dict, folderName=str):
        data = {}
        upload_url = self.uri + 'v1/disk/resources/upload'
        headers = self.get_headers()
        for vk_name, vk_url in tqdm(name_url_dict.items()):
            params = {
                "path": str(folderName) + '/' + str(vk_name) + '.jpg',
                "url": vk_url,
                "overwrite": "true"
            }
            response = requests.post(upload_url,
                                     headers=headers,
                                     params=params)
        pprint(response.json())
        return response.json()

    #Получим список загруженных фото на ЯД для составления JSON
    def get_information(self, path=str):
        get_information_url = self.uri + 'v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.get(get_information_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()['_embedded']['items']


    # def create_json(self, photo_name, photo_size):
    #     data = {}
    #     for name in photo_name:
    #         for type in photo_size:
    #             data['file_name'] = [name]
    #             data['size'] = [type]
    #         with open("data_file.json", "a") as f:
    #             json.dump(data, f)
    #             print(
    #                 f'Информация о загрузке {vk_name}.jpg добавлена в json'
    #             )