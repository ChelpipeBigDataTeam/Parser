from bs4 import BeautifulSoup
import requests
import lxml
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


days = timedelta(10)
deadline = datetime.now() - days


def get_html(url):
    proxy = {
        'https': 'https://127.0.0.1:8085',
        'http': 'http://127.0.0.1:8085',
    }
    r = requests.get(url, proxies=proxy)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='navigation')
    pages = divs.find_all('a', class_='a2')[-1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


def get_page_data(html, hrefs):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('li', class_='news_list_item')
    for new in news:
        name = new.find('div', class_='news_list-ttl').getText()
        url = "http://minpromtorg.gov.ru" + new.find('a').get('href')
        date_str = new.find('span', class_='main-block-date').getText()
        date = int_value_from_ru_month(date_str.lower())

        date = datetime.strptime(date, '%d %m %Y')

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
    base_url = "http://minpromtorg.gov.ru/press-centre/news/"
    page_part = "?from_18=&from_18="

    total_pages = get_total_pages(get_html(base_url))
    hrefs = []
    fl = True
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        fl = get_page_data(html, hrefs)
        if fl == False:
            break
    return hrefs
