import pygame
import sys

# import the main module pages
from data_structures import run_data_structures_module
from algorithms_menu import run_algorithms_menu
from puzzle_module import run_puzzle_module


pygame.init()

# window size for the whole app
WIDTH = 1100
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Explorer and Visualiser App")

# clock is used to control FPS
clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
YELLOW = (255, 255, 153)
LIGHT_GRAY = (230, 230, 230)
ORANGE = (255, 204, 153)


def draw_text(text, font, colour, x, y):
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(text, rect, colour):
    # draw button with border
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # put the text in middle of button
    text_surface = button_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def testing_summary_page():
    # this page is not running tests, only show testing info
    running = True

    back_button = pygame.Rect(25, 25, 95, 40)

    while running:
        screen.fill(WHITE)

        draw_button("Back", back_button, LIGHT_GRAY)

        draw_text(
            "Testing Summary",
            title_font,
            BLACK,
            390,
            80
        )

        draw_text(
            "Automated tests are written in a separate Python file:",
            small_font,
            BLACK,
            260,
            160
        )

        draw_text(
            "test_algorithms.py",
            button_font,
            BLACK,
            430,
            200
        )

        draw_text(
            "Run command:",
            small_font,
            BLACK,
            260,
            270
        )

        draw_text(
            "python -m unittest test_algorithms.py",
            button_font,
            BLACK,
            340,
            310
        )

        draw_text(
            "The tests check the algorithm logic, such as stack, queue, sorting, graph, heap and DP.",
            small_font,
            BLACK,
            180,
            390
        )


        draw_text(
            "This page is only a testing summary. The real automated tests are still in test_algorithms.py.",
            small_font,
            BLACK,
            170,
            500
        )

        # only need back button and quit event on this page
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


def main_menu():
    # main page for choosing different parts of the app
    running = True

    # menu buttons position
    data_button = pygame.Rect(400, 170, 300, 55)
    algorithms_button = pygame.Rect(400, 250, 300, 55)
    puzzle_button = pygame.Rect(400, 330, 300, 55)
    tests_button = pygame.Rect(400, 410, 300, 55)

    while running:
        screen.fill(WHITE)

        draw_text(
            "DSA Explorer and Visualiser App",
            title_font,
            BLACK,
            250,
            80
        )

        draw_text(
            "Main Menu",
            small_font,
            BLACK,
            500,
            135
        )

        # four main choices in the app
        draw_button("Data Structures", data_button, LIGHT_BLUE)
        draw_button("Algorithms", algorithms_button, LIGHT_GREEN)
        draw_button("Puzzle Challenges", puzzle_button, YELLOW)
        draw_button("Tests", tests_button, ORANGE)

        draw_text(
            "u3290623_7170",
            small_font,
            BLACK,
            490,
            500
        )

        # handle user mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # open data structures menu
                if data_button.collidepoint(mouse_pos):
                    run_data_structures_module(screen, clock)

                # open algorithm menu
                elif algorithms_button.collidepoint(mouse_pos):
                    run_algorithms_menu(screen, clock)

                # open puzzle and DP page
                elif puzzle_button.collidepoint(mouse_pos):
                    run_puzzle_module(screen, clock)

                # open testing summary page
                elif tests_button.collidepoint(mouse_pos):
                    testing_summary_page()

        # refresh main window
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# #########start the app from main menu
if __name__ == "__main__":
    main_menu()