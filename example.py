
import Parser_frp74ru
import Parser_gispgovru
import Parser_minpromtorg
import Parser_p218ru
import lxml
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import socks

hrefs = []
hrefs.append(Parser_frp74ru.main())
hrefs.append(Parser_gispgovru.main())
hrefs.append(Parser_minpromtorg.main())
hrefs.append(Parser_p218ru.main())

names_sites = ['Сайт frp74.ru', 'Сайт gisp.gov.ru', 'Сайт minpromtorg.gov.ru', 'Сайт p218.ru']
body = ''
if (hrefs):
    for i in range(len(hrefs)):
        body += names_sites[i] + '\n'
        for j in range(len(hrefs[i])):
            url = hrefs[i][j].get('url')
            name = hrefs[i][j].get('name')
            date = hrefs[i][j].get('date')
            body += date + ' ' + name + ' ' + url + '\n'
print(body)