import json

import pymysql
import scrapy
import yaml
import uuid


class MySQLPipeline:
    def __init__(self):
        mysql_config = yaml.load(open('app/config/database.secret.yml'),
                                 Loader=yaml.SafeLoader)['development']['database']
        self.connect = pymysql.connect(
            host=mysql_config['host'],
            port=mysql_config['port'],
            user=mysql_config['username'],
            password=mysql_config['password'],
            database=mysql_config['database'],
            charset='utf8'
        )

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            type_id = uuid.uuid4().hex
            self.cursor.execute("INSERT t_type(id, name)  VALUE (%s, %s)",
                                (type_id, item['name']))

            self.cursor.executemany("INSERT t_variety(id, name, type_id, origin_code) VALUES (%s, %s, %s, %s)",
                                    tuple(
                                        (uuid.uuid4().hex, variety['varietyName'], type_id, variety['varietyCode']) for
                                        variety in item['variety']
                                    )
                                    )

            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class MofcomSpider(scrapy.Spider):
    name = 'variety'
    allowed_domains = ['nc.mofcom.gov.cn']
    custom_settings = {
        'ITEM_PIPELINES': {
            'app.spiders.variety.MySQLPipeline': 300
        }
    }

    def start_requests(self):
        return [
            scrapy.Request("http://nc.mofcom.gov.cn/jghq/variety", method="GET")
        ]

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for item in data:
            if item['name'] != '拼音ABC':
                yield item
