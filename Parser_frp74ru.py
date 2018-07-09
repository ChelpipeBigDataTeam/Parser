from bs4 import BeautifulSoup
import requests
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
    divs = soup.find('div', class_='row pagination')
    fonts = divs.find_all('font', class_='text')[1]
    pages = fonts.find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def get_page_data(html, hrefs):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_='column float-left small-3')
    for new in news:
        name = new.find('img').get('alt')
        url = "http://frp74.ru" + new.find('a').get('href')
        date_str = new.find('div', class_='date').getText()
        date = datetime.strptime(date_str, '%d.%m.%Y')

        days = timedelta(10)
        deadline = datetime.now() - days

        if date > deadline:
            if "конкурс" in name.lower():
                data = {'name': name,
                        'url': url,
                        'date': date_str}
                hrefs.append(data)
        else:
            return False
    return True


def main():
    base_url = "http://frp74.ru/news/"
    page_part = "?PAGEN_1="

    total_pages = get_total_pages(get_html(base_url))
    fl = True
    hrefs = []
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        fl = get_page_data(html, hrefs)
        if fl == False:
            break
    return hrefs
