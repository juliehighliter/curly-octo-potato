import pygame
import sys
import random
from pygame.math import Vector2
from pygame.locals import *
from pygame import mixer
import mysql.connector as m

def flappy_bird(user):
    pygame.mixer.pre_init(frequency= 44100, size =16, channels=1, buffer=512)
    pygame.init()
    import mysql.connector as m
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    cursor.execute('select max(flappy) from arcade')
    v=cursor.fetchone()[0]
    if v==None:v=0
    
    def draw_floor():
        screen.blit(floor_surface,(floor_x_pos,900))
        screen.blit(floor_surface,(floor_x_pos+576,900))
    def create_pipe():
        rand=random.choice(pipe_height)
        bottom_pipe=pipe_surface.get_rect(midtop=(700,rand))
        top_pipe=pipe_surface.get_rect(midbottom=(700,rand-400))
        return bottom_pipe,top_pipe
    
    def move_pipe(pipes):
        for pipe in pipes:
            pipe.centerx-=5
        return pipes
    
    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom>=1024:
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe=pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe,pipe)
                
    def check_collisions(pipes):
         for pipe in pipes:
             if bird_rect.colliderect(pipe):
                 death_sound.play()
                 return False
         if bird_rect.top<=-100 or bird_rect.bottom>=900:
             death_sound.play()
             return False
         return True
        
    def rotate_bird(bird):
        new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
        return new_bird
    
    def bird_animation():
        new_bird=bird_frames[bird_index]
        new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
        return new_bird, new_bird_rect
    
    def score_display(game_state):
        if game_state=='main game':
            score_surface=game_font.render(str(int(score)),True,(255,255,255))
            score_rect=score_surface.get_rect(center=(288,100))
            screen.blit(score_surface,score_rect)
        if game_state=='game over':
            score_surface=game_font.render('High Score: '+str(int(high_score)),True,(255,255,255))
            score_rect=score_surface.get_rect(center=(288,100))
            screen.blit(score_surface,score_rect)

            highscore_surface=game_font.render('Score: '+str(int(score)),True,(255,255,255))
            highscore_rect=score_surface.get_rect(center=(288,850))
            screen.blit(highscore_surface,highscore_rect)
            
    def update_score(score,high_score):
        if score>high_score:
            high_score=score
        return high_score
        
    screen=pygame.display.set_mode((576,1024))
    clock=pygame.time.Clock()
    game_font=pygame.font.Font('04B_19.ttf',40)

    gravity = 0.25
    bird_movement=0
    game_active=True
    score=0
    high_score=v

    bg_surface=pygame.image.load('assets/background-day.png').convert()
    bg_surface=pygame.transform.scale2x(bg_surface)

    floor_surface= pygame.image.load('assets/base.png').convert()
    floor_surface=pygame.transform.scale2x(floor_surface)
    floor_x_pos=0

    bird_downflap = pygame. transform.scale2x(pygame. image.load( 'assets/bluebird-downflap.png'). convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame. image.load( 'assets/bluebird-midflap.png').convert_alpha())
    bird_upflap = pygame. transform.scale2x(pygame. image.load( 'assets/bluebird-upflap.png'). convert_alpha())
    bird_frames = [bird_downflap,bird_midflap,bird_upflap]
    bird_index=0
    bird_surface=bird_frames[bird_index]
    bird_rect=bird_surface.get_rect(center=(100,512))

    BIRDFLAP=pygame.USEREVENT +1
    pygame.time.set_timer(BIRDFLAP,300)

    pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
    pipe_surface=pygame.transform.scale2x(pipe_surface)
    pipe_list=[]
    SPAWNPIPE=pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE,1200)
    pipe_height=[400,600,800]

    game_over_surface = pygame. transform. scale2x(pygame. image. load('assets/message.png').convert_alpha())
    game_over_rect = game_over_surface.get_rect (center = (288,512))

    flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
    death_sound = pygame.mixer.Sound ('sound/sfx_hit.wav')
    score_sound=pygame.mixer.Sound ('sound/sfx_point.wav')
    score_sound_countdown=100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score>high_score:
                    high_score=score
                    cursor.execute("update arcade set flappy=%s where user=%s",(high_score,user))
                    db.commit()
                db.close()
                return
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and game_active:
                    bird_movement=0
                    bird_movement-=12
                    flap_sound.play()
                if event.key==pygame.K_SPACE and game_active== False:
                    game_active=True
                    pipe_list.clear()
                    bird_rect.center=(100,512)
                    bird_movement=0 
            if event.type==SPAWNPIPE:
                pipe_list.extend(create_pipe())
            if event.type == BIRDFLAP:
                if bird_index<2:
                    bird_index+=1
                else:
                    bird_index=0
                bird_surface,bird_rect= bird_animation()
        screen.blit(bg_surface,(0,0))
        
        if game_active:
            
            #Bird
            bird_movement+=gravity
            rotated_bird=rotate_bird(bird_surface)
            bird_rect.centery+=bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active=check_collisions(pipe_list)
            
            #Pipe
            pipe_list=move_pipe(pipe_list)
            draw_pipes(pipe_list)

            score+=0.01
            score_display('main game')
            score_sound_countdown-=1
            if score_sound_countdown<=0:
                score_sound.play()
                score_sound_countdown=100

        else:
            screen.blit (game_over_surface,game_over_rect)
            high_score=update_score(score,high_score)
            score=0
            cursor.execute("update arcade set flappy=%s where user=%s",(high_score,user))
            db.commit()
            score_display('game over')
        
        floor_x_pos-=1
        draw_floor()
        if floor_x_pos<=-576:
            floor_x_pos=0
        
        pygame.display.update()
        clock.tick(50)

