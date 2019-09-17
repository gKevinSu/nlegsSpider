# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from nlegs import settings
import requests
import random

class NlegsPipeline(object):
    headers = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cookie':'__cfduid=d9cf58f894b52e29aa470f4125d904b631567404640',
    'Host':'www.nlegs.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://www.nlegs.com/girls/2019/09/16/12267.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    def process_item(self, item, spider):
        dir_path = '%s/%s/%s/' % (settings.IMAGES_STORE, item['model'], item['title'])
        #print('dir_path',dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        image_path = dir_path + item['url'][item['url'].rindex("/"):]
        image_exist = False
        if os.path.exists(image_path):
            if os.path.getsize(image_path)>10240:
                image_exist = True
        if not image_exist:
            with open(image_path, 'wb') as f:
                response = requests.get(url=item['url'], headers=self.headers)
                f.write(response.content)
        return item
