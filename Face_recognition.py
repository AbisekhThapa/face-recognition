

import time
import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyA_P3tiYVvyNJstCE8r883Qy_J_s0ba5z4",
  "authDomain": "homeauto-57275.firebaseapp.com",
  "databaseURL": "https://homeauto-57275-default-rtdb.firebaseio.com",
  "projectId": "homeauto-57275",
  "storageBucket": "homeauto-57275.appspot.com",
  "messagingSenderId": "366173104513",
  "appId": "1:366173104513:web:60142bf408ae72f040e080",
  "measurementId": "G-09FXMSFZSV"
};

firebase=pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()
database = firebase.database()
switch = True

data_path= 'C:/Abisekh/KEC/Hamro/python/face recognition/faces/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]

Training_Data , Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asanyarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asanyarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asanyarray(Training_Data), np.asarray(Labels))

print("Training completed!!!!") 


face_classifier = cv2.CascadeClassifier('C:/Abisekh/KEC/Hamro/python/face recognition/haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return img, []
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    
        return img,roi

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()


    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            confidence = int(100*(1-(result[1])/300))
            display_string = 'Face detected'
        cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_PLAIN,1,(250,120,255),2)

        if confidence > 85:
            cv2.putText(image,"Unlocked",(250,450), cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
            cv2.imshow('Face Cropper', image)
            database.child("Lock")
            data = {
                'Switch' : False
            }
            database.set(data)

              
        else:
            cv2.putText(image,"locked",(250,450), cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
            cv2.imshow('Face Cropper', image)
            database.child("Lock")
            data = {
                'Switch' : True
            }
            database.set(data)


    except:
        cv2.putText(image,"Face not found",(250,300), cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
        cv2.putText(image,"locked",(250,450), cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
        cv2.imshow('Face Cropper', image)
        database.child("Lock")
        data = {
                'Switch' : True
        }
        database.set(data)
        pass
    
    if cv2.waitKey(1)==13:
        break

cap.release()
cv2.destroyAllWindows()