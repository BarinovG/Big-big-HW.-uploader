import VK
import Yandex
from pprint import pprint
with open("data_file.json", "w") as f:
  pass
with open('api_vk.txt', encoding='utf-8') as f:
    VKtoken = f.read()


#Инициализация пользователей
Im_YA = Yandex.Yandex_user()
Im_VK = VK.VK_user(VKtoken, '5.131')

#Работа метедов
#Загрузка фото из ВК в Яндекс
Im_YA.upload_by_url(Im_VK.get_url_photos(), Im_YA.newfolder())
#Создание JSON по загруженным файлам
Im_YA.create_json(Im_YA.get_information(), Im_VK.get_size_photos())
