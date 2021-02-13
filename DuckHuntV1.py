# Librerias Necesarias.
import random
import os
import background
import pygame


VidaJugador = 4
Puntuacion = 00
Animales = ['patito', 'pato1', 'bomb', 'b', 'd']
width = 1000
height = 620
Fps = 15
pygame.init()
pygame.display.set_caption('MataPato')
gameDisplay = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# Colores
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

background = pygame.image.load('back.jpg')

# game background
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('P : ' + str(Puntuacion), True, (255, 255, 255))    #score display
lives_icon = pygame.image.load('images/white_lives.png')

def productor_fruta(animal):
    animal_path = "images/" + animal + ".png"
    data[animal] = {
        'img': pygame.image.load(animal_path),
        'x' : random.randint(100,500),
        'y' : 800,
        'speed_x': random.randint(-10,10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[animal]['throw'] = True
    else:
        data[animal]['throw'] = False

data = {}
for animal in Animales:
    productor_fruta(animal)
def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

font_name = pygame.font.match_font('comic.ttf')

def draw_text(display, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        gameDisplay.blit(text_surface, text_rect)

def draw_lives(display, x, y, VidaJugador, image) :
    for i in range(VidaJugador) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "Duck Hunt with Others", 64, width / 2, height / 4)
    if not game_over :
        draw_text(gameDisplay, "P : " + str(score), 50, width / 2, height / 2)

    draw_text(gameDisplay, "Press :/", 24, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(Fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        VidaJugador = 4
        draw_lives(gameDisplay, 690, 5, VidaJugador, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, VidaJugador, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                productor_fruta(key)

            current_position = pygame.mouse.get_pos()

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                if key == 'bomb':
                    VidaJugador -= 1
                    if VidaJugador == 0:
                        hide_cross_lives(690, 15)
                    elif VidaJugador == 1:
                        hide_cross_lives(725, 15)
                    elif VidaJugador == 2:
                        hide_cross_lives(760, 15)

                    if VidaJugador < 0:
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb':
                    Puntuacion += 1
                score_text = font.render('Puntos : ' + str(Puntuacion), True, (255, 255, 255))
                value['hit'] = True
        else:
            productor_fruta(key)

    pygame.display.update()
    clock.tick(Fps)

pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
