import time
import pygame
import pygame_gui
import numpy as np
import sys 
import tkinter
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
import matplotlib as mpl
import matplotlib.pyplot as plt



#iniciamos pygame
pygame.init()
pygame.display.set_caption("CONWAY'S GAME OF LIFE")
# Ancho y alto de la pantalla
width, height = 500,500
#creacion de la pantalla
screen = pygame.display.set_mode((height, width))

manager = pygame_gui.UIManager((height,width))

clock = pygame.time.Clock()

color = colorchooser.askcolor()[1]

#colorr del fondo =  casi negro, casi oscuro
bg = 25, 25, 25
#pintamos el fondo con el color elegido
screen.fill(bg)

#Numero de celdas
nxC,  nyC =  25, 25
#Dimensiones de la celda
dimCM = width /  nxC
dimCH = height /  nyC


root = tkinter.Tk()
root.wm_title("Game of life")

#Estado de las celdas , Vivas = 1 Muertas = 0
gameState = np.zeros((nxC,nyC))
frameCondicion = tkinter.Frame(root)
#automata palo
gameState[5,3]  =  1
gameState[5,4]  =  1
gameState[5,5]  =  1
#automata movil
gameState[21,21]  =  1
gameState[22,22]  =  1
gameState[22,23]  =  1
gameState[21,23]  =  1
gameState[20,23]  =  1

num_cels = 0
num_it =  0

labelLoadCondicion = tkinter.Label(frameCondicion,text = "Choose File .txt",font=("Times New Roman",14))
labelLoadCondicion.pack(side="left")
frameCondicion.grid(row=3,column=0)

#Control de la ejecución 
pauseExect  = False

#Bucle en ejecucion
while True:
    num_it = num_it + 1
    newGameState = np.copy(gameState)
    time_delta = clock.tick(60)/1000.0
    screen.fill(bg)
    time.sleep(0.2)

    #Registramos eventos de teclado y raton


    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Detectamos si se presiona alguna tecla
        elif event.type == pygame.KEYDOWN:
            #si se preciona la tecla de espacio  
            if event.key == pygame.K_ESCAPE:
                pauseExect = not pauseExect
                print("escx")
            elif event.key == pygame.K_SPACE:
                pauseExect = not pauseExect
                print("se gurada")
                with open('celulasIniciales.txt', 'wb') as f:
                    np.savetxt(f, np.column_stack(gameState), fmt='%1.10f')
            if  event.key == pygame.K_UP:
                print("upload")
                try:
                    filename = askopenfilename()
                    if (filename.find(".txt")!=-1):
                        labelLoadCondicion.config(text = filename)
                        newGameState = np.loadtxt(filename)
                        #pygame.display.update()
                    else:
                        gameState = []
                        labelLoadCondicion.config(text = "Choose a file .txt")
                except:
                        gameState = []
                        labelLoadCondicion.config(text = "File Error")
            if event.key == pygame.K_c:
                color = colorchooser.askcolor()[1]
            if event.key ==  pygame.K_g:
                plt.plot(num_cels)
                plt.ylabel('numero de celulas')
                plt.show()
                

        #Detectamos si se presiona el raton
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY =  int(np.floor(posX / dimCM)),int(np.floor(posY / dimCH))
            newGameState[celX,celY]  = not mouseClick[2]

        

        

    for y in range(0, nxC):
        for x in range(0,nyC):

            if not pauseExect:
                #Calculamos el numero de vecions cercanos 
                n_neigh  = gameState[(x - 1) % nxC ,(y - 1) % nyC ] + \
                        gameState[(x) % nxC ,(y - 1) % nyC ] + \
                        gameState[(x + 1) % nxC ,(y - 1) % nyC ] + \
                        gameState[(x - 1)  % nxC ,(y) % nyC ] + \
                        gameState[(x + 1) % nxC ,(y) % nyC ] + \
                        gameState[(x - 1) % nxC ,(y + 1) % nyC ] + \
                        gameState[(x) % nxC ,(y + 1) % nyC ] + \
                        gameState[(x + 1) % nxC ,(y + 1) % nyC ]

                #rule 1 : Una celula muerta con exactamente 3 vecinas viva, "revive"
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1
                    num_cels =  num_cels  + 1
                #rule 2: una viva con menos de dos o más de 3 vecinas vivas, "muere"
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] =  0
                    num_cels =  num_cels - 1
            
            #Creamos el poligono de cada celda a dibujar
            poly = [((x) * dimCM, y * dimCH),
                ((x+1) * dimCM, y * dimCH),
                ((x+1) * dimCM, (y+1) * dimCH),
                ((x) * dimCM, (y+1) * dimCH)]

            #Y dibujamos la celda para cada par de x e y
            if newGameState [x,y]  == 0:
                pygame.draw.polygon(screen,(128,  128, 128), poly, 1)
                
                
            else:
                pygame.draw.polygon(screen,(color), poly, 0)
    #Actualizamos el estado del juego
    print("el numero de celulas es:  " + repr(num_cels))
    print("el numero de iteraciones es:  "+  repr(num_it))
    gameState = np.copy(newGameState)
    #Actualizamos la pantalla       
    pygame.display.flip()