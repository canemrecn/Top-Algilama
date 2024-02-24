import cv2
import imutils
import sys
#Gerekli modülleri import etme
if sys.platform=='win32':
    deltax=0
    deltay=0
else:
    deltax=50
    deltay=105
# Platforma göre deltax ve deltay değerlerini ayarla
video_dosya=''
# Video dosyasının yolu ve adı (boş ise kameradan okuma yapılacak)
GENİSLİK=600
# Kare genişliği
SADECE_MAX=False
# Sadece en büyük konturu kullanma
YESİL= ((29,86,6),(64,255,255))
# YESİL renk aralığı (alt ve üst sınırlar)
KIRMIZI=((139,0,0),(255,160,122))
# KIRMIZI renk aralığı (alt ve üst sınırlar)
MAVI=((110,50,50),(130,255,255))
# MAVI renk aralığı (alt ve üst sınırlar)
TURUNCU=((160,100,47),(179,255,255))
# TURUNCU renk aralığı (alt ve üst sınırlar)
SARI=((10,100,100),(40,255,255))
# SARI renk aralığı (alt ve üst sınırlar)
altRenk,ustRenk = MAVI
# İşlenecek renk aralığına göre alt ve üst sınırları ayarla
if len(video_dosya)==0:
    kamera = cv2.VideoCapture(0)
# Kameradan okuma yap (varsayılan kamera = 0)
else:
    kamera=cv2.VideoCapture(video_dosya)
# Dosyadan okuma yap
cv2.namedWindow('kare')
cv2.moveWindow('kare',10,10)
cv2.namedWindow('maske')
cv2.moveWindow('maske',GENİSLİK+deltax,10)
# Pencereleri oluştur ve konumlandır
while True:
    (ok, kare) = kamera.read()
# Kareden okuma yap
    if len(video_dosya)>0 and not ok:
# Dosyanın sonuna gelindi
        break
    kare = imutils.resize(kare,GENİSLİK)
# Kareyi yeniden boyutlandır
    hsv = cv2.GaussianBlur(kare, (25,25), 0)
# Gürültüyü azaltmak için Gaussian bulanıklığı uygula
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
# Kareyi HSV renk uzayına dönüştür
    maske= cv2.inRange(hsv, altRenk, ustRenk)
# Renk aralığına göre bir maske oluştur
    maske= cv2.erode(maske, None, iterations=3)
# Maskeyi erozyon işlemine tabi tut
    maske= cv2.dilate(maske, None, iterations=3)
# Maskeyi genişlet
    kopya= maske.copy()
# Maske kopyasını al
    konturlar, _ = cv2.findContours(kopya, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Konturları bul
    if len(konturlar)>0:
        for kontur in konturlar:
            cmax = max(konturlar, key=cv2.contourArea)
# En büyük konturu bul
            if SADECE_MAX:
                (x,y), yaricap = cv2.minEnclosingCircle(cmax)
# En büyük konturun çevreleyen daireyi hesapla
            else:
                (x, y), yaricap = cv2.minEnclosingCircle(kontur)
# En büyük konturun çevreleyen daireyi hesapla
            if yaricap >= 10:
                cv2.circle(kare, (int(x), int(y)), int(yaricap), (0, 0, 255), 4)
# Kare üzerine daire çiz
    cv2.imshow('kare', kare)
# Kareyi göster
    cv2.imshow('maske', maske)
# Maskeyi göster
    k=cv2.waitKey(4) & 0xFF
    if k==ord('q') or k==27:
        break
kamera.release()
cv2.destroyAllWindows()
