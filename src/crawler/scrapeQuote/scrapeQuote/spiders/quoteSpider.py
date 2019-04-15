# -*- coding: utf-8 -*-
import scrapy

from scrapeQuote.items import ScrapequoteItem

class QuotesSpider(scrapy.Spider):
    """ 
        def start_requests(self):
            urls = [
                'http://quotes.toscrape.com/page/1/',
                'http://quotes.toscrape.com/page/2/',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, meta={'proxy':'http://127.0.0.1:3128'}) 
    """
    name = "quotes"
    # 快捷方式
    start_urls = ['http://quotes.toscrape.com/page/1/']
    depth = 10

    def parse(self, response):
        """ page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename) """

        #下面这种写法使用生成器方式比较好
        """ items = []
        for i in response.css('div.quote'):
            item =  ScrapequoteItem()
            item['tag'] =  i.css('span.text[itemprop]::text').get()
            item['author'] =  i.css('small.author::text').get()
            items.append(item)
        return items """

        for i in response.css('div.quote'):
            item =  ScrapequoteItem()
            item['tag'] =  i.css('span.text[itemprop]::text').get()
            item['author'] =  i.css('small.author::text').get()
            yield item

        #以下循环获取其他页面
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)  #返回一个Request instance
