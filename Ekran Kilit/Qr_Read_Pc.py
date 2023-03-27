from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys,os,qr_code,time
import numpy as np
from threading import Thread
import keyboard
from gtts import *
import logging
from  playsound import playsound
import mysql.connector
import cv2
import datetime
import uuid


#now = datetime.datetime.utcnow()
import mysql.connector


 
mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Merveot",
    database="bmh204"
)
cursor = mysqldb.cursor()

class main_windows(QWidget):
    def __init__(self):
        self.sayac=0
        super().__init__()
        ############################################################# pencere boyutu
        #self.setFixedSize(1920,1080)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setStyleSheet("background-color:black;")

        ##########################################################  blok anahtarlar
        self.block_keys=[91,1,15,29,56]

        """windows tuşu 91  
            ctrl    tuşu 29
            alt     tuşu  56
            shift   tuşu  42
            esc     tuşu   1
            tab     tuşu  15"""


        ##############################################################  rastgele şifre
        self.qr_img="pasword.png"
        self.pasword_qr=self.random_pasword(4)
        qr_code.make_qr_code(self.pasword_qr,self.qr_img)
    

        time.sleep(2)
        self.etiketler()

    ################################################################   blok klavye kontrol tuşları
    def blockinput_stop(self):  ################### to unlock
        for i in self.block_keys:
            keyboard.unblock_key(i)

    def blockinput_start(self):  #####################   kilitleme
        for i in self.block_keys:
            keyboard.block_key(i)
    def blockinput(self):
        self.keys_lock_start=Thread(target=self.blockinput_start())
        self.keys_lock_start.start()
        print("[SUCCESS] Input blocked!")


    def random_pasword(self,size):

        key="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuopasdfghjklizxcvbnmé!'^+%&/()=?_1234567890*-<>"
        new_pasword=""
        for i in range(size):
            new_pasword+=key[np.random.randint(len(key))]
        return new_pasword
        

    def quit_windows(self):
        exit()

    # mac_address = hex(uuid.getnode()).replace('0x', '').upper()
    # my_list = [str(mac_address)]
    # print(mac_address)
    # cursor = mysqldb.cursor( )
    # sql = cursor.execute("INSERT INTO mac_addresses(address) VALUES (%s)", (my_list))

    # cursor.execute(sql)
    # mysqldb.commit( )
    ###############################################################  şifre kontrol
    def open_windows(self):
    

        if self.url.text()==self.pasword_qr:
            self.hiden.setText("passworld true , it is out ..")
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
            sql= cursor.execute("INSERT INTO GirisLog(Tarih,Mesaj)  VALUES(%s,%s)" ,(time.strftime('%Y-%m-%d %H:%M:%S'),"Başarılı Giriş"))
            cursor.execute(sql)
            mysqldb.commit()   
            print(str(sql)+"Başarılı Giriş Eklendi")
            logging.warning("Başarılı Giriş")
            self.keys_lock_start.stop()
            self.blockinput_stop()
            Thread(target = self.quit_windows()).start()


        else:
            self.setStyleSheet("background-color:red;")
            self.hiden.setText("!!! hatalı parola")

            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            cap = cv2.VideoCapture(0)
            count=0 
           


            while True:
                ret ,frame = cap.read()
                grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=face_cascade.detectMultiScale(grey,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
                count+=1

                for(x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.imwrite("Fotograflar/User." + str(uuid.uuid4().hex) + '.' + str(count) + ".jpg", grey[y:y+h,x:x+w])
                    cv2.imshow("video",frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif count >0:
                    break
            cap.release()
            cv2.destroyAllWindows()
        
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
            fotografAdresi="User." + str(uuid.uuid4().hex) + '.' + str(count) + ".jpg"
            sql= cursor.execute("INSERT INTO GirisLog(Tarih,Mesaj,FotografAdi)  VALUES(%s,%s,%s)" ,(time.strftime('%Y-%m-%d %H:%M:%S'),"Hatalı Giriş",fotografAdresi))
            cursor.execute(sql)
            mysqldb.commit()   
            print(str(sql)+"Hatalı Giriş Saptandı")
            logging.warning("Hatalı Giriş")
            self.sayac +=1
            if self.sayac == 3:
                self.hiden.setText("!!! ŞÜPHELİ GİRİŞ!!!")
                playsound("alarm.mp3")
        self.url.setText("")

        
    def etiketler(self):
        ###############################################  uygulama ana simgesi
        self.yazı = QLabel(self)
        self.yazı.setPixmap(QPixmap(self.qr_img))
        self.yazı.setGeometry(200, 30, 200, 200)
        ###############################################   files the url
        self.url = QLineEdit(self)
        self.url.setFont(QFont("Ariel", 12))
        self.url.setStyleSheet("color:white;")
        ###############################################   the button dowloand files
        self.git = QPushButton(self)
        self.git.setText("GİT")
        self.git.setFont(QFont("Ariel", 10))
        self.git.setStyleSheet("background-color:white;")
        self.git.clicked.connect(self.open_windows)
        #####################################################################
        ############################################### parola hattalı ve doğru için
        self.hiden = QLabel(self)
        self.hiden.setFont(QFont("Ariel", 13))
        self.hiden.setText("!!!Karekodu telefondaki uygulamaya okutup şifreyi girin!!!")
        self.hiden.setStyleSheet("color:white;")
       
        
        self.blockinput()

        ###############################################   argümanlar
        v = QVBoxLayout()
        l=QHBoxLayout()
        l.addStretch()
        l.addWidget(QLabel("<h1 style='color:white;' ><i> LOCK SCREEN </i></h1>"))
        l.addStretch()
        v.addLayout(l)

        k=QHBoxLayout()
        k.addStretch()
        k.addWidget(self.yazı)
        k.addStretch()
        v.addLayout(k)
        v.addStretch()
        v.addStretch()

        h = QHBoxLayout()
        h.addStretch()
        h.addStretch()
        h.addWidget(QLabel("<h3 style='color:white;'> pasworld : </h3>"))
        h.addWidget(self.url)
        h.addStretch()
        h.addStretch()
        v.addLayout(h)
        v.addStretch()

        hidden=QHBoxLayout()
        hidden.addStretch()
        hidden.addStretch()
        hidden.addStretch()
        hidden.addWidget(self.hiden)
        hidden.addStretch()
        hidden.addStretch()
        hidden.addStretch()
        v.addLayout(hidden)
        v.addStretch()
        ############################  Button
        b=QHBoxLayout()
        b.addStretch()
        b.addStretch()
        b.addStretch()
        b.addWidget(self.git)
        b.addStretch()
        b.addStretch()
        b.addStretch()
        v.addLayout(b)
        v.addStretch()
        ############################ profile qr_code
        self.setLayout(v)

    #################################alt+f4 kitleme####################################

    def closeEvent(self, event):
        event.ignore()


if __name__ == '__main__':
   app=QApplication(sys.argv)
   dowland=main_windows()
   dowland.show()
   sys.exit(app.exec_())