def jumpy(user):
    pygame.init()
    import mysql.connector as m
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    cursor.execute('select max(jumpy) from arcade')
    v=cursor.fetchone()[0]
    if v==None:v=0
    
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
    highscore=v
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
    fss=pygame.font.SysFont("Lucida Sans",15)
    
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
            text("HIGHSCORE: "+str(highscore),fss,WHITE,0,score-hs+250)
            
            #display score
            pygame.draw.rect(sc,BLUE,(0,0,400,30))
            pygame.draw.line(sc,WHITE,(0,30),(400,30),2)
            text("SCORE: "+str(scr),fs,WHITE,0,0)
            
            #game over check
            if jumpy.rect.top>600:
                g=True
        else:
            #game over
            if scr>=highscore:
                    highscore=scr
                    hs=highscore*10
                    cursor.execute("update arcade set jumpy=%s where user=%s",(highscore,user))
                    db.commit()
            pygame.draw.rect(sc,WHITE,(100,200,210,150))
            text("GAME OVER!",fs,BLACK,130,200)
            text("SCORE: "+str(scr),fs,BLACK,140,250)
            text("HIGHSCORE: "+str(highscore),fs,BLACK,110,300)
            text("PRESS SPACE TO PLAY AGAIN",fs,BLACK,35,450)
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
                if scr>=highscore:
                    highscore=scr
                    hs=highscore*10
                    cursor.execute("update arcade set jumpy=%s where user=%s",(highscore,user))
                    db.commit()
                db.close()
                return
        pygame.time.Clock().tick(80)
        pygame.display.update()


