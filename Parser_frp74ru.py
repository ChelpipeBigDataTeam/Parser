from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os
import json

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
    divs = soup.find('div', class_='row pagination')
    fonts = divs.find_all('font', class_='text')[1]
    pages = fonts.find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def get_page_data(html, hrefs, dict_old_news):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_='column float-left small-3')
    for new in news:
        name = new.find('img').get('alt')
        url = "http://frp74.ru" + new.find('a').get('href')
        date_str = new.find('div', class_='date').getText()
        date_news = datetime.strptime(date_str, '%d.%m.%Y').date()

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
    base_url = "http://frp74.ru/news/"
    page_part = "?PAGEN_1="

    if (os.path.exists("hrefs_frp74ru.json") and os.stat("hrefs_frp74ru.json").st_size != 0):
        dict_old_news = json.load(open(path + "\\hrefs_frp74ru.json"))
    else:
        dict_old_news = []

    total_pages = get_total_pages(get_html(base_url))
    fl = True
    dict_new_news = []
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        fl = get_page_data(html, dict_new_news, dict_old_news)
        if fl == False:
            break

    json.dump(dict_old_news, open(path + "\\hrefs_frp74ru.json", "w"), ensure_ascii=False)
    json.dump(dict_new_news, open(path + "\\hrefs_frp74ru_new.json", "w"), ensure_ascii=False)
    return dict_new_news
