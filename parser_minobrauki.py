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
    # r = requests.get(url)
    return r.text

def get_page_data(html, hrefs, dict_old_news):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('ul', class_='news-list news-list_images ')
    news = divs.find_all('li')
    for new in news:
        name = new.find('a', class_='news-list__title').getText().replace('\xa0', ' ')
        url = "https://minobrnauki.gov.ru/" + new.find('a', class_='news-list__title').get('href')
        date_str = new.find('time').getText()
        date_news = datetime.strptime(date_str, '%d.%m.%Y').date()

        is_ = False
        for i in range(len(dict_old_news)):
            if name == dict_old_news[i]['name']:
                is_ = True
                break

        days = timedelta(20)
        deadline = datetime.today().date() - days

        if date_news >= deadline and is_ == False:
            if "конкурс" in name.lower() or "тендер" in name.lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                hrefs.append(data)
                dict_old_news.append(data)
                print(data)
        else:
            return False
    return True


def main():
    print('minobrnauki')
    base_url = "https://minobrnauki.gov.ru/"
    page_part = "ru/press-center/press-center/index.php?mode_4=default&order_4=PUB_DATE&dir_4=DESC&page_4="

    if (os.path.exists("hrefs_minobrnauki.json") and os.stat("hrefs_minobrnauki.json").st_size != 0):
        dict_old_news = json.load(open(path + "\\hrefs_minobrnauki.json"))
    else:
        dict_old_news = []

    total_pages = 50
    fl = True
    dict_new_news = []
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        fl = get_page_data(html, dict_new_news, dict_old_news)
        if fl == False:
            break

    json.dump(dict_old_news, open(path + "\\hrefs_minobrnauki.json", "w"), ensure_ascii=False)
    json.dump(dict_new_news, open(path + "\\hrefs_minobrnauki_new.json", "w"), ensure_ascii=False)
    return dict_new_news
