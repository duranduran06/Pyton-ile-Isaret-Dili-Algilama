import cv2
import numpy as np #NumPy(nampay) (Numerical Python) bilimsel hesaplamaları hızlı bir şekilde yapmamızı sağlayan bir matematik kütüphanesidir. Numpy’ın temelini numpy dizileri oluşturur. Numpy dizileri python listelerine benzer fakat hız ve işlevsellik açısından python listelerinden daha kullanışlıdır.Ayrıca python listelerinden farklı olarak Numpy dizileri homojen yapıda olmalıdır yani dizi içindeki tüm elemanlar aynı veri tipinden olmalıdır.
import os
import time

Kamera=cv2.VideoCapture(0) #kamera görüntüsünü aldım 0 olması pc dırek kamerası 1 harici

def ResimFarkBul(Resim1,Resim2):#resım1 kthreshden kameradan gelen ,,resim2 de klasordekı
    Resim2=cv2.resize(Resim2,(Resim1.shape[1],Resim1.shape[0])) #resım boyutları farklı olabılır onları boyutlandırdım resım2 yı resım1 ıle aynnı yapyım
    fark_resim=cv2.absdiff(Resim1,Resim2)
    fark_sayı=cv2.countNonZero(fark_resim)
    return fark_sayı
veri_resmi=cv2.imread("kaydet/"+"yumruk.jpg",0)





#burada klasordekı resımlerı ve resimlerin isimlerini çekıyoruz
def veriyükle():
    veri_isimler=[]
    veri_resimler=[]
    dosyalar=os.listdir("kaydet/")#verdiğimiz yerdekı verilerin isimlerini  sıralıyo
    for dosya in dosyalar:#hepsine tek tek bakıyorum
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















veri_isimgeldi,veri_resimgeldi=veriyükle()#veriyıkleden gelen degerler











#dögü ile çerceveyi alıp ekrana yerlestircez
while True:
    tf,Kare=Kamera.read()# kameradan gelen görüntüyü kareye aldık   baştki TF GÖRÜNTÜ var ise kamera içinde true yoksa false ol diyo
    kesilmiş_kare=Kare[0:350,0:350]



    #gelen resmı threshold(tireşold ) bu ne demek = eşik değeridir griye cevrılmıs resmı siyah beyaz halıne çeviriyo ,buda cismi bulmamızda aşırı kolaylık sağlıyo
    gray=cv2.cvtColor(kesilmiş_kare,cv2.COLOR_BGR2GRAY)#Gri tonlamalı bir görüntü düşünelim.Gri tonlamalı bir resim yalnızca yoğunluk bilgisi gerektirir yani belirli bir pikselin ne kadar parlak olduğu bilgisi.
    #Değer ne kadar yüksek olursa yoğunluk o kadar yüksektir(gri tonla çoğu iş yapıldıgından karmasık renklerre işlenmesi zor renklere gerek yok),,,,,,Giriş olarak verilen görüntüyü ikili görüntüye çevirmek için kullanılan bir yöntemdir...threshold yapabılmek için gri ye cevırdım alttakı yoksa calısmaz
    tr,thresh1=cv2.threshold(gray,100,200,cv2.THRESH_OTSU)#otsuda parlak alanları siliyo koyu alanları bırakıyo ,,,beyaza yakınsa beyaz alır siyaha yakındsa siyah alır
    #yukarda ilk değer parlak yerlerı alma yükseldıkçe parlak olan yerler alınır sadece,,ikinci değerde ağarma

   

    #ELİMİZİ TESPİT ETME YADA ELLERİMİZİN RESMINI ÇIKARMA
   # sınıflan=cv2.CascadeClassifier("hand.xml")
    #sonuc=sınıflan.detectMultiScale(gray,1.1,5)
    #for(x,y,genislik,yukseklik) in sonuc:
     #   cv2.rectangle(kesilmiş_kare,(x,y),(x+genislik+15,y+yukseklik+20),(0,255,0),2)


    sonuc=kesilmiş_kare.copy()
    cnts,_=cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) # burada kare varmı dıye buluyoooooo thresh de eğer varsa altta sonuç uzerıne çiziyo
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
        cv2.rectangle(sonuc,(x,y),(x+w,y+h),(0,250,0),2)#sonuç üzerine kare cızıo
        print(sınıflandır(thresh1,veri_isimgeldi,veri_resimgeldi))
        
    
    



























  
    cv2.imshow("EKRANIMIZZZZZZ",Kare) #BUNUDA EKRANDA GOSTERDIM
    cv2.imshow("kesilenkare",kesilmiş_kare)
    cv2.imshow("FİLTRE",thresh1)
    cv2.imshow("sonuc",sonuc)
    
    if cv2.waitKey(25) & 0xFF==ord('ç'):  # ç basınca çıkar ,,açılan pencereyı kapatmak için  kamera görüntüsünü kapatmak için whiledan cıkmak ıcın
        break
    
    
Kamera.release() #kamera işlemını sonlandırdı
cv2.destroyAllWindows()# cv2 ile açılan tüm pencerelerı kapatalım
 
