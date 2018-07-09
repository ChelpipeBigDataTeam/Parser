from bs4 import BeautifulSoup
import csv
import requests
import lxml
from datetime import datetime, timedelta

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

def get_page_data(html, hrefs):
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
        date = datetime.strptime(date_str, '%d.%m.%Y')

        days = timedelta(10)
        deadline = datetime.now() - days

        if date > deadline:
            if "конкурс" in str(name).lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                hrefs.append(data)
        else:
            return False
    return True

def main():
    base_url = "http://www.p218.ru/k2"
    page_part = "?start="

    total_pages = get_total_pages(get_html(base_url))
    hrefs = []
    fl = True
    for i in range(0, total_pages + 1):
        url_gen = base_url + page_part + str(i * 20)
        html = get_html(url_gen)
        fl = get_page_data(html, hrefs)
        if fl == False:
            break
    return hrefs
