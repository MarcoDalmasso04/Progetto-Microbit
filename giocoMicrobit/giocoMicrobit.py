import queue
import secrets
import sys,time
from tkinter import Y
import pygame
import random
import threading
import serial
import keyboard

pygame.init()

width = 1000
high = 650 

size = (width, high)
screen = pygame.display.set_mode(size)

navicella = pygame.image.load("navicella.png")
navicella_rect = navicella.get_rect()
navicella_rect.centerx = width / 2
navicella_rect.centery = high - 50

sfondo = pygame.image.load("sfondo2.png")
sfondo_rect = sfondo.get_rect()

menu = pygame.image.load("menu.png")
menu_rect = menu.get_rect()

gameOver = pygame.image.load("gameOver.png")
gameOver_rect = gameOver.get_rect()

pygame.display.set_caption("FALL OF ASTEROIDS")

suonoMenu = pygame.mixer.Sound("menu.mp3")
suonoGioco = pygame.mixer.Sound("gioco.mp3")

RED = (255, 0, 0)
BLACK = (0, 0, 0)

lista,i = [],3

speed = 10
q = queue.Queue()


class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM12"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            try: 
                data = s.readline().decode() 
                #print(data)
                acc = [float(x) for x in data[1:-3].split(",")]
                q.put(acc)
            except:
                print("Ricevuti dati errati")

running = True

def movimentoRettangolo(ret,n, x1, y1):
    rect = pygame.draw.rect(screen, RED, (ret.x, (ret.y+n) , 10, 10))
    collisioni(x1, y1, rect.centerx, rect.centery)
    return rect

def collisioni(x1, y1, x2, y2):
    print(f"rettangolo {x2}, {y2}")
    print(f"navicella {x1}, {y1}")
    if y2 + 10 >= y1 and x2 >= x1 - 5 and x2 <= x1 + 5:
        print("colpitoooooooooooooo")
        screen.blit(gameOver, gameOver_rect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()

rm = Read_Microbit()
rm.start()

tasto = "x"
n = 1

while running:

    if tasto == "x":
        suonoMenu.play()
        while keyboard.is_pressed("x") == False:
            screen.blit(menu, menu_rect)
            pygame.display.flip()
        tasto = "y"
        suonoMenu.stop()

    screen.fill(BLACK)
    screen.blit(sfondo, sfondo_rect)

    if n == 1:
        suonoGioco.play()
        n = 0;
    
    acc = q.get()

    if(acc[0] > 0):
        navicella_rect = navicella_rect.move(+speed, 0)
        screen.blit(navicella, navicella_rect)
    elif(acc[0] < 0):
        navicella_rect = navicella_rect.move(-speed, 0)
        screen.blit(navicella, navicella_rect)
    
    q.task_done()
    
    #----------Per muovere il gioco con i tasti------------

    '''
    if keyboard.is_pressed("a"):
        navicella_rect = navicella_rect.move(-speed, 0)
        screen.blit(navicella, navicella_rect)
    elif keyboard.is_pressed("d"):
        navicella_rect = navicella_rect.move(+speed, 0)
        screen.blit(navicella, navicella_rect)
    else:
        navicella_rect = navicella_rect.move(0, 0)
        screen.blit(navicella, navicella_rect)
    '''
    #-------------------------------------------------------------------------

    #-----------------disegno gli ostacoli e li muovo-------------------------
    
    if (i == 3):
        lista1 = [(pygame.draw.rect(screen, RED, (random.randint(0, 980), 0 , 10, 10))) for _ in range(3)]
        for el in lista1:
            collisioni(navicella_rect.centerx, navicella_rect.centery, el.centerx, el.centery)
            lista.append(el)
        i = 0
    i += 1
    for k,el in enumerate(lista):
        lista[k] = movimentoRettangolo(el, 25, navicella_rect.centerx, navicella_rect.centery)

    #---------------------------------------------------------------------------------
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
    time.sleep(0.5)

rm.terminate()
rm.join()