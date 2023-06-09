import pygame
import sys 
from pygame.locals import *
import random

def get_words():
    string = ''
    words = []
    index = 0

    with open('dict.txt', 'r') as fp:
        string = str(fp.readline())
        words = string.split(",")
        index = random.randint(0, len(words))
        print(words[index])
        return words[index].upper()
    
    return 'Error'

def draw_btns(BUTTONS):
    for button,letter in BUTTONS:
        btn_text = btn_font.render(letter, True, BLACK)
        btn_text_rect = btn_text.get_rect(center=(button.x + SIZE//2, button.y + SIZE//2))
        pygame.draw.rect(screen, BLACK, button, 2) 
        screen.blit(btn_text, btn_text_rect)


def display_guess():
    display_word = ''

    for letter in WORD:
        if letter in GUESSED:
            display_word += f"{letter} "
        else:
            display_word += "_ "

    text = letter_font.render(display_word, True, BLACK)
    screen.blit(text, (400, 200))

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

game_over = False

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

#images
IMAGES = []
hangman_status = 0

for i in range(7):
    image = pygame.image.load(f"images\hangman{i}.png")
    IMAGES.append(image)

#Buttons
ROWS = 2
COLS = 13
GAP = 20
SIZE = 40
BOXES = []


for row in range(ROWS):
    for col in range(COLS):
        x = ((GAP * col) + GAP) + (SIZE * col)
        y = ((GAP * row) + GAP) + (SIZE * row) + 330
        box = pygame.Rect(x,y,SIZE,SIZE)
        BOXES.append(box)

A = 65
BUTTONS = []

for ind, box in enumerate(BOXES):
    letter = chr(A+ind)
    button = ([box, letter])
    BUTTONS.append(button)

#Fonts
btn_font = pygame.font.SysFont('Montserrat', 30)
letter_font = pygame.font.SysFont('Montserrat', 60)
game_font = pygame.font.SysFont('Montserrat', 80)

#Word
WORD = get_words()
GUESSED = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN:
            clicked_pos = event.pos

            for button, letter in BUTTONS:
                if button.collidepoint(clicked_pos):
                    GUESSED.append(letter)

                    if letter not in WORD:
                        hangman_status += 1

                    if hangman_status == 6:
                        game_over = True
                        
                    BUTTONS.remove([button, letter])

    screen.fill(WHITE)
    screen.blit(IMAGES[hangman_status], (150,100))
    draw_btns(BUTTONS)
    display_guess()

    won = True

    for letter in WORD:
        if letter not in GUESSED:
            won = False
    
    if won:
        game_over = True
        display_text = 'You Won!'
    else:
        display_text = 'You Lost!'

    pygame.display.update()

    if game_over:
        screen.fill(WHITE)
        game_over_text = game_font.render(display_text, True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH//2,HEIGHT//2))
        screen.blit(game_over_text, game_over_text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()