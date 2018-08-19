#lib import
import sys, os, random, time
sys.path.append('..\\..\\')
import derpapi
import pygame

RUN = False

#screen init
try:
   pygame.init()
except:
   pygame.display.init()

def main():
   global RUN, random, derpapi
   #place main code here
   HS = derpapi.retrieve('HISCORE')
   if HS == None:
      HS = 0
   screen = pygame.display.set_mode([480, 320], pygame.NOFRAME)
   screen.fill((230,230,230))
   try:
      font = pygame.font.Font('..\\..\\font_main.otf', 32)
   except:
      font = pygame.font.Font('font_main.otf', 32)
   RUN = True
   spd = 0.3
   paddle_x = 0
   cp = [240, 160]
   cpd = [random.choice([-1 * spd, spd]), random.choice([-1 * spd, spd])]
   lt = 0
   lst = 0
   s_mult = 1
   score = 0
   lives = 5
   lost_one = False

   pause = pygame.image.load('pause.png')
   paused = 1
   
   while RUN:
      pygame.time.Clock().tick(300)
      for event in pygame.event.get():
         if event.type == pygame.MOUSEMOTION and paused % 2 == 1:
            if event.pos[0] <= 20:
               paddle_x = 0
            elif event.pos[0] >= 460:
               paddle_x = 440
            else:
               paddle_x = event.pos[0] - 20
         if event.type == pygame.KEYDOWN:
            if event.unicode == 'x':
               pygame.display.quit()
               sys.exit()
            if event.unicode == 'p':
               paused += 1
         if event.type == pygame.MOUSEBUTTONDOWN:
            if derpapi.collision((215, 10), (50, 50), event.pos):
               paused += 1
      if paused % 2 == 0:
         screen.fill((200,200,200))
         screen.blit(pygame.Surface((40, 10)), (paddle_x, 300))
         screen.blit(pause, (215, 10))
         pygame.draw.circle(screen, (0,0,0), (int(cp[0]), int(cp[1])), 5)
         screen.blit(font.render(str(score), True, (0,0,0)), (10, 10))
         screen.blit(font.render('HI ' + str(HS), True, (0,0,0)), (10, 40))
         screen.blit(font.render(str(lives), True, (0,0,0)), (450, 10))
         pygame.display.flip()
      else:
         screen.fill((230,230,230))
         screen.blit(pygame.Surface((40, 10)), (paddle_x, 300))
         screen.blit(pause, (215, 10))
         pygame.draw.circle(screen, (0,0,0), (int(cp[0]), int(cp[1])), 5)
         screen.blit(font.render(str(score), True, (0,0,0)), (10, 10))
         screen.blit(font.render('HI ' + str(HS), True, (0,0,0)), (10, 40))
         screen.blit(font.render(str(lives), True, (0,0,0)), (450, 10))
         pygame.display.flip()
         cp = [cp[0] + cpd[0], cp[1] + cpd[1]]
         if cp[0] <= 5 or cp[0] >= 475:
            cpd[0] = cpd[0] * -1
         if cp[1] <= 5 or cp[1] >= 315:
            cpd[1] = cpd[1] * -1
         if derpapi.collision((paddle_x, 300), (40, 10), (cp[0], cp[1] + 5)) and round(time.time()) != lst:
            cpd[1] = cpd[1] * -1
            score += s_mult
            lst = round(time.time())

         if round(time.time()) % 30 == 0 and round(time.time()) != lt:
            lt = round(time.time())
            cpd = [cpd[0] * 1.1, cpd[1] * 1.1]
            s_mult += 1
            print('SPD' + str(cpd[0] * 1.1))

         if cp[1] >= 310 and not lost_one:
            lost_one = True
            lives -= 1
         elif cp[1] < 280:
            lost_one = False

         if lives == 0:
            RUN = False

         if score > int(HS):
            HS = score
      
   screen.fill((230,230,230))
   screen.blit(font.render('GAME OVER', True, (0,0,0)), (10, 10))
   screen.blit(font.render('Your score is ' + str(score), True, (0,0,0)), (10, 60))
   if HS == score:
      screen.blit(font.render('NEW HIGHSCORE', True, (0,0,0)), (10, 100))
      derpapi.store("HISCORE", HS)
   else:
      screen.blit(font.render('HI ' + HS, True, (0,0,0)), (10, 100))
   pygame.display.flip()
   time.sleep(4)
            

main()
pygame.display.quit()
