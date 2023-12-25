import pygame,random
pygame.init()
#game screen
W=400;H=600
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('jumpy')

#variables
scroll=0
bgscroll=0
g=False
score=0
scr=0
highscore=int(input("Enter high score:"))
hs=highscore*10
#image
bg=pygame.image.load('bg.png')
ch=pygame.image.load('jump.png')
wood=pygame.image.load('wood.png')

#clr
WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(153,217,234)
#background scrolling
def bgupdate(bgscroll):
    sc.blit(bg,(0,0+bgscroll))
    sc.blit(bg,(0,bgscroll-600))
#font
fs=pygame.font.SysFont("Lucida Sans",24)
fb=pygame.font.SysFont("Lucida Sans",30)
#text
def text(text,font,clr,x,y):
    t=font.render(text,True,clr)
    sc.blit(t,(x,y))

#character class
class Char():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(ch,(40,40))
        self.height=40
        self.width=25
        self.rect=pygame.Rect(x,y,self.width,self.height)
        self.flip=False
        self.vel=0
    def draw(self,sc):
        sc.blit(pygame.transform.flip(self.image,self.flip,False),(self.rect.x-10,self.rect.y-5))
    def move(self):
        dx=0;dy=0#movement
        scroll=0#initialize
        k=pygame.key.get_pressed()
        if k[pygame.K_LEFT]:
            dx=-10
            self.flip=True
        if k[pygame.K_RIGHT]:
            dx=10
            self.flip=False
        #gravity
        self.vel+=1   
        dy+=self.vel

        #platform check
        for p in platformgrp:
            if p.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                if self.rect.bottom<p.rect.bottom:
                    if self.vel>0:
                        self.rect.bottom=p.rect.top
                        self.vel=-20
                        dy=0
        #border check
        if self.rect.left+dx<0:
            dx=0-self.rect.left
        elif self.rect.right+dx>400:
            dx=400-self.rect.right

        #scrolling
        if self.rect.top<=250:
            if self.vel<0:
                scroll=-dy
                dy=0
        
        self.rect.x+=dx
        self.rect.y+=dy
        return scroll

#platforms
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width,moving):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(wood,(width,10))
        self.rect=self.image.get_rect()
        self.rect.x=x;self.rect.y=y
        self.moving=moving
        self.dir=random.choice([1,-1])
        self.speed=random.randint(1,2)
    def update(self,scroll):
        self.rect.y+=scroll
        dx=0
        #moving
        if self.moving:
            dx=self.dir*self.speed
            if self.rect.left+dx<0 or self.rect.right>400:
                self.dir*=-1
                dx*=-1
        self.rect.x+=dx
                
            
        #out of screen will delete sprite
        if self.rect.top>600:
            self.kill()
            

#sprite group
platformgrp=pygame.sprite.Group()
p=Platform(150,580,100,False)
platformgrp.add(p)
#jumpy character
jumpy=Char(200,450)

#game loop
run=1
while run:
    if not g:
        scroll=jumpy.move()   #gives scroll for platforms
        bgscroll+=scroll  #updating bg with scroll
        score+=(scroll)
        scr=score//10
        if bgscroll>=600:
            bgscroll=0
        bgupdate(bgscroll)    
        
        if len(platformgrp)<=20: #infinite platform
            pw=random.randrange(40,60)
            py=p.rect.y-random.randint(80,100)
            px=random.randint(0,400-pw)
            pt=random.randint(1,2)
            if scr>10 and pt==1:
                pm=True
            else:pm=False
            p=Platform(px,py,pw,pm)
            platformgrp.add(p)
                    
        platformgrp.update(scroll)  #updating platform scroll
        platformgrp.draw(sc)
        jumpy.draw(sc)
        #highscore line
        pygame.draw.line(sc,WHITE,(0,score-hs+250),(400,score-hs+250))

        #display score
        pygame.draw.rect(sc,BLUE,(0,0,400,30))
        pygame.draw.line(sc,WHITE,(0,30),(400,30),2)
        text("SCORE: "+str(scr),fs,WHITE,0,0)
        #game over check
        if jumpy.rect.top>600:
            g=True
    else:
        #game over
        pygame.draw.rect(sc,WHITE,(30,200,350,150))
        text("GAME OVER!",fs,BLACK,130,200)
        text("SCORE: "+str(scr),fs,BLACK,130,250)
        text("PRESS SPACE TO PLAY AGAIN",fs,BLACK,35,300)
        k=pygame.key.get_pressed()
        if k[pygame.K_SPACE]:
            g=False
            score=0
            scroll=0
            bgscroll=0
            jumpy.rect.center=(200,450)
            platformgrp.empty()
            p=Platform(150,580,100,False)
            platformgrp.add(p)
    #event
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=0



    pygame.time.Clock().tick(80)
    pygame.display.update()

pygame.quit()




















