import pygame
import random
import queue
import copy
import Inital_screen

pygame.init()
# A game main loop
# Behöver två stycken grids:
# En i bakgrund när man har klickat på och en framför med tomma rutor
# Gör den bakom först
# Importera en bild på mina!
#

#WIDTH  = 520
#HEIGHT = 560
#window = pygame.display.set_mode((WIDTH , HEIGHT))           # create inital window
#window = pygame.display.set_mode((WIDTH , HEIGHT))           # create inital window
# pygame.display.set_caption("Minesweeper 2.0")
#ROWS = 10
#BOMBS = 10
COLUMNS = 10
BLACK = (0, 0, 0)
GRAY = (158, 158, 158)
WHITE = (255, 255, 255)
LIGHT_GRAY = (18, 1, 1)
COVER_BLUE = (51, 153, 255)

# Clock pos varierar på vilken screen vi har
CLOCK_POS = (20,20)     # Så ändra denna!

NUM_FONT = pygame.font.SysFont('comicsans', 20)
FONT_clock = pygame.font.SysFont('comicsans', 20)
NUM_COLOR = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "orange", 6: "magenta", "X": "black", '': "black"}

# return a nested list with all the mines defined as X!
# fylla i rosw och columns beroende på vilka inställningar man har!
def grid_mines(ROWS, COLUMNS, BOMBS):
    length = ROWS*COLUMNS       # Längd på lista som skapas
    none_bombs_grids = length - BOMBS       # Hur många rutor ska inte vara bomber
    zeros_list = [0]*length
    counter = length
    while counter != none_bombs_grids:
        counter = zeros_list.count(0)            # do a counter of how many the elements equal to zero.
        index = random.randint(0, length-1)
        zeros_list[index] = 100                  # Set the bombs to a int of 10
    nestlist = []

    # Lägg listan i en nested list istället
    click = 1
    for i in range(ROWS):
        upper_limit = click*COLUMNS
        lower_limit = upper_limit-COLUMNS
        ls = zeros_list[lower_limit:upper_limit]
        nestlist.append(ls)
        click += 1
    return nestlist

# Input: nested list, 100 is a bomb, 0 is not bomb.
# Output: Field with bombs = "X", numbers = "1-8", and empty squares = ""
def grid_number(nestlist):
    # Iterate through and add a number around each bomb.
    for i, row in enumerate(nestlist):
        for j, element in enumerate(row):
            if element >= 100:
                if i == 0 and j == 0:   # Uppe vänsta hörnet, måste ändra specialfall när vi har flera olika
                    nestlist[i][j+1] += 1
                    nestlist[i+1][j] += 1
                    nestlist[i+1][j+1] += 1
                elif i == 9 and j == 0:   # Nedre vänsta hörnet
                    nestlist[i-1][j] += 1
                    nestlist[i-1][j+1] += 1
                    nestlist[i][j+1] += 1
                elif i == 0 and j == 9:   # Övre högra hörnet
                    nestlist[i][j-1] += 1
                    nestlist[i+1][j-1] += 1
                    nestlist[i+1][j] += 1
                elif i == 9 and j == 9:
                    nestlist[i-1][j-1] += 1
                    nestlist[i-1][j] += 1
                    nestlist[i][j-1] += 1
                elif i == 0:
                    nestlist[i][j-1] += 1
                    nestlist[i][j+1] += 1
                    nestlist[i+1][j-1] += 1
                    nestlist[i+1][j] += 1
                    nestlist[i+1][j+1] += 1
                elif i == 9:
                    nestlist[i-1][j-1] += 1
                    nestlist[i-1][j] += 1
                    nestlist[i-1][j+1] += 1
                    nestlist[i][j-1] += 1
                    nestlist[i][j+1] += 1
                elif j == 0:
                    nestlist[i-1][j] += 1
                    nestlist[i-1][j+1] += 1
                    nestlist[i][j+1] += 1
                    nestlist[i+1][j] += 1
                    nestlist[i+1][j+1] += 1
                elif j == 9:
                    nestlist[i-1][j-1] += 1
                    nestlist[i-1][j] += 1
                    nestlist[i][j-1] += 1
                    nestlist[i+1][j-1] += 1
                    nestlist[i+1][j] += 1
                else:
                    nestlist[i-1][j-1] += 1
                    nestlist[i-1][j] += 1
                    nestlist[i-1][j+1] += 1
                    nestlist[i][j-1] += 1
                    nestlist[i][j+1] += 1
                    nestlist[i+1][j-1] += 1
                    nestlist[i+1][j] += 1
                    nestlist[i+1][j+1] += 1

    # Convert all the bombs to 'X'
    for i, row in enumerate(nestlist):
        for j, element in enumerate(row):
            if element >= 100:
                nestlist[i][j] = 'X'
            if element == 0:
                nestlist[i][j] = ''

    # Create a copy_field [Used for checking if all bombs are placed correctly]
    # change all "X" for "O"
    copy_nestlist = copy.deepcopy(nestlist)
    for i, row in enumerate(copy_nestlist):
            for j, element in enumerate(row):
                if element == 'X':
                    copy_nestlist[i][j] = 'O'
    return nestlist, copy_nestlist

