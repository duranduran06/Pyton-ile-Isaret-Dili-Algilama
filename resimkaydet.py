import cv2
import numpy as np #NumPy (Numerical Python) bilimsel hesaplamaları hızlı bir şekilde yapmamızı sağlayan bir matematik kütüphanesidir. Numpy’ın temelini numpy dizileri oluşturur. Numpy dizileri python listelerine benzer fakat hız ve işlevsellik açısından python listelerinden daha kullanışlıdır.Ayrıca python listelerinden farklı olarak Numpy dizileri homojen yapıda olmalıdır yani dizi içindeki tüm elemanlar aynı veri tipinden olmalıdır.
import os

Kamera=cv2.VideoCapture(0) #kamera görüntüsünü aldım 0 olması pc dırek kamerası 1 harici
isim="dort4"
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
        
        
    
    



























  
    cv2.imshow("EKRANIMIZZZZZZ",Kare) #BUNUDA EKRANDA GOSTERDIM
    cv2.imshow("kesilenkare",kesilmiş_kare)
    cv2.imshow("FİLTRE",thresh1)
    cv2.imshow("sonuc",sonuc)
    
    if cv2.waitKey(25) & 0xFF==ord('ç'):  # ç basınca çıkar ,,açılan pencereyı kapatmak için  kamera görüntüsünü kapatmak için whiledan cıkmak ıcın
        break
    
cv2.imwrite("kaydet/"+isim+".jpg",thresh1)  
Kamera.release() #kamera işlemını sonlandırdı
cv2.destroyAllWindows()# cv2 ile açılan tüm pencerelerı kapatalım
 
