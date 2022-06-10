from socket import *
from threading import Thread
from pygame import sprite, image, time
from time import  sleep
import pygame
import random
from sabitler import *
import logger

kaynak = "Sunucu"
loglayici = logger.Logger(LOGLAMA)
loglayici.log(kaynak,"Yönler",YONLER)
class Top(sprite.Sprite):
    def __init__(self):
        self.image = TOPGORSEL
        self.rect = self.image.get_rect()

    def konumDegistir(self,konum):
        self.rect.x ,self.rect.y = konum

    def update(self):
        global yonx, yony, kazanan
        self.rect.x += yonx
        self.rect.y += yony
        if sprite.collide_rect(self, cubuk1) or sprite.collide_rect(self, cubuk2):
            isaret = yonx / abs(yonx)
            yonx = -(isaret * (abs(yonx) + HIZLANMA))
            yony = random.choice(YONLER)
        if self.rect.top <= 0:
            yony = -yony
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            yony = -yony
            self.rect.bottom = 600
        if self.rect.left >= 800:
            kazanan = IKINCIKAZANDI
            self.rect.left = 800
            return
        elif self.rect.right <= 0:
            kazanan = BIRINCIKAZANDI
            self.rect.right = 0
            return


class Cubuk(sprite.Sprite):
    def __init__(self):
        self.image = CUBUK
        self.rect = self.image.get_rect()

    def konumDegistir(self,konum):
        self.rect.x,self.rect.y = konum


