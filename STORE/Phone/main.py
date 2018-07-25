#lib import
print(-1)
import sys
sys.path.append('..\\..\\')
import derpapi
import pygame, os
from easygui import exceptionbox as eb

RUN = False

#screen init
print(0)
pygame.init()
print(1)
screen = pygame.display.set_mode([480, 320], pygame.NOFRAME)
print(1.1)
try:
    try:
        font = pygame.font.Font('..\\..\\font_main.otf', 32)
    except:
        font = pygame.font.Font('font_main.otf', 32)
except:
    pass
print(2)
def b_render(darken=None, dial=''):
    global screen, font
    screen.fill((230,230,230))
    buttons = []
    bpos = [(170, 250), (30, 100), (170, 100), (310, 100), (30, 150), (170, 150), (310, 150), (30, 200), (170, 200), (310, 200)]
    for i in range(10):
        try:
            surf = pygame.Surface((140, 50))
            if i == darken:
                surf.fill([150,150,150])
            else:
                surf.fill([200,200,200])
            surf.blit(font.render(str(i), True, (0,0,0)), (60, 10))
            screen.blit(surf, bpos[i])
            buttons.append(bpos[i])
        except:
            print(i)
    if dial != None:
        screen.blit(font.render(dial, True, (0,0,0)), (10, 10))
    pygame.display.flip()
    return buttons
print(3)
def main():
#place main code here
    global screen, font, b_render, pygame, derpapi, RUN
    RUN = True
    screen.fill((230,230,230))
    buttons = b_render()
    number = ''
    print(4)
    while RUN:
        try:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    collided = False
                    selected = None
                    for i in buttons:
                        if derpapi.collision(i, (140, 50), event.pos):
                            collided = True
                            selected = buttons.index(i)
                            b_render(darken=selected, dial=number)
                    if not collided:
                        b_render(dial=number)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if selected != None:
                        number += str(selected)
                        if len(number) == 3 or len(number) == 7:
                            number += ' '
                        b_render(darken=selected, dial=number)
        except:
            pass
        if len(number) == 12:
            RUN = False
    final_num = ''.join(number.split(' '))
    print('Dialing ' + final_num)
    derpapi.call(final_num)
    hang = pygame.image.load('hangup.png')
    screen.fill((230,230,230))
    screen.blit(hang, (0, 0))
    pygame.display.flip()
    RUN = True
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if derpapi.collision((90, 10), (480, 320), event.pos):
                    RUN = False
        uart_rec = derpapi.rx()
        try:
            if uart_rec[len(uart_rec) - 1] == 'NO CARRIER':
                RUN = False
        except:
            pass
    derpapi.hangup()
    print('hung up')
main()
pygame.quit()