def Snake(user):
    import mysql.connector as m
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    cursor.execute('select max(snake) from arcade')
    v=cursor.fetchone()[0]
    if v==None:v=0
    class Snake:
        def __init__(self):
            self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
            self.direction=Vector2(0,0)
            self.new_block=False

            self.head_up=pygame.image.load('Graphics/head_up.png').convert_alpha()
            self.head_down=pygame.image.load('Graphics/head_down.png').convert_alpha()
            self.head_right=pygame.image.load('Graphics/head_right.png').convert_alpha()
            self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
            
            self.tail_up=pygame.image.load('Graphics/tail_up.png').convert_alpha()
            self.tail_down=pygame.image.load('Graphics/tail_down.png').convert_alpha()
            self.tail_right=pygame.image.load('Graphics/tail_right.png').convert_alpha()
            self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

            self.body_vertical=pygame.image.load('Graphics/body_vertical.png').convert_alpha()
            self.body_horizontal=pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

            self.body_tr=pygame.image.load('Graphics/body_tr.png').convert_alpha()
            self.body_tl=pygame.image.load('Graphics/body_tl.png').convert_alpha()
            self.body_br=pygame.image.load('Graphics/body_br.png').convert_alpha()
            self.body_bl=pygame.image.load('Graphics/body_bl.png').convert_alpha()
            self.crunch_sound=pygame.mixer.Sound('Sound/crunch.wav')

        def draw_snake(self):
            self.update_head_graphics()
            self.update_tail_graphics()
            
            for index,block in enumerate(self.body):
                x_pos=int(block.x*cell_size)
                y_pos=int(block.y*cell_size)
                block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

                if index==0:
                    screen.blit(self.head,block_rect)
                elif index==len(self.body)-1:
                    screen.blit(self.tail,block_rect)
                else:
                    previous_block=self.body[index+1]-block
                    next_block=self.body[index-1]-block
                    if previous_block.x==next_block.x:
                        screen.blit(self.body_vertical,block_rect)
                    elif previous_block.y==next_block.y:
                        screen.blit(self.body_horizontal,block_rect)
                    else:
                        if previous_block.x==-1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==-1:
                            screen.blit(self.body_tl,block_rect)
                        if previous_block.x==-1 and next_block.y==1 or previous_block.y==1 and next_block.x==-1:
                            screen.blit(self.body_bl,block_rect)
                        if previous_block.x==1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==1:
                            screen.blit(self.body_tr,block_rect)
                        if previous_block.x==1 and next_block.y==1 or previous_block.y==1 and next_block.x==1:
                            screen.blit(self.body_br,block_rect)              
                    
        def update_head_graphics(self):
            head_relation=self.body[1]-self.body[0]
            if head_relation==Vector2(1,0):
                self.head=self.head_left
            elif head_relation==Vector2(-1,0):
                self.head=self.head_right
            elif head_relation==Vector2(0,1):
                self.head=self.head_up
            elif head_relation==Vector2(0,-1):
                self.head=self.head_down

        def update_tail_graphics(self):
            tail_relation=self.body[-2]-self.body[-1]
            if tail_relation==Vector2(1,0):
                self.tail=self.tail_left
            elif tail_relation==Vector2(-1,0):
                self.tail=self.tail_right
            elif tail_relation==Vector2(0,1):
                self.tail=self.tail_up
            elif tail_relation==Vector2(0,-1):
                self.tail=self.tail_down
        def move_snake(self):
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]

        def add_block(self):
            self.new_block = True

        def play_crunch_sound(self):
            self.crunch_sound.play()

        def reset(self):
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
            self.direction = Vector2(0,0)

    class Fruit:
        def __init__(self):
            self.randomize()
            
        def draw_fruit(self):
            fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
            screen.blit(apple,fruit_rect)

        def randomize(self):
            self.x = random.randint(0,cell_number - 1)
            self.y = random.randint(0,cell_number - 1)
            self.pos = Vector2(self.x,self.y)

    class Main:
        def __init__(self):
            self.snake=Snake()
            self.fruit=Fruit()

        def update(self):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

        def draw_elements(self):
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
            self.draw_hscore()

        def check_collision(self):
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                self.snake.add_block()
                self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

        def check_fail(self):
            if not 0<=self.snake.body[0].x< cell_number or not 0<=self.snake.body[0].y<cell_number:
                self.game_over()
            for block in self.snake.body[1:]:
                if block==self.snake.body[0]:
                    self.game_over()
                    
        def game_over(self):
            nonlocal highscore
            score=len(self.snake.body)-3
            if score>=highscore:
                highscore=score
                cursor.execute("update arcade set snake=%s where user=%s",(highscore,user))
                db.commit()
            self.snake.reset()
            
        def draw_grass(self):
            grass_colour=(167,209,61)
            for row in range(cell_number):
                if row%2==0:
                    for col in range(cell_number):
                        if col%2==0:
                            grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_colour,grass_rect)
                else:
                    for col in range(cell_number):
                        if col%2!=0:
                            grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                            pygame.draw.rect(screen,grass_colour,grass_rect)            
            
        def draw_score(self):
            score_text=str(len(self.snake.body)-3)
            score_surface=game_font.render(score_text,True,(56,74,12))
            score_x=int(cell_size*cell_number-60)
            score_y=int(cell_size*cell_number-40)
            score_rect=score_surface.get_rect(center=(score_x,score_y))
            apple_rect=apple.get_rect(midright=(score_rect.left,score_rect.centery))
            bg_rect=pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

            pygame.draw.rect(screen,(167,209,61),bg_rect)
            screen.blit(apple,apple_rect)
            screen.blit(score_surface,score_rect)
            pygame.draw.rect(screen,(56,74,12),bg_rect,2)
            
        def draw_hscore(self):
            hscore_text="Highscore: " + str(highscore)
            hscore_surface=game_font.render(hscore_text,True,(56,74,12))
            hscore_rect=pygame.Rect(7,5,75,25)
            screen.blit(hscore_surface,hscore_rect)
            
    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()
    cell_size=40
    cell_number=20
    screen=pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
    clock=pygame.time.Clock()
    apple=pygame.image.load('Graphics/apple.png').convert_alpha()
    game_font=pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
    highscore=v

    screen_update=pygame.USEREVENT
    pygame.time.set_timer(screen_update,150)

    main_game=Main()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                score=len(main_game.snake.body)-3
                if score>highscore:
                    highscore=score
                    cursor.execute("update arcade set space=%s where user=%s",(highscore,user))
                    db.commit()
                db.close()
                return
            if event.type==screen_update:
                main_game.update()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    if main_game.snake.direction.y!=1:
                        main_game.snake.direction=Vector2(0,-1)
                if event.key==pygame.K_RIGHT:
                    if main_game.snake.direction.x!=-1:
                        main_game.snake.direction=Vector2(1,0)
                if event.key==pygame.K_DOWN:
                    if main_game.snake.direction.y!=-1:
                        main_game.snake.direction=Vector2(0,1)
                if event.key==pygame.K_LEFT:
                    if main_game.snake.direction.x!=1:
                        main_game.snake.direction=Vector2(-1,0)

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def space_invaders(user):
    import mysql.connector as m
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    cursor.execute('select max(space) from arcade')
    v=cursor.fetchone()[0]
    if v==None:v=0
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
    highscore=v

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
            nonlocal score
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
        nonlocal score
        for k in alien_group:
            k.kill()
        generate_aliens()
        countdown=3
        game_over=0
        score=0
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
                if score>highscore:
                    highscore=score
                    cursor.execute("update arcade set space=%s where user=%s",(highscore,user))
                    db.commit()
                draw_text('GAME OVER - Score: {}'.format(score), font40, white, int(screen_width/2-225),
                          int(screen_height/2+20))
                draw_text('Highscore: '+str(highscore), font30, white, int(screen_width/2-100), int(screen_height/2+80))
                draw_text('Press ENTER to play again', font30, white, int(screen_width / 2 - 200), int(screen_height/2+120))
                
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
                if score>highscore:
                    highscore=score
                    cursor.execute("update arcade set space=highscore where user==%s",(user,))
                db.close()
                return
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    restart_game()
                    
        pygame.display.update()