# Return the back field!
def draw(window, field, width_size, height_size):
    window.fill(GRAY)
    # hur stor är varje ruta!
    for i, row in enumerate(field):
        y_pos = height_size*i + 50
        for j, element in enumerate(row):
            x_pos = width_size*j + 10
            text = NUM_FONT.render(str(element), 1, NUM_COLOR[element])       # What is the number on that index

            pygame.draw.rect(window, GRAY, (x_pos, y_pos, width_size, height_size))            # Actual box, to be used later
            pygame.draw.rect(window, 'black', (x_pos, y_pos, width_size, height_size), 1)      # Create a black frame
            window.blit(text, (x_pos + (width_size/2 -text.get_width()/2),
                               y_pos + (width_size/2 -text.get_width()/2)))     # Center the text in middle of box

    pygame.display.update()

# Create the cover layer, (AKA buttons to be clicked )
def draw_coverfield(field, width_size, height_size, WIDTH, HEIGHT):
    window = pygame.display.set_mode((WIDTH , HEIGHT))           # create inital window
    pygame.display.set_caption("Minesweeper 2.0")
    window.fill(LIGHT_GRAY)
    for i, row in enumerate(field):
            y_pos = height_size*i + 50
            for j, element in enumerate(row):
                x_pos = width_size*j + 10

                pygame.draw.rect(window, COVER_BLUE, (x_pos, y_pos, width_size, height_size))
                pygame.draw.rect(window, "black", (x_pos, y_pos, width_size, height_size), 1)

    pygame.display.update()
    return window

def get_sizes(COLUMNS, ROWS, WIDTH, HEIGHT):
    width_size = (WIDTH-20)/COLUMNS
    height_size = (HEIGHT-60)/ROWS
    return width_size, height_size

# Input: mouseclick coordinates
# Output: index of in what square the click occured.
def get_grid_pos(mouse_pos, width_size, height_size):

    mouse_pos_ls = list(mouse_pos)
    x_pos = mouse_pos_ls[0] - 10
    y_pos = mouse_pos_ls[1] - 50
    x_index = int(x_pos / width_size)
    y_index = int(y_pos / height_size)
    cord_list = get_cord_list(x_index, y_index, height_size, width_size)
    index_list = [x_index, y_index]

    return cord_list, index_list

# Input: Index
# Output: Coordinates
def get_cord_list(x_index, y_index, height_size, width_size):
    y_pos = height_size*y_index + 50
    x_pos = width_size*x_index + 10
    cord_list = [x_pos, y_pos]
    return cord_list

