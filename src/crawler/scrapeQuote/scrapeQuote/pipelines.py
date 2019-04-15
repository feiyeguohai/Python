# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class ScrapequotePipeline(object):
    def process_item(self, item, spider):

        # print item
        # for i in  item:
        #     print(i)

        # write to json
        with open('item.json','a') as f:
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            f.write(line)
        return item