def Breakout(username):
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
                return
            
        #delay
        pygame.time.Clock().tick(60)
        pygame.display.update()
    game_selection_screen()

db=m.connect(host='localhost', user='root',passwd='vikas@19')
cursor=db.cursor()
cursor.execute('use game')
cursor.execute('create table if not exists arcade(user varchar(50) primary key,password varchar(50),space int,flappy int,jumpy int,breakout int,snake int)')
db.close()
pygame.init()

width=630
height=630
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Gamu Arcade')

bg_image1=pygame.image.load('main bg.png')
bg_image1=pygame.transform.scale(bg_image1, (630,630))

bg_image2=pygame.image.load('Untitled design.png')
bg_image2=pygame.transform.scale(bg_image2, (630,630))

black=(0,0,0)
white=(255,255,255)

font1=pygame.font.Font('arcade_ya/ARCADE_N.TTF',20)
font2=pygame.font.SysFont('Georgia',20)

selected_game=None
def userpassword():
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    d={}
    cursor.execute("select user,password from arcade")
    for k in cursor.fetchall():
        d[k[0]]=k[1]
    db.close()
    return d
def insertuser(user,password):
    db=m.connect(host='localhost',user='root',passwd='vikas@19')
    cursor=db.cursor()
    cursor.execute('use game')
    cursor.execute('insert into arcade(user,password) values(%s,%s)',(user,password))
    db.commit()
    db.close()
def login_screen():
    global selected_game
    username=''
    password=''
    input_active=None
    dict=userpassword()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 240<x<580 and 280<y<330:
                    input_active='username'
                elif 240<x<580 and 360<y<400:
                    input_active='password'
                elif 305<x<570 and 495<y<520: #log out
                    input_active=None
                    selected_game=None
                    return
                else:
                    input_active=None
            elif event.type==pygame.KEYDOWN:
                if input_active=='username':
                    if event.key==pygame.K_RETURN:
                        if username not in dict:
                            print('Invalid username')
                            username=''
                        else:
                            input_active='password'
                    elif event.key==pygame.K_BACKSPACE:
                        username=username[:-1]
                    else:
                        username+=event.unicode
                elif input_active=='password':
                    if event.key==pygame.K_RETURN:
                        try:
                            if password==dict[username]:#sql
                                print('Login Successful')
                                game_selection_screen(username)
                            else:
                                print('Incorrect password. Try again')
                                password=''
                        except KeyError:
                            print('Username does not exist')
                            username=''
                    elif event.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        password+=event.unicode
                        
            screen.blit(bg_image2,(0,0))

            display_text('Username:', 'white', 50, 295)
            display_text('Password:', 'white', 50, 375)

            pygame.draw.rect(screen, black, (240, 280, 340, 50))
            username_surface = font2.render(username, True, white)
            screen.blit(username_surface, (240, 290))

            # Render and draw the password text
            pygame.draw.rect(screen, black, (240, 360, 340, 50))
            password_surface = font2.render('*' * len(password), True, white)
            screen.blit(password_surface, (240, 375))

            display_text('Log out', 'red', 310, 500)

            pygame.display.flip()

