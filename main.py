import VK
import Yandex
from pprint import pprint

with open("data_file.json", "w") as f:
  pass

with open('api_vk.txt', encoding='utf-8') as f:
    VKtoken = f.read()



Im_YA = Yandex.Yandex_user()
Im_VK = VK.VK_user(VKtoken, '5.131')
# Im_YA.upload_by_url(Im_VK.get_url_photos(), Im_YA.newfolder())

# pprint(Im_YA.get_information('777'))
