import threading
import winsound

import cv2
import imutils

# variables 
VARD = 500000

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

_ , startFrame = capture.read()
startFrame = imutils.resize(startFrame, width = 500)

startFrame = cv2.cvtColor(startFrame, cv2.COLOR_BGR2GRAY)

startFrame = cv2.GaussianBlur(startFrame, (21, 21), 0)

alarm = False
alarmMode = False
alarmCounter = 0

def alarmTrigger():
    global alarm 
    for _ in range(5):
        if not alarmMode:
            break
        print("WARNING TRIGGER!")
        winsound.Beep(2500, 1000)
    alarm = False    

while True:
    _ , frame = capture.read()
    frame = imutils.resize(frame, width=500)

    if alarmMode:
        frameTW = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameTW = cv2.GaussianBlur(frameTW, (5, 5), 0)

        frameDiff = cv2.absdiff(frameTW, startFrame)
        threshold = cv2.threshold(frameDiff, 25, 255, cv2.THRESH_BINARY)[1]

        startFrame = frameTW

        if threshold.sum() > VARD:
            alarmCounter += 1
        else:
            if alarmCounter > 0:
                alarmCounter -= 1
        
        cv2.imshow("Camera capture", threshold)
    else:
        cv2.imshow("Camera capture", frame)

    if alarmCounter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=alarmTrigger).start()

    keyPressed = cv2.waitKey(30)
    if keyPressed == ord("r"):
        alarmMode = not alarmMode
        alarmCounter = 0

    if keyPressed == ord("q"):
        alarmMode = False
        break

capture.release()
cv2.destroyAllWindows()

