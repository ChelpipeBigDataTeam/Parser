import Parser_frp74ru
import Parser_gispgovru
import Parser_minpromtorg
import Parser_p218ru
import parser_minobrauki
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import socks
from subprocess import Popen
import os, time
import json
from datetime import datetime, timedelta

socks.setdefaultproxy(socks.SOCKS5, '127.0.0.1', 1080)
socks.wrapmodule(smtplib)

path = os.getcwd()

p = Popen(path + "/" + "start_crawlers.bat", cwd=path)
stdout, stderr = p.communicate()

data_exportcenter = []
if (os.path.exists(path+ "/" + "hrefs_exportcenter_new.json")):
    if (os.stat(path+ "/" + "hrefs_exportcenter_new.json").st_size != 0):
        data_exportcenter = json.load(open(path+ "/" + "hrefs_exportcenter_new.json"))

hrefs = []
hrefs.append(parser_minobrauki.main())
hrefs.append(data_exportcenter)
hrefs.append(Parser_frp74ru.main())
hrefs.append(Parser_gispgovru.main())
hrefs.append(Parser_minpromtorg.main())
hrefs.append(Parser_p218ru.main())

names_sites = ['Сайт минобрнауки.рф', 'Сайт exportcenter.ru', 'Сайт frp74.ru', 'Сайт gisp.gov.ru', 'Сайт minpromtorg.gov.ru', 'Сайт p218.ru']
body = ''
if (hrefs):
    for i in range(len(hrefs)):
        if (hrefs[i]):
            body += '\n' + '\n' + names_sites[i] + '\n'
            for j in range(len(hrefs[i])):
                url = hrefs[i][j].get('url')
                name = hrefs[i][j].get('name')
                date = hrefs[i][j].get('date')
                body += date + ' ' + name + ' ' + url + '\n'
    if body != '':
        login = 'news.sending@yandex.ru'
        password = '12345qwert'
        recipients = ['Kirill.Nikitin@chelpipe.ru','Anton.Gizatullin@chelpipe.ru','Dmitriy.Tropin@chelpipe.ru','Mikhail.Fedorov@chelpipe.ru','Aleksandr.Lunev@chelpipe.ru','Anastasiya.Mittseva@chelpipe.ru']
        # recipients = ['Anastasiya.Mittseva@chelpipe.ru']

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header('Конкурсы', 'utf-8')
        msg['From'] = login
        msg['To'] = ", ".join(recipients)

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(login, password)
        server.sendmail(msg['From'], recipients, msg.as_string())
        server.close()