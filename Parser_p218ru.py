from bs4 import BeautifulSoup
import os
import requests
import json
from datetime import datetime, timedelta

path = os.getcwd()

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

def get_html(url):
    proxy = {
        'https': 'https://127.0.0.1:8085',
        'http': 'http://127.0.0.1:8085',
    }
    r = requests.get(url, proxies=proxy)
    # r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('li', class_='pagination-end')
    pages = divs.find('a').get('href')
    total_pages = pages.split('=')[1]
    return int(int(total_pages) / 20)

def get_page_data(html, hrefs, dict_old_news):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_='itemContainer itemContainerLast')
    for new in news:
        name = new.find('h3', class_='k2title_cat').getText().replace('\n', ' ')
        url = "http://www.p218.ru" + new.find('h3', class_='k2title_cat').find('a').get('href')
        date_str = new.find('time').get_text().replace('\t', '').replace('\n', '').split(', ')[1]
        date = int_value_from_ru_month(date_str.lower())
        date_news = datetime.strptime(date, '%d %m %Y').date()

        is_ = False
        for i in range(len(dict_old_news)):
            if name == dict_old_news[i]['name']:
                is_ = True
                break

        days = timedelta(20)
        deadline = datetime.today().date() - days

        if date_news >= deadline and is_ == False:
            if "конкурс" in str(name).lower() or "тендер" in name.lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                print(data)
                hrefs.append(data)
                dict_old_news.append(data)
        else:
            return False
    return True

def main():
    print('p218ru')
    base_url = "http://www.p218.ru/k2"
    page_part = "?start="

    if (os.path.exists("hrefs_p218ru.json") and os.stat("hrefs_p218ru.json").st_size != 0):
        dict_old_news = json.load(open(path + "\\hrefs_p218ru.json"))
    else:
        dict_old_news = []

    total_pages = get_total_pages(get_html(base_url))
    dict_new_news = []
    fl = True
    for i in range(0, total_pages + 1):
        url_gen = base_url + page_part + str(i * 20)
        html = get_html(url_gen)
        fl = get_page_data(html, dict_new_news, dict_old_news)
        if fl == False:
            break
    json.dump(dict_old_news, open(path + "\\hrefs_p218ru.json", "w"), ensure_ascii=False)
    json.dump(dict_new_news, open(path + "\\hrefs_p218ru_new.json", "w"), ensure_ascii=False)
    return dict_new_news

