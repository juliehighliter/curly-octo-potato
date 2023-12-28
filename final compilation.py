import pygame
import sys
import random
import flappy as f
import jumpy as j
import Space_Invaders as si
import Snake_final as s
import breakout as b
import mysql.connector as m
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

            display_text('Back to Login', 'red', 310, 500)

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
                    return
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
                    selected_game='Tetris'
                    #play_game(selected_game,username)
                elif 80<x<255 and 490<y<530:
                    selected_game='Snake'
                    play_game(selected_game,username)
                elif 380<x<555 and 190<y<230:
                    selected_game='Breakout'
                    play_game(selected_game,username)
                elif 380<x<555 and 345<y<385:
                    selected_game='Space Invaders'
                    play_game(selected_game,username)
                elif 380<x<555 and 495<y<530:
                    selected_game='Jumpy'
                    play_game(selected_game,username)
                if 375<x<425 and 660<y<700:
                    login_screen()
                   
        screen.blit(bg_image2,(0,0))
        display_text('Choose a Game','white',190,100)

        draw_button(20,90,300,250,'Game_button/flappy_button.png')
        draw_button(20,240,300,250,'Game_button/tetris_button.png')
        draw_button(20,390,300,250,'Game_button/snake_button.png')
        draw_button(320,90,300,250,'Game_button/breakout_button.png')
        draw_button(320,240,300,250,'Game_button/space invaders_button.png')
        draw_button(320,390,300,250,'Game_button/jumpy_button.png')

        display_text('Log out','red',375,660)

        pygame.display.flip()
    
def play_game(selected_game,username):
    if selected_game=='Flappy Bird':
        f.flappy_bird(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Tetris':
        pass
    elif selected_game=='Snake':
        s.Snake(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Breakout':
        b.Breakout(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Space Invaders':
        si.space_invaders(username)
        screen=pygame.display.set_mode((width,height))
    elif selected_game=='Jumpy':
        j.jumpy(username)
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
        draw_button(280,120, 250, 200, 'sign_up_button.png')  # Sign-up button


        pygame.display.flip()

start_screen()
