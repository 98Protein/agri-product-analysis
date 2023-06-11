# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import yaml
import pymysql
import uuid
from time import localtime, strftime
from scrapy.exceptions import CloseSpider
import random

class AppPipeline:
    def process_item(self, item, spider):
        return item


class ProductPipeline:
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
            self.cursor.execute("""
                INSERT t_product(id, variety_id, market_id, price, date, sell_number)
                SELECT %s, t_variety.id, t_market.id, %s, %s, %s
                FROM t_variety
                INNER JOIN t_market ON t_variety.origin_code = %s AND t_market.origin_id = %s
            """, (
                uuid.uuid4().hex, float(item['AG_PRICE']),
                strftime('%Y-%m-%d', localtime(int(item['GET_P_DATE']) / 1000)),
                random.randint(0, 50), int(item['CRAFT_INDEX']), int(item['ID'])))

            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()
            raise CloseSpider('failed')  # 请求终止爬虫

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
