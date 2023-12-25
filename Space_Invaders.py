import pygame
from pygame.locals import *
import random
from pygame import mixer
def space_invaders():
    pygame.mixer.pre_init(44100,-16,2,512)

    pygame.init()

    clock=pygame.time.Clock()
    fps=60

    screen_width=600
    screen_height=800

    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption('Space Invaders')

    #define game variables

    rows=5
    cols=5
    alien_cooldown=1000
    last_alien_shot=pygame.time.get_ticks()
    countdown=3
    last_count=pygame.time.get_ticks()
    game_over=0
    score=0

    #define fonts
    font30=pygame.font.SysFont('Cooper Black',30)
    font40=pygame.font.SysFont('Cooper Black',40)

    #define function for creating text
    def draw_text(text,font,text_col,x,y):
        img=font.render(text,True, text_col)
        screen.blit(img,(x,y))

    #load sounds
    explosion_fx=pygame.mixer.Sound('img/explosion.wav')
    explosion_fx.set_volume(0.25)

    explosion2_fx=pygame.mixer.Sound('img/explosion.wav')
    explosion2_fx.set_volume(0.25)

    laser_fx=pygame.mixer.Sound('img/laser.wav')
    laser_fx.set_volume(0.25)

    #define colours
    red=(255,0,0)
    green=(0,255,0)
    white=(255,255,255)

    #load image

    bg=pygame.image.load('img/bg.png')

    def draw_bg():
        screen.blit(bg,(0,0))

    #create spaceship class
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self,x,y,health):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('img/spaceship.png')
            self.rect=self.image.get_rect()
            self.rect.center=[x,y]
            self.health_start=health
            self.health_remaining=health
            self.last_shot=pygame.time.get_ticks()

        def update(self):
            speed=8
            cooldown=500
            game_over=0

            #get key press
            key=pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left>0:
                self.rect.x-=speed
            if key[pygame.K_RIGHT] and self.rect.right<600:
                self.rect.x+=speed

            #record time
            time_now=pygame.time.get_ticks()

            #shoot
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                laser_fx.play()
                bullet=Bullets(self.rect.centerx,self.rect.top)
                bullet_group.add(bullet)
                self.last_shot=time_now
                
            #update mask
            self.mask=pygame.mask.from_surface(self.image)
                
            #draw health bar
            pygame.draw.rect(screen,red,(self.rect.x,(self.rect.bottom+10),self.rect.width,15))
            if self.health_remaining>0:
                pygame.draw.rect(screen,green,(self.rect.x,(self.rect.bottom+10),int(self.rect.width*(self.health_remaining/self.health_start)),15))
            elif self.health_remaining<=0:
                explosion=Explosion(self.rect.centerx,self.rect.centery,3)
                self.kill()
                game_over=-1
            return game_over
        
    #create bullet class
    class Bullets(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('img/bullet.png')
            self.rect=self.image.get_rect()
            self.rect.center=[x,y]

        def update(self):
            global score
            self.rect.y-=5
            if self.rect.bottom<0:
                self.kill()
            if pygame.sprite.spritecollide(self,alien_group,True):
                self.kill()
                explosion_fx.play()
                explosion=Explosion(self.rect.centerx,self.rect.centery,2)
                explosion_group.add(explosion)
                score+=10
                

    #create aliens class
    class Aliens(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('img/alien'+str(random.randint(1,5))+'.png')
            self.rect=self.image.get_rect()
            self.rect.center=[x,y]
            self.move_counter=0
            self.move_direction=1

        def update(self):
            self.rect.x+=self.move_direction
            self.move_counter+=1
            if abs(self.move_counter)>75:
                self.move_direction*=-1
                self.move_counter*=self.move_direction

    #create alien bullets class
    class Alien_Bullets(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('img/alien_bullet.png')
            self.rect=self.image.get_rect()
            self.rect.center=[x,y]
        def update (self):
            self.rect.y+=2
            if self.rect.top>screen_height:
                self.kill()
            if pygame.sprite.spritecollide(self,spaceship_group,False,pygame.sprite.collide_mask):
                self.kill()
                explosion2_fx.play()
                spaceship.health_remaining-=1
                explosion=Explosion(self.rect.centerx,self.rect.centery,1)
                explosion_group.add(explosion)

    #create explosion class          
    class Explosion(pygame.sprite.Sprite):
        def __init__(self,x,y,size):
            pygame.sprite.Sprite.__init__(self)
            self.images=[]
            for num in range(1,6):
                img=pygame.image.load('img/exp{}.png'.format(num))
                if size==1:
                    img=pygame.transform.scale(img,(20,20))
                if size==2:
                    img=pygame.transform.scale(img,(40,40))
                if size==3:
                    img=pygame.transform.scale(img,(160,160))
                self.images.append(img)
            self.index=0 
            self.image=self.images[self.index]
            self.rect=self.image.get_rect()
            self.rect.center=[x,y]
            self.counter=0

        def update(self):
            explosion_speed=3
            self.counter+=1
            if self.counter>=explosion_speed and self.index<len(self.images)-1:
                self.counter=0
                self.index+=1
                self.image=self.images[self.index]

            if self.index>=len(self.images)-1 and self.counter>=explosion_speed:
                self.kill()
            
    #create sprite groups
    spaceship_group=pygame.sprite.Group()
    bullet_group=pygame.sprite.Group()
    alien_group=pygame.sprite.Group()
    alien_bullet_group=pygame.sprite.Group()
    explosion_group=pygame.sprite.Group()

    def generate_aliens():
        for row in range(rows):
            for item in range(cols):
                alien=Aliens(100+item*100,100+row*70)
                alien_group.add(alien)

    generate_aliens()

    def restart_game():
        #defining restart conditions
        nonlocal countdown
        nonlocal game_over
        for k in alien_group:
            k.kill()
        generate_aliens()
        countdown=3
        game_over=0
        spaceship.health_remaining=3

    #create player
    spaceship=Spaceship(int(screen_width/2),screen_height-100,3)
    spaceship_group.add(spaceship)
    run=True

    while run:

        clock.tick(fps)
        
        #draw background
        draw_bg()

        if countdown==0:
            #create random alien bullets
            #record current time
            time_now=pygame.time.get_ticks()
            #shoot
            if time_now-last_alien_shot>alien_cooldown and len(alien_bullet_group)<5 and len(alien_group)>0:
                attacking_alien=random.choice(alien_group.sprites())
                alien_bullet=Alien_Bullets(attacking_alien.rect.centerx,attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shot=time_now

            if len(alien_group)==0:
                game_over=1

            if game_over==0:
                spaceship.update()
                
                #update sprite groups
                bullet_group.update()
                alien_group.update()
                alien_bullet_group.update()

            if len(alien_group)==0:
                game_over=1
            elif spaceship.health_remaining<=0:
                game_over=-1

            if game_over!=0:
                draw_text('GAME OVER - Score: {}'.format(score), font40, white, int(screen_width/2-200),
                          int(screen_height/2+20))
                draw_text('Do you want to play again?', font30, white, int(screen_width/2-200), int(screen_height/2+80))
                draw_text('Press Y for Yes or N for No', font30, white, int(screen_width / 2 - 200), int(screen_height/2+120))
                
        #update explosion_group
        explosion_group.update()

        draw_text('Score: {}'.format(score), font30, white, 10, 10)

        #draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        if countdown>0:
            draw_text('GET READY!',font40,white,int(screen_width/2-110),int(screen_height/2))
            draw_text(str(countdown),font40,white,int(screen_width/2),int(screen_height/2+50))
            count_timer=pygame.time.get_ticks()
            if count_timer-last_count>1000:
                countdown-=1
                last_count=count_timer
        #event handlers
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_y:
                    restart_game()
                elif event.key==pygame.K_n:
                    run=False   
        pygame.display.update()


    pygame.quit()

