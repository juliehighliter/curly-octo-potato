import pygame
import sys
import random
import flappy as f
import jumpy as j
import Space_Invaders as si
import Snake_final as s
import breakout as b

pygame.init()

width=900
height=900
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Gamu Arcade')

bg_image1=pygame.image.load('main bg.png')
bg_image1=pygame.transform.scale(bg_image1, (900,900))

bg_image2=pygame.image.load('Untitled design.png')
bg_image2=pygame.transform.scale(bg_image2, (900,900))

black=(0,0,0)
white=(255,255,255)

font1=pygame.font.Font('arcade_ya/ARCADE_N.TTF',20)
font2=pygame.font.SysFont('Georgia',20)

selected_game=None

def login_screen():
    global selected_game
    username=''
    password=''
    input_active=None

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 280<x<620 and 280<y<330:
                    input_active='username'
                elif 280<x<620 and 360<y<400:
                    input_active='password'
                elif 525<x<825 and 810<y<855: #log out
                    input_active=None
                    selected_game=None
                    return
                else:
                    input_active=None
            elif event.type==pygame.KEYDOWN:
                if input_active=='username':
                    if event.key==pygame.K_RETURN:
                            input_active='password'
                    elif event.key==pygame.K_BACKSPACE:
                        username=username[:-1]
                    else:
                        username+=event.unicode
                elif input_active=='password':
                    if event.key==pygame.K_RETURN:
                        if password=='pass':#sql
                            print('Login Successful')
                            game_selection_screen()
                        else:
                            print('Incorrect password. Try again')
                            password=''
                    elif event.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        password+=event.unicode
                        
            screen.blit(bg_image2,(0,0))

            display_text('Username:', 'white', 90, 295)
            display_text('Password:', 'white', 90, 375)

            pygame.draw.rect(screen, black, (280, 280, 340, 50))
            username_surface = font2.render(username, True, white)
            screen.blit(username_surface, (280, 290))

            # Render and draw the password text
            pygame.draw.rect(screen, black, (280, 360, 340, 50))
            password_surface = font2.render('*' * len(password), True, white)
            screen.blit(password_surface, (280, 375))

            pygame.display.flip()

def sign_up_screen():
    new_username=''
    new_password=''
    input_active=None

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x, y=pygame.mouse.get_pos()
                if 350< x <500 and 450< y <500:
                    if new_username and new_password: 
                        #sql
                        login_screen()
                elif 700<x<825 and 810<y<855:  # Back to login
                    input_active=None
                    return
                else:
                    input_active=None
                if 280<x<620 and 280<y<330:
                    input_active = 'new_username'
                elif 280<x<620 and 360<y<400 :
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

        pygame.draw.rect(screen, black, (280, 280, 340, 50))
        new_username_surface = font2.render(new_username, True, white)
        screen.blit(new_username_surface, (280, 290))

        pygame.draw.rect(screen, black, (280, 360, 340, 50))
        new_password_surface = font2.render('*' * len(new_password), True, white)
        screen.blit(new_password_surface, (280, 370))

        display_text('Username:', 'white', 90, 295)
        display_text('Password:', 'white', 90, 375)

        draw_button(350, 400, 200, 150, 'sign_up_button.png')  # Sign-up button
        display_text('Back to Login', 'red', 525, 810)  # Back to login button

        pygame.display.flip()

def game_selection_screen():
    global selected_game
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 50<x<600 and 225<y<275:
                    selected_game='Flappy Bird'
                    play_game(selected_game)
                elif 50<x<600 and 325<y<375:
                    selected_game='Tetris'
                    play_game(selected_game)
                elif 50<x<600 and 425<y<475:
                    selected_game='Snake'
                    play_game(selected_game)
                elif 600<x<825 and 225<y<275:
                    selected_game='Breakout'
                    play_game(selected_game)
                elif 600<x<825 and 325<y<375:
                    selected_game='Space Invaders'
                    play_game(selected_game)
                elif 600<x<825 and 425<y<475:
                    selected_game='Jumpy'
                    play_game(selected_game)
                if 675<x<810 and 810<y<855:
                    login_screen()
                    
        screen.blit(bg_image2,(0,0))
        display_text('Choose a Game','white',450,100)

        draw_button(150,225,500,150,'Game_button/flappy_button.png')
        draw_button(150,325,450,100,'Game_button/tetris_button.png')
        draw_button(150,425,450,100,'Game_button/snake_button.png')
        draw_button(825,225,450,100,'Game_button/breakout_button.png')
        draw_button(825,325,450,100,'Game_button/space invaders_button.png')
        draw_button(825,425,450,100,'Game_button/jumpy_button.png')

        display_text('Log out','red',675,810)

        pygame.display.flip()
    
def play_game(selected_game):
    if selected_game=='Flappy Bird':
        f.flappy_bird()
    elif selected_game=='Tetris':
        pass
    elif selected_game=='Snake':
        pygame.display.quit()
        s.Snake()
    elif selected_game=='Breakout':
        pygame.display.quit()
        b.Breakout()
    elif selected_game=='Space_Invaders':
        pygame.display.quit()
        si.space_invaders()
    elif selected_game=='Jumpy':
        pygame.display.quit()
        j.Jumpy()
        
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
                if 275<x<420 and 290<y<325:
                    login_screen()
                elif 450<x<600 and 290<y<325:
                    sign_up_screen()

        screen.blit(bg_image1,(0,0))
        display_text('Welcome to Gamu Arcade','white',220,270)
        draw_button(220,210,250,200,'login_button.png')
        draw_button(400, 210, 250, 200, 'sign_up_button.png')  # Sign-up button


        pygame.display.flip()

start_screen()
