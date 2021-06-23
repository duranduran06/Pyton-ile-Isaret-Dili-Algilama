import cv2
import numpy as np
import os

Kamera=cv2.VideoCapture(0) 
isim="dort4"
while True:
    tf,Kare=Kamera.read()
    kesilmiş_kare=Kare[0:350,0:350]
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
    cv2.imshow("EKRANIMIZZZZZZ",Kare)
    cv2.imshow("kesilenkare",kesilmiş_kare)
    cv2.imshow("FİLTRE",thresh1)
    cv2.imshow("sonuc",sonuc)
    if cv2.waitKey(25) & 0xFF==ord('ç'): 
        break
cv2.imwrite("kaydet/"+isim+".jpg",thresh1)  
Kamera.release() #kamera işlemını sonlandırdı
cv2.destroyAllWindows()# cv2 ile açılan tüm pencerelerı kapatalım
 
