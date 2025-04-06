import cv2
import cvzone
from datetime import datetime
import face_recognition
from firebase_admin import db
import numpy as np
import os  
import pickle
import math
from ultralytics import YOLO
from AddDataToDataBase import data

cap = cv2.VideoCapture(3) # for droid cam
# cap = cv2.VideoCapture(1) # for laptop's webcam
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/background.png")

# IMPORTING MODE IMAGES
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList :
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

modeType = 0
counter = 0
id = -1

# antsipoof  -------------------------------------
confidence = .9
model = YOLO("../models/s_50.pt")
# model = YOLO("../models/l_version_1_300.pt")
classNames = ["fake", "real" ]
prev_frame_time = 0
new_frame_time = 0
cls = 0
conf  = 0
# antsipoof -------------------------------------

def isReal(img):
    results = model(img, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            w, h = x2 - x1, y2 - y1
           
            global conf
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            global cls
            cls = int(box.cls[0])
            if conf > confidence:

                if classNames[cls] == 'real': # send true                    
                    return True
                else:                    
                    return False


def inc_attendance_offline(name):
    for k , v in data.items() :
        if( k == name):
            for k2, v2 in v.items():
                if(k2 == "total attendance"):
                    v2 = v2 + 1                    
                                
while True: 
    succeess, img = cap.read()
    
    imgS = cv2.resize(img, (0,0), None, .25,.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162: 162+480, 55: 55+640] = img # puts up webcam on the BGimg
    imgBackground[44: 44+633, 808: 808+414] = imgModeList[modeType] # puts up webcam on the BGimg

    if faceCurrFrame:         
        for encodeFace , faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            # print("matches = ", matches)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("faceDis = ", faceDis)
            
            matchIdx = np.argmin(faceDis)
            # print("matchIdx = ", matchIdx)
            
            if matches[matchIdx] and isReal(img):
                # print("known face detected", studentIds[matchIdx])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox, rt = 0)
                id = studentIds[matchIdx]
                # print(id)
                
                if (counter == 0):
                    # cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cvzone.putTextRect(img, f'{classNames[cls].upper()} {int(conf*100)}%',
                                   (max(0, x1), max(35, y1)), scale=2, thickness=4,colorR=(0, 255, 0),
                                   colorB=(0, 255, 0))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
            
        if( counter != 0):
            if(counter == 1):
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                
                imgname = studentInfo["sid"]+".jpg"
                imgStudent = cv2.imread(os.path.join("Images/", imgname))           
                
                # UPDATE LAST ATTENDED
                datetimeobj = datetime.strptime(studentInfo["last_attended"],"%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeobj).total_seconds()
                
                if(secondsElapsed > 30):
                    #  UPDATE ATTENDANCE         
                    ref = db.reference(f'Students/{id}')
                    studentInfo["total attendance"] += 1
                    ref.child("total attendance").set(studentInfo["total attendance"])
                    ref.child("last_attended").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    inc_attendance_offline(studentInfo["sid"])
                            

                else:
                    modeType = 3
                    counter = 0             
                    imgBackground[44: 44+633, 808: 808+414] = imgModeList[modeType] # puts up webcam on the BGimg

                
            if( modeType != 3):
                
                if( 10 < counter < 20): 
                    modeType = 2
                
                imgBackground[44: 44+633, 808: 808+414] = imgModeList[modeType] # puts up webcam on the BGimg


                if ( counter<=10):
                    cv2.putText(imgBackground, str(studentInfo["total attendance"]),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    
                    (w,h), _ = cv2.getTextSize(studentInfo["name"], cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentInfo["name"]),(808+offset, 445), cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
            
                    cv2.putText(imgBackground, str(studentInfo["sid"]),(1006, 493), cv2.FONT_HERSHEY_COMPLEX,.5,(255,255,255),1)
            
                    cv2.putText(imgBackground, str(studentInfo["Specialisation"]),(1006,550), cv2.FONT_HERSHEY_COMPLEX,.5,(255,255,255),1)
            
                    imgBackground[175:175+216, 909: 909+216] = imgStudent
                    
                counter += 1
            
                if( counter  >= 20 ):
                    imgname = ""
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = None
                    imgBackground[44: 44+633, 808: 808+414] = imgModeList[modeType] # puts up webcam on the BGimg

            
    else:
        modeType = 0
        counter = 0
        
    
    cv2.imshow("Face Attendance", imgBackground) # gets us bg img
    cv2.waitKey(1)
    
    
