import cv2
import numpy as np

cap = cv2.VideoCapture("highway.mp4")
substractor = cv2.createBackgroundSubtractorMOG2()
out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
while True:
    _,frame = cap.read()
    mask = substractor.apply(frame)

    cv2.imshow("Frame", frame)
    cv2.imshow("Frame_Mog2", mask)

    out.write(mask)
    key = cv2.waitKey(30)
    if key == 27:
        break

out.realese()
cap.realese()
cv2.destroyAllWindows()