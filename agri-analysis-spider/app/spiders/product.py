import json
from datetime import datetime
import scrapy
import requests


class MofcomSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['nc.mofcom.gov.cn']

    custom_settings = {
        'ITEM_PIPELINES': {
            'app.pipelines.ProductPipeline': 300
        }
    }

    def __init__(self, date=None, **kwargs):
        super().__init__(**kwargs)
        self.date = date

    def start_requests(self):
        if self.date is None:
            self.date = datetime.now().strftime('%Y-%m-%d')
        print("爬取日期：", self.date)
        res = requests.post(url="http://nc.mofcom.gov.cn/jghq/priceList",
                            data=f"queryDateType=4&timeRange={self.date}+~+{self.date}",
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                            })
        page_count = json.loads(res.content)['totalPageCount']

        return [
            scrapy.Request("http://nc.mofcom.gov.cn/jghq/priceList", method="POST",
                           body=f"queryDateType=4&timeRange={self.date}+~+{self.date}&pageNo=" + str(page),
                           headers={
                               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                           })
            for page in range(1, page_count + 1)
        ]

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for item in data["result"]:
            yield item
