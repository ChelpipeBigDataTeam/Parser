from bs4 import BeautifulSoup
import requests
import os
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

path = os.getcwd()

def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str

def get_html(url):
    proxy = {
        'https': 'https://127.0.0.1:8085',
        'http': 'http://127.0.0.1:8085',
    }
    r = requests.get(url, proxies=proxy)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='box-articles')
    fonts = divs.find_all('font', class_='text')[1]
    pages = fonts.find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def get_page_data(html, hrefs, dict_old_news):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_='item')
    for new in news:
        name = new.find('div', class_='iname').getText()
        url = "https://gisp.gov.ru" + new.find('div', class_='iname').find('a').get('href')
        date_str = new.find('div', class_='date').getText()
        date_news = int_value_from_ru_month(date_str.lower())
        date_news = datetime.strptime(date_news, '%d %m %Y').date()

        is_ = False
        for i in range(len(dict_old_news)):
            if name == dict_old_news[i]['name']:
                is_ = True
                break

        days = timedelta(100)
        deadline = datetime.today().date() - days

        if date_news >= deadline and is_ == False:
            if "конкурс" in name.lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                hrefs.append(data)
                dict_old_news.append(data)
        else:
            return False
    return True


def main():
    base_url = "https://gisp.gov.ru/news/"
    page_part = "?PAGEN_1="

    if (os.path.exists("hrefs_gispgovru.json") and os.stat("hrefs_gispgovru.json").st_size != 0):
        dict_old_news = json.load(open(path + "\\hrefs_gispgovru.json"))
    else:
        dict_old_news = []

    total_pages = get_total_pages(get_html(base_url))
    dict_new_news = []
    fl = True
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        fl = get_page_data(html, dict_new_news, dict_old_news)
        if fl == False:
            break

    json.dump(dict_old_news, open(path + "\\hrefs_gispgovru.json", "w"), ensure_ascii=False)
    json.dump(dict_new_news, open(path + "\\hrefs_gispgovru_new.json", "w"), ensure_ascii=False)
    return dict_new_news