class Oyuncu():
    def __init__(self, sunucu: socket,top:Top,cubuk1:Cubuk,cubuk2:Cubuk,ben:Cubuk,index:int):
        self.sunucu = sunucu
        self.top = top
        self.cubuk1 = cubuk1
        self.cubuk2 = cubuk2
        self.ben = ben
        self.rakipAdi = False
        self.index = index
        self.bagli = False
        while True:
            try:
                self.istemci , self.addr = self.sunucu.accept()
                self.bagli = True
                break
            except timeout:
                pass
            except Exception as error:
                loglayici.log(f"Oyuncu {self.index}","Bağlanamadı",error)
                break
        if self.bagli:
            loglayici.log(f"Oyuncu {self.index}","Bağlandı")
            t = Thread(target=self.arkaPlan)
            t.start()
    
    def arkaPlan(self):
        global calisiyor,herkesHazirMi,oyuncular,kazanan
        self.isim = self.ismiAl()
        herkesHazirMi[self.index] = True
        while calisiyor:
            try:
                self.acilis()
                while not self.rakipBaglandimi(all(herkesHazirMi)) and calisiyor:
                    pass
                if not self.rakipAdi:
                    self.rakipAdi = oyuncular[(self.index + 1) % 2].isim
                    self.rakibinIsminiGonder(self.rakipAdi)
                while not kazanan and calisiyor:
                    self.konumAlGonder()
                self.kazananiGonder(kazanan)
                self.kapat()
                calisiyor = False
                loglayici.log(self.isim,"Oyun Bitti","Başa Döndü")
            except ConnectionResetError:
                loglayici.log(self.isim,"Bağlantı koptu")
                break
            except Exception as error:
                loglayici.log(self.isim,"Hata",error)
                self.istemci.close()
                break
        self.bagli = False
    def kapat(self):
        self.istemci.send(KAPAT.to_bytes(1,"little"))

    def acilis(self):
        konum = self.konumlariHesapla()
        self.istemci.send(ACILISKONUMLAR.to_bytes(1,"little"))
        self.istemci.send((self.index+1).to_bytes(1,"little")+konum)
        self.tamamMi("acilis")
        loglayici.log(self.isim,"Açılış yapıldı",(self.index+1).to_bytes(1,"little")+konum)

    def konumAlGonder(self): #TODO butadasın
        self.istemci.send(KONUMLAR.to_bytes(1,"little"))
        cubuky_bytes = self.istemci.recv(2)
        cubuky = cubuky_bytes[0] * 256 + cubuky_bytes[1]
        self.ben.rect.y = cubuky
        loglayici.log(self.isim,"Konum",cubuky)
        konum = self.konumlariHesapla()
        self.istemci.send(konum)
        self.tamamMi("konumAlGonder")

    def kazananiGonder(self,kazanan:int):
        self.istemci.send(KAZANMA.to_bytes(1,"little"))
        self.istemci.send(kazanan.to_bytes(kazanan,"little"))
        self.tamamMi("kazananiGonder")

    def rakipBaglandimi(self,durum:bool):
        if durum:
            baglanma = BAGLANDI
        else:
            baglanma = BAGLANMADI
        self.istemci.send(BAGLANMA.to_bytes(1,"little"))
        self.istemci.send(baglanma.to_bytes(1,"little"))
        self.tamamMi("rakipBaglandimi")
        return durum

    def rakibinIsminiGonder(self,rakipİsmi:str):
        self.istemci.send(RAKIPADINIALMA.to_bytes(1,"little"))
        self.istemci.send(rakipİsmi.zfill(MAKSOYUNCUISMIUZUNLUGU).encode())
        self.tamamMi("rakipİsmi")
        loglayici.log(self.isim,"Rakip ismi alındı",rakipİsmi)
    
    def konumlariHesapla(self):
        topYedek = [self.top.rect.x,self.top.rect.y]
        topYedek[0] += 256
        topYedek[1] += 256
        konumlar = (topYedek[0] // 256, topYedek[0] % 256, topYedek[1] // 256, topYedek[1] % 256,
                self.cubuk1.rect.x // 256, self.cubuk1.rect.x % 256, self.cubuk1.rect.y // 256, self.cubuk1.rect.y % 256,
                self.cubuk2.rect.x // 256, self.cubuk2.rect.x % 256, self.cubuk2.rect.y // 256, self.cubuk2.rect.y % 256)
        konum = bytearray()
        for kon in konumlar:
            if kon < 0:
                kon = 0
            elif kon > 255:
                kon = 255
            konum.append(kon)
        return bytes(konum)

    def ismiAl(self):
        self.istemci.send(ISIMGONDER.to_bytes(1,"little"))
        isim = self.istemci.recv(MAKSOYUNCUISMIUZUNLUGU).decode().strip("0")
        loglayici.log(self.index,"İsim alındı",isim)
        return isim
    
    def tamamMi(self,durum):
        b = self.istemci.recv(1)[0]
        if not b == 1:
            loglayici.log(self.isim,"Bir sıkıntı var",b,durum)
            print("Bir sıkıntı var :",b,durum)

def baslat():
    global yonx,yony,kazanan,herkesHazirMi
    yonx, yony = random.choice(YONLER), random.choice(YONLER)
    loglayici.log(kaynak,"Yön",yonx,yony)
    kazanan = 0
    herkesHazirMi = [False,False]
    top.konumDegistir(TOPBASLANGICKONUM)
    cubuk1.konumDegistir(CUBUK1BASLANGICKONUM)
    cubuk2.konumDegistir(CUBUK2BASLANGICKONUM)



calisiyor = True
top = Top()
cubuk1 = Cubuk()
cubuk2 = Cubuk()
clock = time.Clock()
sunucu = socket()
sunucu.settimeout(1)
sunucu.bind((IP, PORT))
sunucu.listen()

baslat()
oyuncular = []
oyuncu1 = Oyuncu(sunucu,top,cubuk1,cubuk2,cubuk1,0)
oyuncu2 = Oyuncu(sunucu,top,cubuk1,cubuk2,cubuk2,1)
oyuncular.append(oyuncu1)
oyuncular.append(oyuncu2)
saniye = 0

while (oyuncu1.bagli or oyuncu2.bagli) and saniye < BEKLEMESURESI:
    sleep(1)
    saniye += 1
while calisiyor:
    clock.tick(60)
    top.update()
    if kazanan == BIRINCIKAZANDI:
        loglayici.log(kaynak,"Birinci kazandı")
        calisiyor = False
    elif kazanan == IKINCIKAZANDI:
        loglayici.log(kaynak,"İkinci kazandı")
        calisiyor = False
loglayici.log(kaynak,"Doğru bir şekilde kapatıldı")