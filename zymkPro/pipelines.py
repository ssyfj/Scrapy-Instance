# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests,os
from fake_useragent import UserAgent

class ZymkproPipeline:
    def process_item(self, item, spider):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload', item['title'])
        ua = UserAgent().random

        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        header = {
            'User-Agent': ua,
            'Referer': item['img_url']
        }

        response = requests.get(item['img_url'], stream=False,headers=header)
        with open(os.path.join(file_path,"%d.jpg"%item['img_number']), "wb") as fp:
            fp.write(response.content)

        return item
