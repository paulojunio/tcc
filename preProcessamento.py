# Trabalho de conclusao de curso -- PUC Minas
# Aluno: Paulo Junio -- 565544 -- pjrrodrigues@sga.pucminas.br
# Orientador: Alexei Machado -- alexeimcmachado@gmail.com
# Nome do Trabalho...
# Breve Explicao...

import cv2
import numpy as np
import imutils


def custom_sort(t):
    return t[0]


capturaDoVideo = cv2.VideoCapture("inputECG.mp4")
substractor = cv2.createBackgroundSubtractorMOG2(
    history=30, varThreshold=16, detectShadows=False)

larguraDoQuadro = int(capturaDoVideo.get(3))
alturaDoQuadro = int(capturaDoVideo.get(4))

# Define o codec do video e seu nome
saida = cv2.VideoWriter('outputECG.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 30, (larguraDoQuadro, alturaDoQuadro))

listaDePontos = []
flag = 1
retangulo = None
pontoEsquerda = 0
teste = 0

while (capturaDoVideo.isOpened()):

    ret, quadro = capturaDoVideo.read()
    if flag:
        # Selecionar o ROI
        retangulo = cv2.selectROI(quadro)
        flag = 0
    if ret == True:
        # print(retangulo)
        # Pegando somente um parte do video
        x, y, w, h = retangulo
        cv2.rectangle(quadro, (x, y), (x+w, y+h), (255, 0, 0), 2)
        quadroRecortado = np.zeros_like(quadro)
        quadroRecortado[y:y+h, x:x+w] = quadro[y:y+h, x:x+w]

        # Transformando BGR para HSV
        hsv = cv2.cvtColor(quadroRecortado, cv2.COLOR_BGR2HSV)

        # Colocar range das cores escolhidas
        grau = 15
        nivelBaixoVerde = np.array([60 - grau, 100, 100])
        nivelAltoVerde = np.array([60 + grau, 255, 255])

        # Limite das cores que serao aceitas
        mascaraCor = cv2.inRange(hsv, nivelBaixoVerde, nivelAltoVerde)

        # Aplicando uma soma com o quadro original com a mascara criada de cor
        res = cv2.bitwise_and(
            quadroRecortado, quadroRecortado, mask=mascaraCor)

        # Aplicando um fitro Gaussiano para tirar ruidos
        # quadroCinza = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # quadroCinza = cv2.GaussianBlur(quadroCinza, (3, 3), 0)

        # Quadro final com a aplicao do algoritmo mog2
        # quadroFinal = substractor.apply(quadroCinza)
        quadroFinal = substractor.apply(res)
        """
        quadroFinal = cv2.dilate(quadroFinal, None, iterations=1) 
        quadroFinal = cv2.erode(quadroFinal, None, iterations=1) 
        """
        
        contornos = cv2.findContours(quadroFinal.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)
        numeroDeSegmentos = 0

        pontoEsquerda = 0
        cXFull = 10000
        cYFull = 10000
        teste += 1
        for c in contornos:
            numeroDeSegmentos += 1
        # looping for contours
        for c in contornos:
            if (numeroDeSegmentos > 50):
                continue
            # print(cv2.contourArea(c))
            if cv2.contourArea(c) < 5:
                continue

            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if(pontoEsquerda == 1):
                # print("Entro", cX, ' ', cXFull)
                if(cX > cXFull):
                    # print("ferrou")
                    continue

            cXFull = cX
            cYFull = cY
            pontoEsquerda = 1
            # get bounding box from countour
            # (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            # cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.drawContours(res, c, -1, (0, 255, 0), 3)

        cv2.circle(res, (cXFull, cYFull), 3, (0, 0, 255), -1)
        if cXFull != 10000:
            listaDePontos.append([cXFull, cYFull])

        # Modo para gravar o video...
        # quadroFinalVideo = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)
        saida.write(res)

        # Renderizacao dos dois quadros, original e final
        cv2.imshow('Video Original', res)
        cv2.imshow('Tela Final', quadroFinal)

        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break
    else:
        break

# print(listaDePontos[2], 'tamanho : ', len(listaDePontos))
x, y, w, h = retangulo
numeroImagem = 0
flagImagem = 2

while(True):

    novaImagem = np.zeros(
        (y+h, x+w, 3), dtype=np.uint8)
    # novaImagem = cv2.cvtColor(novaImagem, cv2.COLOR_BGR2HSV)
    aux = flagImagem
    listAux = []
    # print('Passo aqui ', flagImagem)
    for ponto in range(len(listaDePontos)-aux):

        pontos = listaDePontos[ponto+aux]
        flagImagem += 1
        pontosAnteriores = listaDePontos[ponto+aux-1]
        listAux.append(pontos)
        if(pontos[0] + 150 < pontosAnteriores[0]):
            # print(pontos[0], ' ', pontosAnteriores[0])
            break

        cv2.circle(novaImagem, (pontos[0], pontos[1]), 1, (0, 0, 255), -1)

        #cv2.line(novaImagem, (pontosAnteriores[0], pontosAnteriores[1]),
        #         (pontos[0], pontos[1]), (0, 0, 255), 2)

    """
    print(len(listAux))
    listAux.sort(key=custom_sort)

    for ponto in range(len(listAux) - 1):
        pontos = listAux[ponto+1]
        pontosAnteriores = listAux[ponto-1]
        cv2.line(novaImagem, (pontosAnteriores[0], pontosAnteriores[1]),
                 (pontos[0], pontos[1]), (0, 0, 255), 2)
    """
    nomeImage = 'imageTest' + str(numeroImagem) + '.jpg'
    numeroImagem += 1
    cv2.imwrite(nomeImage, novaImagem)

    if(flagImagem >= len(listaDePontos)):
        break


capturaDoVideo.release()
saida.release()
cv2.destroyAllWindows()
"""
imageFlag = 0
numeroImagens = 0
while(imageFlag < len(listaDePontos)):
"""
