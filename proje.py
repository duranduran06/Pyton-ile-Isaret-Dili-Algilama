import cv2
import numpy as np 
import os
import time

Kamera=cv2.VideoCapture(0) 

def ResimFarkBul(Resim1,Resim2):
    Resim2=cv2.resize(Resim2,(Resim1.shape[1],Resim1.shape[0])) 
    fark_resim=cv2.absdiff(Resim1,Resim2)
    fark_sayı=cv2.countNonZero(fark_resim)
    return fark_sayı
veri_resmi=cv2.imread("kaydet/"+"yumruk.jpg",0)




#burada klasordekı resımlerı ve resimlerin isimlerini çekıyoruz
def veriyükle():
    veri_isimler=[]
    veri_resimler=[]
    dosyalar=os.listdir("kaydet/")
    for dosya in dosyalar:
        veri_isimler.append(dosya.replace(".jpg",""))# .jpglerini siliyorum ve isimler dizime atıyorum
        veri_resimler.append(cv2.imread("kaydet/"+dosya,0))
    return veri_isimler,veri_resimler






#klasordekı resımler ıle kameradakı hareketı karsılastırıp en az farkı olanı bulup ekrana o hangı resimse ismini basıyoruz
def sınıflandır(resim,veri_isimler,veri_resimler):
    
    min_ındex=0
    min_değer=ResimFarkBul(resim,veri_resimler[0])
    for t in range(len(veri_isimler)):
        fark_değer=ResimFarkBul(resim,veri_resimler[t])
        if(fark_değer<min_değer):
            min_değer=fark_değer
            min_ındex=t
    return veri_isimler[min_ındex]


veri_isimgeldi,veri_resimgeldi=veriyükle()

#dögü ile çerceveyi alıp ekrana yerlestircez
while True:
    tf,Kare=Kamera.read()
    kesilmiş_kare=Kare[0:350,0:350]



    #gelen resmı threshold bu ne demek = eşik değeridir griye cevrılmıs resmı siyah beyaz halıne çeviriyo ,buda cismi bulmamızda aşırı kolaylık sağlıyo
    gray=cv2.cvtColor(kesilmiş_kare,cv2.COLOR_BGR2GRAY)
    tr,thresh1=cv2.threshold(gray,100,200,cv2.THRESH_OTSU)
    sonuc=kesilmiş_kare.copy()
    cnts,_=cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    max_genislik=0
    max_yukseklık=0
    max_ındex=-1
    
    for t in range(len(cnts)):
        cnt=cnts[t]
        x,y,w,h =cv2.boundingRect(cnt)
        if(w>max_genislik and h>max_yukseklık):
            max_yukseklık=h
            max_genislik=w
            max_ındex=t
    if(len(cnts)>0):
        x,y,w,h=cv2.boundingRect(cnts[max_ındex])
        cv2.rectangle(sonuc,(x,y),(x+w,y+h),(0,250,0),2)
        print(sınıflandır(thresh1,veri_isimgeldi,veri_resimgeldi))
        
 
    cv2.imshow("EKRANIMIZZZZZZ",Kare) 
    cv2.imshow("kesilenkare",kesilmiş_kare)
    cv2.imshow("FİLTRE",thresh1)
    cv2.imshow("sonuc",sonuc)
    
    if cv2.waitKey(25) & 0xFF==ord('ç'): 
        break
    
    
Kamera.release() 
cv2.destroyAllWindows()
 
