#lib import
import sys, os, time, random
sys.path.append('..\\..\\')
import derpapi
import pygame

RUN = False

#screen init
try:
   pygame.init()
except:
   pygame.display.init()

def set_transparent(surf, color=[255,255,255], alpha=0):
   _ccol = list(color)
   _ccol.append(255)
   _col = tuple(_ccol)
   nsurf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
   nsurf.blit(surf, (0,0))
   for x in range(nsurf.get_width()):
      for y in range(nsurf.get_height()):
         curcol = nsurf.get_at((x,y))
         #print(curcol)
         if curcol == _col:
            nsurf.set_at((x,y), (0,0,0,alpha))
   return nsurf

def main():
   global RUN, random, time, os, sys, set_transparent
   #place main code here
   screen = pygame.display.set_mode([480, 320], pygame.NOFRAME | pygame.SRCALPHA)

   try:
      font = pygame.font.Font('..\\..\\font_main.otf', 32)
   except:
      font = pygame.font.Font('font_main.otf', 32)

   dinos = {}
   for i in os.listdir('sprites\\dinos'):
      dinos[i.split('.')[0]] = set_transparent(pygame.transform.scale(pygame.image.load('sprites\\dinos\\' + i), (50, 50)), (230,230,230))

   cacti = []
   for i in os.listdir('sprites\\cacti'):
      cacti.append(set_transparent(pygame.transform.scale(pygame.image.load('sprites\\cacti\\' + i), (25, 40)), (230,230,230)))

   active_cacti = []
   pygame.mouse.set_visible(False)
   RUN = True
   ypos = 250
   jumping = False
   just_jumped = False
   ydel = -2.5
   SPD = 1
   score = 0
   tbc = round(time.time()) + random.randint(2, 4)
   sc = False
   END = False

   HS = derpapi.retrieve('HISCORE')
   if HS == None:
      HS = 0
   
   while RUN:
      pygame.time.Clock().tick(100)
      for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
            if event.unicode == ' ' and ypos >= 248:
               jumping = True
               just_jumped = False
               ydel = -2.5
      if jumping:
         ypos = ydel + ypos
         ydel += 0.04
         #print(ypos)
      if ypos >= 249 and jumping:
         jumping = False
         just_jumped = True
         ydel = -2.5
      if round(time.time()) % 2 == 0:
         just_jumped = False

      if round(time.time()) == tbc:
         tbc = round(time.time()) + random.randint(2, 4)
         if random.randint(0,2) == 2 and SPD >= 3:
            cpos = 480
            for i in range(random.randint(1, 3)):
               active_cacti.append({'pos':cpos, 'type':random.choice(cacti)})
               cpos += random.randint(15, 30)
         else:
            active_cacti.append({'pos':480, 'type':random.choice(cacti)})
      screen.fill((230,230,230))
      c_c = 0
      to_rem = []
      for cactus in active_cacti:
         cactus['pos'] -= SPD
         if cactus['pos'] >= 30 and cactus['pos'] <= 60 and ypos >= 230:
            END = True
         if cactus['pos'] >= 30 and cactus['pos'] <= 40 and ypos >= 210:
            END = True
         if cactus['pos'] <= 2:
            to_rem.append(c_c)
         else:
            screen.blit(cactus['type'], (cactus['pos'], 260))
         c_c += 1
      for rem in to_rem:
         del active_cacti[rem]
      if END:
         screen.blit(dinos['hurt'], (30, ypos))
         RUN = False
      else:
         if not jumping:
            if not just_jumped:
               if round(time.time(), 1) % 0.5 == 0:
                  screen.blit(dinos['walk_1'], (30, ypos))
               else:
                  screen.blit(dinos['walk_2'], (30, ypos))
            else:
               if round(time.time(), 1) % 0.5 == 0:
                  screen.blit(dinos['walk_1_j'], (30, ypos))
               else:
                  screen.blit(dinos['walk_2_j'], (30, ypos))
         else:
            screen.blit(dinos['jump_1'], (30, ypos))
      if round(time.time(), 1) % 0.5 == 0:
         if not sc:
            score += 1
            sc = True
      else:
         sc = False

      SPD = int(score / 100) + 1

      if score > int(HS):
         HS = score
   
      screen.blit(font.render(str(score), True, (0,0,0)), (10,10))
      screen.blit(font.render('HI: ' + str(HS), True, (0,0,0)), (10,40))
      ground = pygame.Surface((480, 4))
      ground.fill((83,83,83))
      bground = pygame.Surface((480, 16))
      bground.fill((150,150,150))
      screen.blit(ground, (0, 300))
      screen.blit(bground, (0, 304))
      pygame.display.flip()

   derpapi.store('HISCORE', HS)
   time.sleep(2)
   screen.fill((230,230,230))
   screen.blit(dinos['hurt'], (30, ypos))
   for cactus in active_cacti:
      screen.blit(cactus['type'], (cactus['pos'], 260))
   ground = pygame.Surface((480, 4))
   ground.fill((83,83,83))
   bground = pygame.Surface((480, 16))
   bground.fill((150,150,150))
   screen.blit(ground, (0, 300))
   screen.blit(bground, (0, 304))
   mask = pygame.Surface((480,320), flags=pygame.SRCALPHA)
   mask.fill((230,230,230, 200))
   screen.blit(mask, (0,0))
   screen.blit(font.render('SCORE: ', True, (0,0,0)), (10,10))
   screen.blit(font.render(str(score), True, (0,0,0)), (10,40))
   screen.blit(font.render('HIGHSCORE: ', True, (0,0,0)), (10,70))
   screen.blit(font.render(str(HS), True, (0,0,0)), (10,100))
   pygame.display.flip()
   time.sleep(5)

main()
pygame.display.quit()
