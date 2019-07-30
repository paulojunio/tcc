import cv2
import numpy as np

cap = cv2.VideoCapture("teste.flv")
substractor = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=50, detectShadows = False)

while True:
    _,frame = cap.read()
    mask = substractor.apply(frame)

    cv2.imshow("Frame", frame)
    cv2.imshow("Frame_Mog2", mask)

    key = cv2.waitKey(30)
    if key == 27:
        breakd

out.realese()
cap.realese()
cv2.destroyAllWindows()