import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from hlbmy.items import Article
import requests
import json


class hlbmySpider(scrapy.Spider):
    name = 'hlbmy'
    start_urls = ['https://www.hlb.com.my/en/personal-banking/news-updates.html?icp=hlb-en-all-menu-txt-newsupdate']

    def parse(self, response):
        id = 1619092146909
        json_response = json.loads(requests.get(f"https://www.hlb.com.my/bin/hlb/newsandupdates?locale=en&counter=0&categories=%5B%5D&from=&to=&componentPath=%2Fcontent%2Fhlb%2Fmy%2Fen%2Fpersonal-banking%2Fnews-updates&_={id}").text)
        articles = json_response["result"]
        for article in articles:
            link = response.urljoin(article['link'])
            date = article["articleDate"]
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

    def parse_article(self, response, date):
        if 'pdf' in response.url.lower():
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//title/text()').get()
        if title:
            title = title.split('-')[0].strip()

        content = response.xpath('//div[@data-emptytext="Text"]//text()').getall()
        content = [text.strip() for text in content if text.strip() and '{' not in text]
        content = " ".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
