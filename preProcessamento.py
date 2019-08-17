import cv2
import numpy as np


capturaDoVideo = cv2.VideoCapture("videoplayback.mp4")
substractor = cv2.createBackgroundSubtractorMOG2(
    history=1, varThreshold=10, detectShadows=False)

while (1):
    # Pegando os quadros do video
    _, quadro = capturaDoVideo.read()

    # Transformando BGR para HSV
    hsv = cv2.cvtColor(quadro, cv2.COLOR_BGR2HSV)

    # Colocar range das cores escolhidas
    grau = 15
    nivelBaixoVerde = np.array([60 - grau, 100, 100])
    nivelAltoVerde = np.array([60 + grau, 255, 255])

    # Threshold the HSV image to get only blue colors
    mascaraCor = cv2.inRange(hsv, nivelBaixoVerde, nivelAltoVerde)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(quadro, quadro, mask=mascaraCor)

    quadroFinal = substractor.apply(res)

    cv2.imshow('Video Original', quadro)
    cv2.imshow('Tela Final', quadroFinal)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
