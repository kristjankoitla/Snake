#IMPORTS
import time
import os
from msvcrt import getch
import threading
from random import randint
import pygame
from pygame.locals import *


pygame.init()
pygame.display.set_caption('Snek')

def game():
    #FONT
    score_font = pygame.font.SysFont('Comic Sans MS', 10)

    #DEFINING COLORS
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    dark_brown = (51, 25, 0)

    snake_color = yellow
    food_color = green

    #DEFAULTS
    length = 0
    history = [] #of snake
    direction = 'RIGHT' #of snake
    direction_new = 'RIGHT'
    toggle = False #dope mode
    light_toggle = False
    done = False #main loop

    score = 0

    #BOUNDS
    screen_x = 300
    screen_y = 200

    x_bound_high = screen_x-10
    y_bound_high = screen_y-10

    #STARTING POS FOR FOOD & SNAKE
    snake_x = 0
    snake_y = 0
    food_x = randint(0, screen_x/10-1)
    food_y = randint(0, screen_y/10-1)
    special_food_x = -2
    special_food_y = -2

    #TICK START & COUNT
    tick = 0
    tc = 2

    #MAIN (IDK)
    screen = pygame.display.set_mode((screen_x, screen_y))
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 25)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == timer_event:
                tick += 1

                #<ENGINE START>
                #GET PRESSED KEY
                pressed = pygame.key.get_pressed()

                #SET DIRECTION
                if pressed[pygame.K_UP]: direction_new = 'UP'
                if pressed[pygame.K_DOWN]: direction_new = 'DOWN'
                if pressed[pygame.K_LEFT]: direction_new = 'LEFT'
                if pressed[pygame.K_RIGHT]: direction_new = 'RIGHT'

                #MOVING & LOCK
                if tick % tc == 0:
                    if direction != 'DOWN' and direction_new == 'UP':
                        direction = 'UP'
                        
                    if direction != 'UP' and direction_new == 'DOWN':
                        direction = 'DOWN'

                    if direction != 'RIGHT' and direction_new == 'LEFT':
                        direction = 'LEFT'

                    if direction != 'LEFT' and direction_new == 'RIGHT':
                        direction = 'RIGHT'

                    if direction == 'UP': snake_y -= 10
                    if direction == 'DOWN': snake_y += 10
                    if direction == 'LEFT': snake_x -= 10
                    if direction == 'RIGHT': snake_x += 10

                #IF OUT OF BOUNDS
                if snake_x > x_bound_high: snake_x = 0
                if snake_x < 0: snake_x = x_bound_high
                if snake_y > y_bound_high: snake_y = 0
                if snake_y < 0: snake_y = y_bound_high

                #SNAKE LOCATION
                snake = pygame.Rect(snake_x, snake_y, 10, 10)
                head_patch = pygame.Rect(snake_x+2, snake_y+2, 6, 6)

                #FOOD LOCATION
                food = pygame.Rect(food_x*10+2, food_y*10+2, 6, 6)
                special_food = pygame.Rect(special_food_x*10+2, special_food_y*10+2, 6, 6)

                #FOOD COLLISION
                if snake.colliderect(food):
                    food_collision = True
                else:
                    food_collision = False

                if snake.colliderect(special_food):
                    special_food_collision = True
                else:
                    special_food_collision = False

                #FOOD RELOCATING & SPECIAL TOGGLE
                if food_collision == True:
                    score += 100+ length*10
                    if randint(1,75)%74==0:
                        tick_start = tick
                        food_x = -2
                        food_Y = -2
                        special_food_x = randint(0, screen_x/10-1)
                        special_food_y = randint(0, screen_y/10-1)
                        light_toggle = not light_toggle
                    else:
                        food_x = randint(0, screen_x/10-1)
                        food_y = randint(0, screen_y/10-1)
                        special_food_x = -2
                        special_food_y = -2

                if special_food_collision == True:
                    score += 250 + length*10
                    for i in range(int(length/10)):
                        del history[0]
                        
                    special_food_collision = False
                    if not toggle:
                        toggle = not toggle
                        special_food_x = randint(0, screen_x/10-1)
                        special_food_y = randint(0, screen_y/10-1)
                    else:
                        toggle = not toggle
                        light_toggle = False
                        special_food_x = -2
                        special_food_y = -2
                        food_x = randint(0, screen_x/10-1)
                        food_y = randint(0, screen_y/10-1)

                #TAIL LOGGING
                if tick % tc == 0:
                    if food_collision == True or pressed[pygame.K_SPACE]:
                        history.append([snake_x, snake_y])
                        length +=1
                    else:
                        history.append([snake_x, snake_y])
                        del history[0]

                #TAIL COLLISION
                if [snake_x, snake_y] in history[:-1] and not toggle:
                    done = True
                        
                #SCORE
                text = score_font.render(str(score), False, (255, 255, 255))
                
                #<CAST PICTURE>
                #BACKGROUND
                screen.fill(dark_brown)

                #FOOD
                pygame.draw.rect(screen, (food_color), food)
                pygame.draw.rect(screen, (red), special_food)

                #FULL TAIL & COLOR SWITCH
                for i in range(len(history)):
                    pygame.draw.rect(screen, (snake_color), pygame.Rect(history[i][0]+2, history[i][1]+2, 6, 6))

                #SNAKE HEAD
                pygame.draw.rect(screen, (snake_color), snake)
                pygame.draw.rect(screen, (black), head_patch)

                #SCORE
                screen.blit(text, [0, 0])


                #DOPE
                if pressed[pygame.K_r]:
                    toggle = not toggle

                if light_toggle:
                    red = (randint(1, 255), randint(1, 255), randint(1, 255))
                else:
                    red = (255, 0, 0)

                if toggle:
                    if tick % 3 == 0:
                        snake_color = (randint(1, 255), randint(1, 255), randint(1, 255))
                        food_color = (randint(1, 255), randint(1, 255), randint(1, 255))

                    if tick % 12 == 0:
                        dark_brown = (randint(1, 255), randint(1, 255), randint(1, 255))

                    if tick % 50 == 0:
                        snake_x = randint(0, screen_x-10)
                        snake_y = randint(0, screen_y-10)
                else:
                        snake_color = (yellow)
                        food_color = (green)
                        dark_brown = (51, 25, 0)

                #</CAST PICTURE>
                #DEV TOOLS
                #if tick % 2 == 0:
                #    if pressed[pygame.K_q]:
                #        history.append([snake_x, snake_y])
                #
                #    if pressed[pygame.K_s]:
                #        direction = None
                    
                #</DEV TOOLS>
                #</ENGINE>

        pygame.display.flip()
while True:
    game()
    time.sleep(4)
    
