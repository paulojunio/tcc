import numpy as np
import cv2

# Open image and make into numpy array
img1 =cv2.imread('resultTest2.1.jpg')
img2 =cv2.imread('imageTest0.jpg')
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

# Colocar range das cores escolhidas
grau = 30
nivelBaixoVerde = np.array([60 - grau, 100, 100])
nivelAltoVerde = np.array([60 + grau, 255, 255])
img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Limite das cores que serao aceitas
mascaraCor = cv2.inRange(hsv, nivelBaixoVerde, nivelAltoVerde)

# Work out what we are looking for

# Find all pixels where the 3 RGB values match "sought", and count
result = cv2.countNonZero(mascaraCor)

dst = cv2.addWeighted(img1,0.7,img2_resized,0.3,0)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()