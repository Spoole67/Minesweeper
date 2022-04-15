import pygame
pygame.init()

WIDTH = 300
HEIGHT = 400
GRAY = (158,158,158)
box_size_x = 200
box_size_y = 80
x_box_start = 50
y_box_start = 50
y_increase_between = 110

def initial_screen():


    window = pygame.display.set_mode((WIDTH , HEIGHT))
    window.fill(GRAY)
    INTIAL_SCREEN_FONT = pygame.font.SysFont('comicsans', 40)

    pygame.draw.rect(window, "black", (x_box_start, y_box_start, box_size_x, box_size_y), 2)
    pygame.draw.rect(window, "black", (x_box_start, y_box_start + y_increase_between, box_size_x, box_size_y), 2)
    pygame.draw.rect(window, "black", (x_box_start, y_box_start + 2*y_increase_between, box_size_x, box_size_y), 2)

    text_easy = INTIAL_SCREEN_FONT.render('EASY', 1, 'black')
    text_medium = INTIAL_SCREEN_FONT.render('MEDIUM', 1, 'black')
    text_hard = INTIAL_SCREEN_FONT.render('HARD', 1, 'black')

    window.blit(text_easy, (x_box_start + box_size_x/2 - text_easy.get_width()/2, y_box_start + box_size_y/2 - text_easy.get_height()/2))
    window.blit(text_medium, (x_box_start + box_size_x/2 - text_medium.get_width()/2,
                              y_box_start + y_increase_between + box_size_y/2 - text_medium.get_height()/2))
    window.blit(text_hard, (x_box_start + box_size_x/2 - text_hard.get_width()/2,
                            y_box_start + 2*y_increase_between + box_size_y/2 - text_hard.get_height()/2))

    pygame.display.update()


    return window

# return what box that was clicked on!
def get_difficulty(mouse_pos):
    mouse_pos_ls = list(mouse_pos)
    if x_box_start <= mouse_pos_ls[0] <= x_box_start + box_size_x and y_box_start <= mouse_pos_ls[1] <= y_box_start + box_size_y:
        gamemode = "easy"
    # if medium
    # if hard
    return gamemode

def game_over_screen():

    window = pygame.display.set_mode((WIDTH , HEIGHT))
    window.fill(GRAY)
    GAME_OVER_SCREEN_FONT = pygame.font.SysFont('comicsans', 30)

    pygame.draw.rect(window, "black", (x_box_start, y_box_start + y_increase_between, box_size_x, box_size_y), 2)
    pygame.draw.rect(window, "black", (x_box_start, y_box_start + 2*y_increase_between, box_size_x, box_size_y), 2)

    text_easy = GAME_OVER_SCREEN_FONT.render('GAME OVER', 1, 'black')
    text_medium = GAME_OVER_SCREEN_FONT.render('PLAY AGAIN', 1, 'black')
    text_hard = GAME_OVER_SCREEN_FONT.render('MAIN MENU', 1, 'black')

    window.blit(text_easy, (x_box_start + box_size_x/2 - text_easy.get_width()/2, y_box_start + box_size_y/2 - text_easy.get_height()/2))
    window.blit(text_medium, (x_box_start + box_size_x/2 - text_medium.get_width()/2,
                              y_box_start + y_increase_between + box_size_y/2 - text_medium.get_height()/2))
    window.blit(text_hard, (x_box_start + box_size_x/2 - text_hard.get_width()/2,
                            y_box_start + 2*y_increase_between + box_size_y/2 - text_hard.get_height()/2))

    pygame.display.update()

def game_over_click_options(mouse_pos):
    mouse_pos_ls = list(mouse_pos)
    if x_box_start <= mouse_pos_ls[0] <= x_box_start + box_size_x \
    and y_box_start + y_increase_between <= mouse_pos_ls[1] <= y_box_start + y_increase_between + box_size_y:
         game_over_option = "play_again"
    # if ....
    # game_over_option = "main_menu"

