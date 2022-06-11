import pygame
from pygame import *
from baglanti import *
from threading import Thread
from pygame import font,display
from time import sleep
from sabitler import *



pygame.init()
benKazandim = OYUNFONT.render(ISIM + " kazandi",0,YESIL)
benKazandimKonum = ((GENISLIK - benKazandim.get_width())/2 , (YUKSEKLIK - benKazandim.get_height())/2)
baglandi = False
kazanan = 0
calisiyor = True

sahne = display.set_mode(BOYUT,DOUBLEBUF,HWSURFACE)
pygame.display.set_caption("Online Top Oyunu")
pikselsayisi = pygame.time.Clock()
rakip = "Rakip"
saniye = 0
baglan()

class Top(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.image = TOPGORSEL
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Cubuk(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.image = CUBUK
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gecici_y = y

    def update(self, *args):
        up, down = args
        self.gecici_y = int(self.rect.y)
        if up:
            self.gecici_y -= 15
        if down:
            self.gecici_y += 15
        if self.gecici_y + self.rect.size[1] > YUKSEKLIK:
            self.gecici_y = YUKSEKLIK - self.rect.size[1]
        if self.gecici_y < 0:
            self.gecici_y = 0


def spriteBastir(*x: pygame.sprite.Sprite):
    sahne.fill((0, 0, 0))
    sahne.blit(ARKAPLAN, (0, 0))
    for i in x:
        sahne.blit(i.image, i.rect)


def veriAlici():
    global baglandi,kazanan,top,cubuk1,cubuk2,yon,rakip,ben,basla,rakipAdi,calisiyor,rakipKazandi,rakipKazandiKonum,saniye
    yon = False
    clock = pygame.time.Clock()
    while calisiyor:
        clock.tick(FPS)
        islem = alisTipi()
        if islem == ACILISKONUMLAR:
            acilis = acilisKonumlari()
            yon = acilis[0]
            topxy   = (acilis[1] * 256 + acilis[2] - 256 , acilis[3] * 256 + acilis[4] - 256)
            cubuk1xy = (acilis[5] * 256 + acilis[6], acilis[7] * 256 + acilis[8])
            cubuk2xy = (acilis[9] * 256 + acilis[10], acilis[11] * 256 + acilis[12])
            top = Top(*topxy)
            cubuk1 = Cubuk(*cubuk1xy)
            cubuk2 = Cubuk(*cubuk2xy)
            if yon == 1:
                ben = cubuk1
                rakip = cubuk2
            elif yon == 2:
                ben = cubuk2
                rakip = cubuk1
            yon = False
            basla = True
        elif islem == KONUMLAR:
            top.rect.x, top.rect.y, cubuk1.rect.x , cubuk1.rect.y , cubuk2.rect.x ,cubuk2.rect.y = konumVerAl(ben)
        elif islem == KAZANMA:
            kznn = kimKazanmis()
            if kznn == BIRINCIKAZANDI:
                kazanan = kznn
            elif kznn == IKINCIKAZANDI:
                kazanan = kznn
        elif islem == BAGLANMA:
            sonuc = ikinciBaglandiMi()
            if sonuc == BAGLANMADI:
                baglandi = False
                if saniye % 60 == 0:
                    loglayici.log(ISIM,"Bağlantı bekleniyor",saniye,sonuc)
            else:
                baglandi = True
        elif islem == RAKIPADINIALMA:
            rakipAdi = rakipİsminiAl().decode()
            rakipKazandi = OYUNFONT.render(rakipAdi + " kazandi",0,KIRMIZI)
            rakipKazandiKonum = ((GENISLIK - rakipKazandi.get_width())/2 , (YUKSEKLIK - rakipKazandi.get_height())/2)
        elif islem == ISIMGONDER:
            ismiGonder(ISIM)
        elif islem == KAPAT:
            sleep(3)
            calisiyor = False


def bekleme():
    if saniye % 180 < 60:
        b = 0
    elif 60 <= saniye % 180 < 120:
        b = 1
    elif 120 <= saniye % 180 < 180:
        b = 2
    sahne.blit(BAGLANIYOR[b],BAGLANIYORKONUM[b])

basla = False
anten = Thread(target=veriAlici)
anten.start()



while calisiyor:
    pikselsayisi.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisiyor = False
    if basla:
        spriteBastir(top, cubuk1, cubuk2)
    else:
        continue
    if not baglandi:
        bekleme()
    else:
        tuslar = pygame.key.get_pressed()
        up, down = tuslar[pygame.K_UP], tuslar[pygame.K_DOWN]
        ben.update(up, down)
    if kazanan == IKINCIKAZANDI:
        sahne.blit(rakipKazandi,rakipKazandiKonum)
    elif kazanan == BIRINCIKAZANDI:
        sahne.blit(benKazandim,benKazandimKonum)
    saniye += 1
    if saniye >= 18000:
        saniye = 0
    display.flip()
loglayici.log(kaynak,"Kapatıldı")
