import pygame
import sys

# import each data structure pages
from stack_page import run_stack_page
from queue_page import run_queue_page
from linked_list_page import run_linked_list_page
from linear_search_page import run_linear_search_page


# basic colours use in this page
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)


def draw_text(screen, text, font, colour, x, y):
    # draw text on screen
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # draw the button shape
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # make button text in center
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def run_data_structures_module(screen, clock):
    # fonts for title, button and small text
    title_font = pygame.font.SysFont(None, 46)
    button_font = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 24)

    # back button
    back_button = pygame.Rect(30, 30, 100, 42)

    # buttons for each module
    stack_button = pygame.Rect(400, 170, 300, 55)
    queue_button = pygame.Rect(400, 250, 300, 55)
    linked_list_button = pygame.Rect(400, 330, 300, 55)
    linear_search_button = pygame.Rect(400, 410, 300, 55)

    running = True

    while running:
        screen.fill(WHITE)

        # draw page layout
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(
            screen,
            "Data Structures Module",
            title_font,
            BLACK,
            355,
            55
        )

        draw_text(
            screen,
            "Choose one data structure or algorithm to explore.",
            small_font,
            BLACK,
            330,
            110
        )

        draw_button(screen, "Stack", stack_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Queue", queue_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Linked List", linked_list_button, button_font, ORANGE)
        draw_button(screen, "Linear Search", linear_search_button, button_font, YELLOW)

        draw_text(
            screen,
            "Click the help button in the upper right corner of the page to check the operation guide",
            small_font,
            BLACK,
            205,
            510
        )

        # check mouse and window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # back to main menu
                if back_button.collidepoint(mouse_pos):
                    running = False

                # open stack
                elif stack_button.collidepoint(mouse_pos):
                    run_stack_page(screen, clock)

                # open queue
                elif queue_button.collidepoint(mouse_pos):
                    run_queue_page(screen, clock)

                # open linked list
                elif linked_list_button.collidepoint(mouse_pos):
                    run_linked_list_page(screen, clock)

                # open linear search
                elif linear_search_button.collidepoint(mouse_pos):
                    run_linear_search_page(screen, clock)


        pygame.display.update()
        clock.tick(60)