#lib import
import sys, os
sys.path.append('..\\..\\')
import derpapi
import pygame

RUN = False
y = 30
c = 0
optpos = {}
optkeys = []
set_stor = [{'name':'Airplane Mode', 'type':'switch', 'default':False}, {'name':'WiFi','type':'custom','default':None}]

#screen init
try:
   pygame.init()
except:
   pygame.display.init()
screen = pygame.display.set_mode([480, 320], pygame.NOFRAME)
try:
   font = pygame.font.Font('..\\..\\font_main.otf', 32)
except:
   font = pygame.font.Font('font_main.otf', 32)
#load option sprites
sprites = {}
for i in os.listdir('optionsprites'):
   for n in os.listdir('optionsprites\\' + i):
      sprites[i + '.' + n.split('.')[0]] = pygame.image.load('optionsprites\\' + i + '\\' + n)
print(sprites)

def cusfunc(cname):
   if cname == 'WiFi':
      print('NO CONNECTION SRY SCRUB')

def render(opt, custom=False):
   global screen, sprites, y, optpos, set_stor, c, font, optkeys
   screen.blit(sprites[opt], (10,y))
   if custom:
      screen.blit(font.render(set_stor[c]['name'], True, (0,0,0)), (25, y + 5))
   else:
      screen.blit(font.render(set_stor[c]['name'], True, (0,0,0)), (sprites[opt].get_width() + 15, y + 5))
   optpos[sprites[opt]] = ((10, y), sprites[opt].get_size())
   optkeys.append(sprites[opt])
   
def main():
   global RUN, derpapi, cusfunc, screen, render, y, optpos, set_stor, c, font, optkeys
   #place main code here
   EXIT = pygame.image.load('exit.png')
   
   settings = derpapi.retrieve()
   for i in set_stor:
      if not i['name'] in settings.keys():
         settings[i['name']] = i['default']

   
   RUN = True
   while RUN:
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONDOWN:
            if derpapi.collision((430, 0), (50, 50), event.pos):
               RUN = False
            else:
               cc = 0
               for i in optkeys:
                  if derpapi.collision(optpos[i][0], optpos[i][1], event.pos):
                     if set_stor[cc]['type'] == 'switch':
                        if settings[set_stor[cc]['name']] == True:
                           settings[set_stor[cc]['name']] = False
                        else:
                           settings[set_stor[cc]['name']] = True
                     elif set_stor[cc]['type'] == 'custom':
                        cusfunc(set_stor[cc]['name'])
                  cc += 1
      screen.fill((230,230,230))
      screen.blit(font.render('SETTINGS', True, (0,0,0)), (10,10))
      screen.blit(EXIT, (430, 0))
      y = 45
      optpos = {}
      optkeys = []
      c = 0
      for i in set_stor:
         if i['type'] == 'switch':
            if settings[i['name']] == True:
               render('switch.on')
            else:
               render('switch.off')
         elif i['type'] == 'custom':
            render('custom.custom', custom=True)
         y += 42
         c += 1
      pygame.display.flip()
   derpapi.store(data=settings)

main()
pygame.display.quit()
