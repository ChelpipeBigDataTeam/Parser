from bs4 import BeautifulSoup
import os
import requests
import json
from datetime import datetime, timedelta

path = os.getcwd()

def get_html(url):
    proxy = {
        'https': 'https://127.0.0.1:8085',
        'http': 'http://127.0.0.1:8085',
    }
    r = requests.get(url, proxies=proxy)
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
        try:
            name = new.find('a', class_='itemImage_news').get('title')
            url = "http://www.p218.ru" + new.find('a', class_='itemImage_news').get('href')
            date_str = new.find('time').get_text().replace('\t', '').replace('\n', '').replace(' ', '')
        except Exception:
            name = new.find('div', class_='itemTitle_news').find('a').getText()
            url = "http://www.p218.ru" + new.find('div', class_='itemTitle_news').find('a').get('href')
            date_str = new.find('time').get_text().replace('\t', '').replace('\n', '').replace(' ', '')
        date_news = datetime.strptime(date_str, '%d.%m.%Y').date()

        is_ = False
        for i in range(len(dict_old_news)):
            if name == dict_old_news[i]['name']:
                is_ = True
                break

        days = timedelta(100)
        deadline = datetime.today().date() - days

        if date_news >= deadline and is_ == False:
            if "конкурс" in str(name).lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                hrefs.append(data)
                dict_old_news.append(data)
        else:
            return False
    return True

def main():
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
