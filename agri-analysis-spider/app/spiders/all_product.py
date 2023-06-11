from datetime import datetime
import json

import requests
import scrapy
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


class MofcomSpider(scrapy.Spider):
    name = 'all_product'
    allowed_domains = ['nc.mofcom.gov.cn']

    custom_settings = {
        'ITEM_PIPELINES': {
            'app.pipelines.ProductPipeline': 400
        }
    }

    def __init__(self, start='2014-01-01', end=None, **kwargs):
        super().__init__(**kwargs)
        self.start_date = start
        self.end_date = end

    def start_requests(self):
        if self.end_date is not None:
            end_date = parse(self.end_date, fuzzy=True)
        else:
            end_date = datetime.now()
        start_date = end_date - relativedelta(months=3)
        limit_date = parse(self.start_date, fuzzy=True)
        print("start: ", start_date.strftime('%Y-%m-%d'))
        print("limit: ", limit_date.strftime('%Y-%m-%d'))
        res_list = []

        while (start_date - limit_date).days >= 0:
            res = requests.post(url="http://nc.mofcom.gov.cn/jghq/priceList",
                                data=f"queryDateType=4&timeRange={start_date.strftime('%Y-%m-%d')}"
                                     f"+~+{end_date.strftime('%Y-%m-%d')}",
                                headers={
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                                })
            page_count = json.loads(res.content)['totalPageCount']

            res_list.extend([
                scrapy.Request("http://nc.mofcom.gov.cn/jghq/priceList", method="POST",
                               body=f"queryDateType=4&timeRange={start_date.strftime('%Y-%m-%d')}"
                                    f"+~+{end_date.strftime('%Y-%m-%d')}&pageNo={str(page)}",
                               headers={
                                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                               })
                for page in range(1, page_count + 1)
            ])

            print(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

            end_date = start_date - relativedelta(days=1)
            start_date = end_date - relativedelta(months=3)

        if (start_date - limit_date).days < 0 and (end_date - limit_date).days >= 0:
            start_date = limit_date
            res = requests.post(url="http://nc.mofcom.gov.cn/jghq/priceList",
                                data=f"queryDateType=4&timeRange={start_date.strftime('%Y-%m-%d')}"
                                     f"+~+{end_date.strftime('%Y-%m-%d')}",
                                headers={
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                                })
            page_count = json.loads(res.content)['totalPageCount']

            print(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

            res_list.extend([
                scrapy.Request("http://nc.mofcom.gov.cn/jghq/priceList", method="POST",
                               body=f"queryDateType=4&timeRange={start_date.strftime('%Y-%m-%d')}"
                                    f"+~+{end_date.strftime('%Y-%m-%d')}&pageNo={str(page)}",
                               headers={
                                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                               })
                for page in range(1, page_count + 1)
            ])

        return res_list

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for item in data["result"]:
            yield item