# Input:
# Output: Ritar ut rutan
def change_box(cord_list, index_list, field, window, width_size, height_size):
    # Draw the box!
    x_pos = cord_list[0]
    y_pos = cord_list[1]
    pygame.draw.rect(window, GRAY, (x_pos, y_pos, width_size, height_size))

    # Draw the text
    element = field[index_list[0]][index_list[1]]
    text = NUM_FONT.render(str(element), 1, NUM_COLOR[element])       # What is the number on that index
    window.blit(text, (x_pos + (width_size/2 -text.get_width()/2),
                               y_pos + (width_size/2 -text.get_width()/2)))

    pygame.display.update()

# Input: A rightclick
# Output: A "O" is visualised as the bomb
def change_box_mine(cord_list, window, width_size):
    x_pos = cord_list[0]
    y_pos = cord_list[1]
    text = NUM_FONT.render("O", 1, "black")       # What is the number on that index
    window.blit(text, (x_pos + (width_size/2 -text.get_width()/2),
                               y_pos + (width_size/2 -text.get_width()/2)))
    pygame.display.update()


def change_controllfield(controll_field, index_list):
    controll_field[index_list[0]][index_list[1]] = 'X'
    return controll_field

# Input: Index list and the field
# Output, True or False statement
def check_gameover(index_list, field):
    element = field[index_list[0]][index_list[1]]
    if element == 'X':
        return False
    else:
        return True

# Output: Kollar om ruta är tom, isf skriver den ut alla som angränsar till tom ruta.
def blank_checker(index_list, field, height_size, width_size, window, visited_list = []):
    element = field[index_list[0]][index_list[1]]
    if element == '':
        q = queue.Queue()               # Skappa en queue, men är det här vi önskar ha den?!?
        for i in range(-1, 2):
            for j in range(-1, 2):
                grannar_list = [index_list[0] + i, index_list[1] + j]

                # måste ändra denna till rows
                if grannar_list[0] == 10 or grannar_list[0] == -1 or grannar_list[1] == -1 or grannar_list[1] == 10:
                    pass
                elif grannar_list == index_list:
                    pass
                else:
                    q.put(grannar_list)             # Lägg till alla i omgivning i lista!

        # Måste kolla så element varit i
        while not q.empty():
            index_list = q.get()
            cord_list = get_cord_list(index_list[0], index_list[1], height_size, width_size)         # Hitta coordinater för att draw picture!
            if index_list not in visited_list:
                change_box(cord_list, index_list, field, window, width_size, height_size)
                visited_list.append(index_list)
                blank_checker(index_list, field, height_size, width_size, window, visited_list)
    else:
        return

# Inital screen AKA home screen!
def background_setup():
    Inital_screen.initial_screen()

def check_game_diff(game_diffculty):
    if game_diffculty == 'easy':
            WIDTH  = 520
            HEIGHT = 560
            ROWS = 10
            BOMBS = 10
            COLUMNS = 10
        # if game_diffculty == 'medium':

    return WIDTH, HEIGHT, ROWS, BOMBS, COLUMNS

def check_game_over_option(game_over_option):
    if game_over_option == 'play_again':
        # Gå till vilken funktion?
        pass




# Where are we, when the counter is what?
# counter = 0: Setting up prefered gamemode
# counter = 1: Placed at bottom --> Change to two right away: Gameplay screen
# counter = 2: At the first click we start the time -->
# counter = 3: The clock is only avaibale when clock = 3 (Game is running)
# counter = 4: At game end screen