def sign_up_screen():
    new_username=''
    new_password=''
    input_active=None
    dict=userpassword()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x, y=pygame.mouse.get_pos()
                if 350< x <500 and 430< y <460:
                    if new_username and new_password and new_username not in dict:
                        insertuser(new_username,new_password)                     
                        login_screen()
                elif 305<x<570 and 495<y<520:  # Back to login
                    input_active=None
                    start_screen()
                else:
                    input_active=None
                if 240<x<580 and 280<y<330:
                    input_active = 'new_username'
                elif 240<x<580 and 360<y<400 :
                    input_active = 'new_password'
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    pass
                elif event.key==pygame.K_BACKSPACE:
                    # Handle backspace key press
                    if input_active=='new_username':
                        new_username=new_username[:-1]
                    elif input_active=='new_password':
                        new_password=new_password[:-1]
                else:
                    # Handle other key presses
                    if input_active=='new_username':
                        new_username+=event.unicode
                    elif input_active=='new_password':
                        new_password+=event.unicode

        screen.blit(bg_image2, (0, 0))

        pygame.draw.rect(screen, black, (240, 280, 340, 50))
        new_username_surface = font2.render(new_username, True, white)
        screen.blit(new_username_surface, (240, 290))

        pygame.draw.rect(screen, black, (240, 360, 340, 50))
        new_password_surface = font2.render('*' * len(new_password), True, white)
        screen.blit(new_password_surface, (240, 370))

        display_text('Username:', 'white', 50, 295)
        display_text('Password:', 'white', 50, 375)

        draw_button(350, 370, 200, 150, 'sign_up_button.png')  # Sign-up button
        display_text('Back to Login', 'red', 310, 500)

        pygame.display.flip()

def game_selection_screen(username):
    global selected_game
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 80<x<250 and 190<y<230:
                    selected_game='Flappy Bird'
                    play_game(selected_game,username)
                elif 80<x<250 and 340<y<380:
                    selected_game='Jumpy'
                    play_game(selected_game,username)
                elif 215<x<390 and 270<y<315:
                    selected_game='Snake'
                    play_game(selected_game,username)
                elif 380<x<555 and 190<y<230:
                    selected_game='Breakout'
                    play_game(selected_game,username)
                elif 380<x<555 and 345<y<385:
                    selected_game='Space Invaders'
                    play_game(selected_game,username)
                if 230<x<370 and 430<y<470:
                    login_screen()
                   
        screen.blit(bg_image2,(0,0))
        display_text('Choose a Game','white',190,100)

        draw_button(20,90,300,250,'Game_button/flappy_button.png')
        draw_button(20,240,300,250,'Game_button/jumpy_button.png')
        draw_button(150,170,300,250,'Game_button/snake_button.png')
        draw_button(320,90,300,250,'Game_button/breakout_button.png')
        draw_button(320,240,300,250,'Game_button/space invaders_button.png')

        display_text('Log out','red',230,450)

        pygame.display.flip()
    
def play_game(selected_game,username):
    if selected_game=='Flappy Bird':
        flappy_bird(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Snake':
        Snake(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Breakout':
        Breakout(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Space Invaders':
        space_invaders(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Jumpy':
        jumpy(username)
        screen=pygame.display.set_mode((width,height))
        
def draw_button(x,y,width,height,image_path):
    button_image=pygame.image.load(image_path)
    button_image=pygame.transform.scale(button_image,(width,height))
    screen.blit(button_image,(x,y))

def display_text(text,colour,x,y):
    text_surface=font1.render(text,True,colour)
    screen.blit(text_surface,(x,y))

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 164<x<308 and 200<y<230:
                    login_screen()
                elif 333<x<480 and 200<y<235:
                    sign_up_screen()

        screen.blit(bg_image1,(0,0))
        display_text('Welcome to Gamu Arcade','white',120,179)
        draw_button(110,120,250,200,'login_button.png')
        draw_button(280,120, 250, 200, 'sign_up_button.png') # Sign-up button


        pygame.display.flip()

start_screen()
