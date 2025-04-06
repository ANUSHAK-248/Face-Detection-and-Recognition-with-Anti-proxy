import cv2
import face_recognition
import pickle
import os
from firebase_admin import db

folderPath = "Images"
PathList = os.listdir(folderPath)

imgList = []
studentIds = []
for path in PathList :
    imgList.append(cv2.imread(os.path.join(folderPath, path)))    
    studentIds.append(os.path.splitext(path)[0])
   
def findEncodings(imagesList):
    encodeList = []
    for idx, img in enumerate(imagesList):
        # OpenCV uses BGR, face_recognition uses RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            encodeList.append(encodings[0])
        else:
            print(f"Warning: No face detected in image at index {idx}")
    return encodeList

print("Encoding starts")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
# print(encodeListKnown)
print("Encoding ends")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("file saved")