def main():

    background_setup()
    clock = pygame.time.Clock()
    start_time = None

    run = True
    counter = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Initial screen with three different options to choose among

            gameplay(event, game_diffculty)

            # Kollar vilken svårighet man klickar på! --> returnerar variabler för att skapa den spelplanen!
            if event.type == pygame.MOUSEBUTTONDOWN and counter == 0:            # När spelare klickar på ruta
                mouse_pos = pygame.mouse.get_pos()                # Erhåll pos av musen

                # När jag ska spela igen, vill jag komma tillbaka hit!

                game_diffculty = Inital_screen.get_difficulty(mouse_pos)

                # Allt härifrån behöver jag mata in igen
                WIDTH, HEIGHT, ROWS, BOMBS, COLUMNS = check_game_diff(game_diffculty)

                nestlist = grid_mines(ROWS, COLUMNS, BOMBS)                             # A nested list
                field, controll_field = grid_number(nestlist)                                           # Create the field. Just in the backend all the time
                width_size, height_size = get_sizes(ROWS, COLUMNS, WIDTH, HEIGHT)       # Get size of board
                window = draw_coverfield(field, width_size, height_size, WIDTH, HEIGHT)                 # Create inital look
                counter = 1

            # En if loop som startar tiden
            if event.type == pygame.MOUSEBUTTONDOWN and counter == 2:
                if event.button == 1:
                    start_time = pygame.time.get_ticks()                # Startar tiden till timer (Nu är start_time ej längre 0)
                counter = 3

            # håller koll på tiden!
            if start_time != None and counter == 3:
                time_since_enter = pygame.time.get_ticks() - start_time
                klocka = int(time_since_enter/1000)
                pygame.draw.rect(window, 'black', (0, 0, 100, 50))
                window.blit(FONT_clock.render(str(klocka), 1, "red"), (CLOCK_POS))      # Den börjar bli lite seg! FIXA
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and counter >= 3:            # När spelare klickar på ruta
                mouse_pos = pygame.mouse.get_pos()                # Erhåll pos av musen
                cord_list, index_list = get_grid_pos(mouse_pos, width_size, height_size)    # Erhåll index och coordinat pos

                # Nu skiljer vi på vänster och högerclick
                if event.button == 3:       # RIGHT Button
                    change_box_mine(cord_list, window, width_size)      # Rita ut en cirkel!
                    controll_field = change_controllfield(controll_field, index_list)    # update the controllfield
                    if controll_field == field:         # Check if the player has won!
                        # Another screen that shows up - Time (20), highscore (60), play again (20), in order from top to bottom
                        print("you win - Yay")


                if event.button == 1:       # LEFT Button
                    if counter == 3:
                        change_box(cord_list, index_list, field, window, width_size, height_size)                       # Update the window
                    bool_checker = check_gameover(index_list, field)                        # Kolla om "mina"
                    if bool_checker == False:
                        counter = 4
                        # Make the bomb red
                        Inital_screen.game_over_screen()            # Paint out the game_over screen!
                    blank_checker(index_list, field, height_size, width_size, window)   # Kolla angående angränsande rutor!

                # Now are we att the game_over screen!
                if counter == 4:
                    game_over_option = Inital_screen.game_over_click_options(mouse_pos)
                    check_game_over_option(game_over_option)
                    print(game_diffculty)
                        # Play again
                        # Main menu
                        # if mousebutton == 1
                            # Så återkallar
                        # Nu vi quit --> Annars ska vi få upp en screen som säger Game over
                        # draw screen som kommer fram och frågar - play again?
                        # Något med High score?
                        # event.type = pygame.QUIT



            # Ger en paus i iteration
            if counter == 1:
                counter = 2

            clock.tick(60)
                            # högerklick, markera ut ett O (flagga) --> skapa en kopia field med "O" istället för "X"
                            # När alla "X" ärytbytta  mot "O" då ser de likadana ut. Då har man vunnit!
                            # Game win - Hur ska vi kontrollera att vi vunnit - Allt förutom bomber markerade eller tio korrekta högerclick
                            # High score lista. Hur sparar man en highscore lista?



    # GAME OVER


        # Om man klickar på en bomb, game over
        # Funktion där man kan välja inställningar kring hur stort man vill spela

        #draw(window, field, ROWS, COLUMNS)

    #pygame.quit()


if __name__ == "__main__":
    main()