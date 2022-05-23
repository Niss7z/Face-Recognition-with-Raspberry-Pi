import cv2
import numpy as np
import os
import face_recognition
import RPi.GPIO as GPIO
import time

# Door Servo
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # set it as board so that one can simply use pin numbers
GPIO.setup(11, GPIO.OUT) # set the specific pin as output
pwm=GPIO.PWM(11,50) # set pulse rate of the servo for that specific pin
pwm.start(1)
pin = 11
faceDetected = 0

def get_pwm(angle):
    return (angle/18.0) + 2.5 # converting angles to duty cycle

def unlockDoor(pinNum):
    global faceDetected # declare this as global variable so that we may use it later
    if faceDetected == 10:
        print('unlocking')
        GPIO.output(pinNum, True)
        pwm.ChangeDutyCycle(get_pwm(180)) #unlock
        time.sleep(10)
        pwm.ChangeDutyCycle(get_pwm(0)) #lock
        time.sleep(1)
        faceDetected = 0 

directory = 'faceTrain'
images = []
names = []
List = os.listdir(directory)
print(List)

for n in List:  # importing current image and remove extensions of picture types for names(.jpeg, .png, etc.)
    currentImg = cv2.imread(f'{directory}/{n}')
    images.append(currentImg)
    names.append(os.path.splitext(n)[0])
print(names)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

capture = cv2.VideoCapture(0)

while True:  # smaller image scale for better detection
    success, img = capture.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    ret, frame = capture.read()
    
    facesCurrentFrame = face_recognition.face_locations(imgSmall)
    encodesCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)
    
    for encodeFace, faceLocation in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDistance)
        matchIndex = np.argmin(faceDistance)
        if matches[matchIndex] and float(faceDistance[matchIndex]) < 0.37: # if confidence is below 0.37 then don't rpint
            name = names[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, name, (x1+7, y2-7),cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
            faceDetected += 1
            unlockDoor(pin)
            print(f'# of times detected ={faceDetected}')
            prevName = name
            if name != prevName:
                faceDetected = 0 # if the previous name is not equal to the current name, in order words if A.I detects person differently, restart the count


        else:
            print('unknown')
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'unknown', (x1 + 7, y2 - 7), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
            faceDetected = 0 # whenever a face is detected as 'unknown' reset the count - this is for security purposes
            print(f'# of times detected ={faceDetected}') 
            
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
