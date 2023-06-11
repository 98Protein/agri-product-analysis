import json

import scrapy
import yaml
import pymysql
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
            province_id = uuid.uuid4().hex
            self.cursor.execute(
                'INSERT t_province(id, name, origin_index, full_name) VALUE (%s, %s, %s, %s)',
                (province_id, item['S_NAME'], item['P_INDEX'], item['P_NAME'])
            )

            self.cursor.executemany(
                'INSERT t_city(id, name, province_id, origin_index, full_name) VALUES (%s, %s, %s, %s, %s)',
                tuple((uuid.uuid4().hex, city['S_NAME'], province_id, city['P_INDEX'], city['P_NAME'])
                      for city in item['CITIES'])
            )

            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class MofcomSpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['nc.mofcom.gov.cn']
    custom_settings = {
        'ITEM_PIPELINES': {
            'app.spiders.city.MySQLPipeline': 300
        }
    }

    def start_requests(self):
        return [
            scrapy.Request("http://nc.mofcom.gov.cn/nc/qyncp/province", method="POST")
        ]

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for item in data:
            yield scrapy.Request("http://nc.mofcom.gov.cn/nc/qyncp/province", method="POST", headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }, body="pIndex=" + item["P_INDEX"], meta={'province': item}, callback=self.parse_city)

    def parse_city(self, response):
        province = response.meta["province"]
        cities = [item for item in json.loads(response.text) if item["P_INDEX"] != province["P_INDEX"]]
        province["CITIES"] = cities
        yield province
