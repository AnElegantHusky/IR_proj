# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import xml.etree.ElementTree as ET
import sys
sys.path.append("../")
from engine.elasticsearch_orm import engineMiddleware


class EnginePipeline(object):
    def process_item(self, item, spider):
        item.save_to_es()
        return item


class DocumentationPythonPipeline:
    def __init__(self):
        for i in range(1, 11):
            with open('../data/docs/sum_{}.txt'.format(i), 'r') as f:
                num = int(f.readline())
                if num <= 1000:
                    self.folder = i
                    self.num = num
                    break
        self.index = open('../data/docs/index_{}.txt'.format(self.folder), 'a')
        self.sum = open('../data/docs/sum_{}.txt'.format(self.folder), 'w')

    def process_item(self, item, spider):
        self.index.write("{:>4d} {}\n".format(self.num, item['url']))
        path = '../data/docs/{}/{}.xml'.format(self.folder, self.num)
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d" % (self.num)
        ET.SubElement(doc, "url").text = item['url']
        ET.SubElement(doc, "title").text = item['title']
        ET.SubElement(doc, "body").text = item['body']
        tree = ET.ElementTree(doc)
        tree.write(path, encoding='utf-8', xml_declaration=True)
        self.num += 1
        if self.num == 1001:
            self.index.close()
            self.sum.write("{}".format(self.num))
            self.sum.close()

            self.folder += 1
            self.num = 1
            self.index = open('../data/docs/index_{}.txt'.format(self.folder), 'a')
            self.sum = open('../data/docs/sum_{}.txt'.format(self.folder), 'w')
        return item

    def close_spider(self, spider):
        self.index.close()
        self.sum.write("{}".format(self.num))
        self.sum.close()
