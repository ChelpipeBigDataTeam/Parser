import scrapy
from bs4 import BeautifulSoup
import os
import json
class SpidyQuotesSpider(scrapy.Spider):
    name = 'spidyquotes'
    quotes_base_url = 'https://www.exportcenter.ru/events/?AJAX_MODE=1&PAGEN_1=%s&date_period=all&city=&search=&rec_participation=&reg_open=Y&international='
    start_urls = [quotes_base_url % 1]
    download_delay = 1.5
    path = os.getcwd()

    if (os.path.exists("hrefs_exportcenter.json") and os.stat("hrefs_exportcenter.json").st_size != 0):
        dict_old_news = json.load(open(path+"\\hrefs_exportcenter.json"))
    else:
        dict_old_news = []
    dict_new_news = []
    f = open(path+'\\hrefs_exportcenter_new.json', 'w')
    f.close()

    def start_requests(self):
        quotes_base_url = 'https://www.exportcenter.ru/events/?AJAX_MODE=1&PAGEN_1=1&date_period=all&city=&search=&rec_participation=&reg_open=Y&international='
        yield scrapy.Request(url=quotes_base_url, callback=self.parse, meta={'proxy': 'https://127.0.0.1:8085', 'proxy': 'http://127.0.0.1:8085'})
        # yield scrapy.Request(url=quotes_base_url, callback=self.parse)
            
    def parse(self, response):
        data = []
        if (os.path.exists(self.path+"\\hrefs_exportcenter.json") and os.stat(self.path+"\\hrefs_exportcenter.json").st_size != 0):
                data = json.load(open(self.path+"\\hrefs_exportcenter.json"))
        
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        news = soup.find_all('div', class_='event-block')

        for new in news:
            url = 'https://www.exportcenter.ru' + new.find('div', class_='event-item__desc').find('a').get('data-url')
            name = new.find('a', class_ = 'event-item__title js-events-detail-link').getText().replace('  ','').replace('\n','').replace('\r','')
            date = new.find('span', class_ = 'event-item__date_day').getText() + '/' + new.find('span', class_ = 'event-item__date_month').getText()
            href = {'name': name,
                    'url': url,
                    'date': date}

            is_ = False
            for i in range(len(data)):
                if name == data[i]['name']:
                    is_ = True
                    break


            if is_ == False:
                self.dict_old_news.append(href)
                self.dict_new_news.append(href)

        if soup.find('div', class_='event-btn_more js-events-go-next'):
            next_page = int(soup.find('div', class_='event-btn_more js-events-go-next').get('data-next-page'))
            print(next_page)
            yield scrapy.Request(url = self.quotes_base_url % next_page, meta={'proxy': 'https://127.0.0.1:8085', 'proxy': 'http://127.0.0.1:8085' })
            # yield scrapy.Request(url=self.quotes_base_url % next_page)
        else:
            json.dump(self.dict_old_news, open(self.path+"\\hrefs_exportcenter.json", "w"), ensure_ascii=False)
            json.dump(self.dict_new_news, open(self.path+"\\hrefs_exportcenter_new.json", "w"), ensure_ascii=False)
