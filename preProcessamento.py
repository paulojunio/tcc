# Trabalho de conclusao de curso -- PUC Minas
# Aluno: Paulo Junio -- 565544 -- pjrrodrigues@sga.pucminas.br
# Orientador: Alexei Machado -- alexeimcmachado@gmail.com
# Nome do Trabalho...
# Breve Explicao...

import cv2
import numpy as np


capturaDoVideo = cv2.VideoCapture("inputECG.mp4")
substractor = cv2.createBackgroundSubtractorMOG2(
    history=30, varThreshold=16, detectShadows=False)

larguraDoQuadro = int(capturaDoVideo.get(3))
alturaDoQuadro = int(capturaDoVideo.get(4))

# Define o codec do video e seu nome
saida = cv2.VideoWriter('outputECG.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 30, (larguraDoQuadro, alturaDoQuadro))
# Select ROI
#_, primeiroQuadro = capturaDoVideo.read()
#r = cv2.selectROI(primeiroQuadro, False, False)
# Crop image

while (capturaDoVideo.isOpened()):

    # Pegando os quadros do video
    _, quadro = capturaDoVideo.read()

    # Pegando somente um parte do video
    #r = cv2.selectROI(quadro, False, False)
    #quadro = quadro[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Transformando BGR para HSV
    hsv = cv2.cvtColor(quadro, cv2.COLOR_BGR2HSV)

    # Colocar range das cores escolhidas
    grau = 15
    nivelBaixoVerde = np.array([60 - grau, 100, 100])
    nivelAltoVerde = np.array([60 + grau, 255, 255])

    # Limite das cores que serao aceitas
    mascaraCor = cv2.inRange(hsv, nivelBaixoVerde, nivelAltoVerde)

    # Aplicando uma soma com o quadro original com a mascara criada de cor
    res = cv2.bitwise_and(quadro, quadro, mask=mascaraCor)

    # Aplicando um fitro Gaussiano para tirar ruidos
    #quadroCinza = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    #quadroCinza = cv2.GaussianBlur(quadroCinza, (5, 5), 0)

    # Quadro final com a aplicao do algoritmo mog2
    #quadroFinal = substractor.apply(quadroCinza)
    quadroFinal = substractor.apply(res)

    # Modo para gravar o video...
    quadroFinalVideo = cv2.cvtColor(quadroFinal, cv2.COLOR_GRAY2RGB)
    saida.write(quadroFinalVideo)

    # Renderizacao dos dois quadros, original e final
    cv2.imshow('Video Original', quadro)
    cv2.imshow('Tela Final', quadroFinal)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

capturaDoVideo.release()
saida.release()
cv2.destroyAllWindows()
