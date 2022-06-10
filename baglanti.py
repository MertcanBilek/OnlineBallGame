from socket import *
from sabitler import *

import logger

loglayici = logger.Logger(LOGLAMA)
sunucu = socket()
kaynak = "İstemci"

def baglan():
    global sunucu, IP, PORT
    try:
        sunucu.connect((IP, PORT))
    except Exception as error:
        loglayici.log(kaynak,"Bağlantı Hatası",error)
        quit()

def tamam():
    sunucu.send(b"\x01")

def ismiGonder(isim:str):
    isim = isim.zfill(MAKSOYUNCUISMIUZUNLUGU)
    sunucu.send(isim.encode()[:MAKSOYUNCUISMIUZUNLUGU])

def rakipİsminiAl():
    s = sunucu.recv(MAKSOYUNCUISMIUZUNLUGU).strip(b"0")
    tamam()
    return s

def konumVerAl(cubuk):
    konum = bytearray()
    konum.append(cubuk.gecici_y // 256)
    konum.append(cubuk.gecici_y % 256)
    sunucu.send(bytes(konum))
    loglayici.log(kaynak,"Gönderildi",konum)
    konum = sunucu.recv(12)
    tamam()
    cubuk2y = konum[10]*256 + konum[11]
    topx = konum[0]*256 + konum[1] - 256
    topy = konum[2]*256 + konum[3] - 256
    cubuk1x = konum[4]*256 + konum[5]
    cubuk1y = konum[6]*256 + konum[7]
    cubuk2x = konum[8]*256 + konum[9]
    return topx, topy, cubuk1x,cubuk1y, cubuk2x,cubuk2y

def ikinciBaglandiMi():
    s = sunucu.recv(1)[0]
    tamam()
    return s

def kimKazanmis():
    s = sunucu.recv(1)[0]
    tamam()
    return s

def acilisKonumlari():
    s = sunucu.recv(13)
    tamam()
    return s

def alisTipi():
    s = sunucu.recv(1)[0]
    return s