from pygame import *
import pygame
from pygame import font
init()
############
# BAĞLANTI #
############

PORT = 19274
IP = "192.168.1.120"
BAGLANDI = 3
BAGLANMADI = 4
BEKLEMESURESI = 5
ACILISKONUMLAR = 1
KONUMLAR = 2
KAZANMA  = 3
BAGLANMA = 4
RAKIPADINIALMA = 5
ISIMGONDER = 6
KAPAT = 7

###########
# RENKLER #
###########

YESIL = (78, 191, 55)
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (0, 191, 255)
KIRMIZI = (255,0,0)

#########
# EKRAN #
#########

GENISLIK = 800
YUKSEKLIK = 600
BOYUT = (GENISLIK, YUKSEKLIK)

########
# YAZI #
########

PUNTO = 30
OYUNFONT = font.Font("font/PressStart2PRegular.ttf",PUNTO)

########
# OYUN #
########

ISIM = "Eyup"
FPS = 60
HIZLANMA = 1
_yonler = range(-3, 4)
_yonler = list(_yonler)
_yonler.remove(0)
YONLER = tuple(_yonler)
BIRINCIKAZANDI =1
IKINCIKAZANDI = 2
MAKSOYUNCUISMIUZUNLUGU = 16
LOGLAMA = False

##########
# GÖRSEL #
##########

CUBUK = pygame.image.load("image/cubuk.png")
TOPGORSEL = pygame.image.load("image/top.png")
ARKAPLAN = pygame.image.load("image/arkaplan.png")
BAGLANIYOR = tuple(OYUNFONT.render("Diğer oyuncu bekleniyor"+f,0,MAVI) for f in (".","..","..."))

#########
# KONUM #
#########

UZAKLIK = 30
BAGLANIYORKONUM = tuple(((GENISLIK - bagla.get_width())/2 , (YUKSEKLIK - bagla.get_height())/2) for bagla in BAGLANIYOR)
TOPBASLANGICKONUM = (int((BOYUT[0] - TOPGORSEL.get_width())/2),
          int((BOYUT[1] - TOPGORSEL.get_height())/2))
CUBUK1BASLANGICKONUM = (UZAKLIK, int((BOYUT[1] - CUBUK.get_height())/2))
CUBUK2BASLANGICKONUM = (BOYUT[0] - (UZAKLIK + CUBUK.get_width()),
             int((BOYUT[1] - CUBUK.get_height())/2))