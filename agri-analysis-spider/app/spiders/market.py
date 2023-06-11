import json
import traceback

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
        market = item['market']
        city = item['city']
        try:
            self.cursor.execute(
                'INSERT t_market(id, city_id, name, address, picture_url, details, origin_id) '
                'SELECT %s, t_city.id, %s, %s, %s, %s, %s FROM t_city WHERE t_city.origin_index = %s',
                (uuid.uuid4().hex, market.get('EUD_NAME', None), market.get('ADDR', None),
                 market.get('EUD_PIC', None), market.get('CONTENT', None), market.get('ID', None), city.get('P_INDEX', None))
            )
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class MofcomSpider(scrapy.Spider):
    name = 'market'
    allowed_domains = ['nc.mofcom.gov.cn']

    custom_settings = {
        'ITEM_PIPELINES': {
            'app.spiders.market.MySQLPipeline': 300
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
        for city in cities:
            yield scrapy.Request("http://nc.mofcom.gov.cn/jghq/marketList", method="POST", headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }, body=f"province={province['P_INDEX']}&city={city['P_INDEX']}&isprod_mark=&par_craft_index=&pageNo=1",
                                 meta={'city': city, 'province': province}, callback=self.parse_market)

    def parse_market(self, response):
        province = response.meta['province']
        city = response.meta['city']
        data = json.loads(response.text)
        for item in [
            {
                "province": province,
                "city": city,
                "market": market
            } for market in data["result"]
        ]:
            yield item

        if data["hasNext"]:
            yield scrapy.Request("http://nc.mofcom.gov.cn/nc/qyncp/province", method="POST", headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }, body=f"province={province['P_INDEX']}&city={city['P_INDEX']}"
                    f"&isprod_mark=&par_craft_index=&pageNo={data['nextPage']}",
                                 meta={'city': city, 'province': province}, callback=self.parse_market)
