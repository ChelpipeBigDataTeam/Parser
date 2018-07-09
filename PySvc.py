import win32service
import win32serviceutil
import win32event
import Parser_frp74ru
import Parser_gispgovru
import Parser_minpromtorg
import Parser_p218ru
import lxml
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import socks
import os

class PySvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "PySvc"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Python Test Service"
    # this text shows up as the description in the SCM
    _svc_description_ = "This service writes stuff to a file"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        # core logic of the service

    def SvcDoRun(self):
        socks.setdefaultproxy(socks.SOCKS5, '127.0.0.1', 1080)
        socks.wrapmodule(smtplib)

        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            os.system("C:/Windows/System32/cmd.exe /c C:/Users/Anastasiya.Mittseva/PycharmProjects/ServiceParserSites/start_crawlers.bat")
            hrefs = []
            hrefs.append(Parser_frp74ru.main())
            hrefs.append(Parser_gispgovru.main())
            hrefs.append(Parser_minpromtorg.main())
            hrefs.append(Parser_p218ru.main())

            names_sites = ['Сайт frp74.ru', 'Сайт gisp.gov.ru', 'Сайт minpromtorg.gov.ru', 'Сайт p218.ru']
            body = ''
            if (hrefs):
                for i in range(len(hrefs)):
                    if (hrefs[i]):
                        body += '\n'+ '\n'+ names_sites[i] + '\n'
                        for j in range(len(hrefs[i])):
                            url = hrefs[i][j].get('url')
                            name = hrefs[i][j].get('name')
                            date = hrefs[i][j].get('date')
                            body += date + ' ' + name + ' ' + url + '\n'

                login = 'pi7.iwan0ff@yandex.ru'
                password = 'ZXcv1234'
                recipients_emails = 'Anastasiya.Mittseva@chelpipe.ru'

                msg = MIMEText(body, 'plain', 'utf-8')
                msg['Subject'] = Header('Конкурсы', 'utf-8')
                msg['From'] = login
                msg['To'] = recipients_emails

                server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
                server.login(login, password)
                server.sendmail(msg['From'], recipients_emails, msg.as_string())
                server.close()

            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)

    def SvcStop(self):
        # tell the SCM we're shutting down
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PySvc)