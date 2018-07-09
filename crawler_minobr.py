import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import os
import requests
import json
from datetime import datetime, timedelta

RU_MONTH_VALUES = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
}


def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str


class SpidyQuotesSpider(scrapy.Spider):
    name = 'spidyquotes'
    quotes_base_url = 'https://минобрнауки.рф/пресс-центр/by-page?page=%s&events_sections=1'
    start_urls = [quotes_base_url % 1]
    download_delay = 1.5
    next_page = 1
    dict_new_news = []
    path = 'C:/Users/Anastasiya.Mittseva/PycharmProjects/ServiceParserSites/'

    def start_requests(self):
        quotes_base_url = 'https://минобрнауки.рф/пресс-центр/by-page?page=1&events_sections=1'
        yield scrapy.Request(url=quotes_base_url, callback=self.parse,
                             meta={'proxy': 'https://127.0.0.1:8085', 'proxy': 'http://127.0.0.1:8085'})

    def parse(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        news = soup.find_all('div', class_='news-item')

        for new in news:
            url = 'https://минобрнауки.рф' + new.find('a', class_='media-item-link').get('href')
            name = new.find('a', class_='media-item-link').getText()
            date_str = new.find('span', class_='published published-alt').getText().split(',')[0][:-5]
            href = {'name': name,
                    'url': url,
                    'date': date_str}

            days = timedelta(10)
            deadline = datetime.now() - days

            date = int_value_from_ru_month(date_str.lower())
            date = datetime.strptime(date, '%d %m %Y')

            if date > deadline:
                if "конкурс" in name.lower():
                    self.dict_new_news.append(href)
            else:
                break

        if date > deadline:
            if self.next_page < 307:
                print(self.next_page)
                self.next_page = self.next_page + 1
                yield scrapy.Request(
                    url='https://минобрнауки.рф/пресс-центр/by-page?page=%s&events_sections=1' % self.next_page,
                    meta={'proxy': 'https://127.0.0.1:8085', 'proxy': 'http://127.0.0.1:8085'})
        else:
            json.dump(self.dict_new_news, open(self.path+"hrefs_minobr.json", "w"), ensure_ascii=False)
