import time
import smtplib
import config
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_mail(sub,filename):
    try:
        message = MIMEMultipart()
        message['From'] = config.SENDER
        message['To'] = config.RECEIVER
        message['Subject'] = sub

        with open(filename, "rb") as f:
            part = MIMEApplication(f.read(),Name=filename)
        part['Content-Disposition'] = 'attachment; filename="%s"' % filename
        message.attach(part)

        svr = smtplib.SMTP('smtp.gmail.com:587')
        svr.ehlo()
        svr.starttls()
        svr.login(config.SENDER, config.PASSWORD)
        svr.sendmail(config.SENDER, config.RECEIVER, message.as_string())
        svr.quit()
        print("Success")
    except:
        print("fail")

current_time = datetime.datetime.now()
month = current_time.strftime("%B")
day = current_time.strftime("%d")
sub = "{}. {} Manga Recap".format(day,month)
filename = "log.txt"
send_mail(sub, filename)
