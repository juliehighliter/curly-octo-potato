import pygame,random
pygame.init()
#screen
sc=pygame.display.set_mode((700,700))
pygame.display.set_caption("breakout")

#clr
bg=(230,220,180)
red=(250,80,80)
green=(80,250,80)
blue=(80,80,250)
paddle=(230,160,80)
fontclr=(80,80,140)
#variables
live=0
gameover=0
#fonts
font=pygame.font.SysFont("Lucida Sans",30)
#drawtext
def text(text,font,clr,x,y):
    img=font.render(text,True,fontclr)
    sc.blit(img,(x,y))
#wall dimensions
l1=[[1 for k in range(6)]for j in range(6)];l2=[[1 for k in range(6)] for j in range(6)];l3=[[1 for k in range(6)] for j in range(6)]
for k in range(6):
    for j in range(6):
        if k%2==0 and j not in (0,5):
            l2[k][j]=0
        if (k+j)%2:
            l3[k][j]=0
l=[l1,l2,l3]

class Wall():
    def __init__(self):
        self.offset=50
        self.width=100
        self.height=50
    def create(self):
        self.bricks=[]
        self.dim=l[random.randrange(3)]
        for k in range(6):
            row=[]
            for j in range(6):
                if self.dim[k][j]:
                    blockx=self.offset+j*self.width
                    blocky=k*self.height
                    rectx=pygame.Rect(blockx,blocky,self.width,self.height)
                    if k<2:
                        strength=3
                    elif k<4:
                        strength=2
                    else:
                        strength=1
                    row.append([rectx,strength])
                else:row.append([(0,0,0,0),1])
            self.bricks.append(row)
    def draw(self):
        for k in self.bricks:
            for j in k:
                if j[1]==3:
                    clr=red
                elif j[1]==2:
                    clr=blue
                else:
                    clr=green
                pygame.draw.rect(sc,clr,j[0])
                pygame.draw.rect(sc,bg,j[0],1)

class Paddle:
    def __init__(self):
        self.reset()
    def reset(self):
        self.width=140
        self.height=30
        self.x=280
        self.y=650
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.dir=0
        self.speed=10
    def move(self):
        k=pygame.key.get_pressed()
        if k[pygame.K_LEFT] and self.rect.left>0:
            self.dir=-1
            self.rect.x-=self.speed
        elif k[pygame.K_RIGHT] and self.rect.right<700:
            self.dir=1
            self.rect.x+=self.speed
    def draw(self):
        pygame.draw.rect(sc,paddle,self.rect)
        pygame.draw.rect(sc,(50,50,50),self.rect,1)
        
class Ball():
    def __init__(self,x,y):
        self.reset(x,y)
    def reset(self,x,y):
        self.rad=15
        self.x=x-self.rad
        self.y=y
        self.rect=pygame.Rect(self.x,self.y,self.rad*2,self.rad*2)
        self.speedx=4
        self.speedy=-4
        self.status=0 #-1 is losing, 1 is winning, 0 is playing
    def move(self):
        #collisions
        overlap=7
        if self.rect.left<0 or self.rect.right>700:
            self.speedx*=-1
        if self.rect.top<0:
            self.speedy*=-1
        #collision with wall
        wallcheck=1
        for k in range(len(wall.bricks)):
            for j in range(len(wall.bricks[k])):
                brick=wall.bricks[k][j]
                if self.rect.colliderect(brick[0]):
                    #top
                    if abs(self.rect.bottom-brick[0].top)<overlap and self.speedy>0:
                        self.speedy*=-1
                    #bottom
                    elif abs(self.rect.top-brick[0].bottom)<overlap and self.speedy<0:
                        self.speedy*=-1
                    #left
                    if abs(self.rect.right-brick[0].left)<overlap and self.speedx>0:
                        self.speedx*=-1
                    #right
                    elif abs(self.rect.left-brick[0].right)<overlap and self.speedx<0:
                        self.speedx*=-1
                    if brick[1]>1:brick[1]-=1
                    else:brick[0]=(0,0,0,0)
                if brick[0]!=(0,0,0,0):wallcheck=0
        #win condition
        if wallcheck==1:
            self.status=1
        #collisions w paddle
        if self.rect.colliderect(p):
            #top
            if abs(self.rect.bottom-p.rect.top)<overlap and self.speedy>0:
                self.speedy*=-1
                self.speedx+=p.dir
                if self.speedx>5:
                    self.speedx=5
                elif self.speedx<-5:
                    self.speedx=-5
                #corner
                if abs(self.rect.left-p.rect.right)<7 and self.speedx<0 or abs(self.rect.right-p.rect.left)<7 and self.speedx>0:
                    self.speedx*=-1
            #side
            else:
                self.speedx*=-1
        #life status
        if self.rect.bottom>700:
            self.status=-1
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        return self.status
    def draw(self):
        pygame.draw.circle(sc,(230,160,80),(self.rect.x+self.rad,self.rect.y+self.rad),self.rad)
        pygame.draw.circle(sc,(50,50,50),(self.rect.x+self.rad,self.rect.y+self.rad),self.rad,2)
wall=Wall()
wall.create()
p=Paddle()
b=Ball(p.x+(p.width//2),p.y-p.height)
run=1
while run:
    sc.fill(bg)
    #display
    wall.draw()
    b.draw()
    p.draw()
    if live:
        p.move()
        gameover=b.move()
        if gameover!=0:
            live=0

    #game status
    if not live:
        text("Press SPACE To Start",font,fontclr,200,450)
        if gameover==0:
            pass
        elif gameover==1:
            text("You Won!",font,fontclr,320,400)
        else:
            text("You Lost!",font,fontclr,300,400)
        k=pygame.key.get_pressed()
        if k[pygame.K_SPACE] :
            wall.create()
            b.reset(p.x+(p.width//2),p.y-p.height)
            p.reset()
            live=1
            gameover=0
    #close
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=0
    #delay
    pygame.time.Clock().tick(60)
    pygame.display.update()
pygame.quit()







