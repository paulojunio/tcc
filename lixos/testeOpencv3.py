import numpy as np
import cv2

cap = cv2.VideoCapture("videoplayback.mp4")
substractor = cv2.createBackgroundSubtractorMOG2(
    history=1, varThreshold=50, detectShadows=False)
# Get the Default resolutions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and filename.
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        mask = substractor.apply(frame)
        # write the  frame
        frame_out = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        out.write(frame_out)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
