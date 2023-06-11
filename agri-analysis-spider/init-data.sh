source venv/bin/activate
start-all.sh
/usr/local/spark/sbin/start-all.sh
# 爬取区域数据和农产品种类数据
# scrapy crawl city & scrapy crawl market & scrapy crawl variety
# 爬取段农产品价格和售卖行情数据
scrapy crawl all_product -a start=2023-05-31 -a end=2023-06-02