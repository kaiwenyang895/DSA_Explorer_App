#pygame
import pygame
# for system exit
import sys
from data_structures import run_data_structures_module
from sorting_visualizer import run_sorting_module
from graph_visualizer import run_graph_module
from puzzle_module import run_puzzle_module
#initial the window
pygame.init()
# Window size 900600  !!Preparing in advance is safer
WIDTH = 900
HEIGHT = 600

# creat the window,
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#tital of the window
pygame.display.set_caption("DSA Explorer and Visualiser App")
#Limiting the program's refresh doesn't really do much here,
# but I included it since I learned it.
clock = pygame.time.Clock()

# Fonts for tittle button and others
title_font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 26)

# just colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)
LIGHT_GRAY = (230, 230, 230)
GREEN = (144, 238, 144)

#
def draw_text(text, font, colour, x, y):
    #Convert plain text into an image object that Pygame can display.
    #true for Anti-aliasing
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))

# rect is the position and size
def draw_button(text, rect, colour):
    pygame.draw.rect(screen, colour, rect)
    #Draw a black border around the button.

#The final 2 indicates that the border thickness is 2 pixels.
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = button_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    #dipict on the screen
    screen.blit(text_surface, text_rect)


def show_placeholder_page(module_name):
    """
    This is a temporary page for each module.
    Later we will replace this with real visualisation.
    """
    running = True

    back_button = pygame.Rect(30, 30, 120, 45)

    while running:
        screen.fill(WHITE)

        draw_button("Back", back_button, LIGHT_GRAY)

        draw_text(module_name, title_font, BLACK, 260, 120)

        draw_text(
            "This module page is working.",
            small_font,
            BLACK,
            280,
            200
        )

        draw_text(
            "Later we will add Pygame visualisation here.",
            small_font,
            BLACK,
            240,
            240
        )

        draw_text(
            "Press Back to return to Main Menu.",
            small_font,
            BLACK,
            260,
            280
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    running = False

        pygame.display.update()
        clock.tick(60)

#important
def main_menu():
# show the window
    running = True
# creat the button and the position
    data_button = pygame.Rect(300, 160, 300, 55)
    sorting_button = pygame.Rect(300, 230, 300, 55)
    graph_button = pygame.Rect(300, 300, 300, 55)
    puzzle_button = pygame.Rect(300, 370, 300, 55)
#Start the main menu loop. As long as the program hasn’t exited,
# the main menu will keep refreshing.
    while running:
        #background
        screen.fill(WHITE)
#DSA Explorer and Visualiser App our title
        draw_text(
            "DSA Explorer and Visualiser App",
            title_font,
            BLACK,
            160,
            70
        )

        draw_text(
            "Main Menu",
            small_font,
            BLACK,
            395,
            130
        )

        draw_button("Data Structures", data_button, LIGHT_BLUE)
        draw_button("Sorting Algorithms", sorting_button, LIGHT_BLUE)
        draw_button("Graph Algorithms", graph_button, LIGHT_BLUE)
        draw_button("Puzzle Challenges", puzzle_button, LIGHT_BLUE)

        draw_text(
            "Click a button to open a module.",
            small_font,
            BLACK,
            310,
            460
        )
#This code is used to get all current user events. such as click and close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #Get the position of the mouse click.
                mouse_pos = event.pos
#Here, screen and clock are passed in
  #so that the submodules can use the same window and refresh controller.
                if data_button.collidepoint(mouse_pos):
                    run_data_structures_module(screen, clock)


                elif sorting_button.collidepoint(mouse_pos):

                    run_sorting_module(screen, clock)


                elif graph_button.collidepoint(mouse_pos):

                    run_graph_module(screen, clock)

                elif puzzle_button.collidepoint(mouse_pos):
                    run_puzzle_module(screen, clock)
#It doesn't have much significance in this assignment, because the
        # images haven't been updated much,
        # but it can be used for future expansion.
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

#The following code will only execute when this file is run directly.
#It's not useful in this assignment either.
if __name__ == "__main__":
    # start the program, that is useful lol
    main_menu()