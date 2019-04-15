import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapeQuote.items import ScrapequoteItem

# 使用正则表达式 获取url
class RegexSpider(CrawlSpider):
    name = "quotes_reg"
    # 快捷方式
    start_urls = ['http://quotes.toscrape.com/page/1/']
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r'/page/\d/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        for i in response.css('div.quote'):
            item = ScrapequoteItem()
            item['tag'] = i.css('span.text[itemprop]::text').get()
            item['author'] = i.css('small.author::text').get()
            yield item
