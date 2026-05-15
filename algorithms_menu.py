import pygame
import sys

# import each algorithm pages
from sorting_algorithms_module import run_sorting_algorithms_module
from graph_algorithms_module import run_graph_algorithms_module
from graph_traversal_module import run_graph_traversal_module
from heap_priority_queue_module import run_heap_priority_queue_module


# basic colours for the menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)


def draw_text(screen, text, font, colour, x, y):
    # draw normal text on the screen
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # draw button box and border
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # put the button text in center
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def run_algorithms_menu(screen, clock):
    # fonts for title, buttons and small notes
    title_font = pygame.font.SysFont(None, 46)
    button_font = pygame.font.SysFont(None, 25)
    small_font = pygame.font.SysFont(None, 23)

    # back button
    back_button = pygame.Rect(30, 30, 100, 42)

    # main menu buttons
    sorting_button = pygame.Rect(380, 180, 340, 55)
    bst_button = pygame.Rect(380, 260, 340, 55)
    graph_button = pygame.Rect(380, 340, 340, 55)
    heap_button = pygame.Rect(380, 420, 340, 55)

    running = True

    while running:
        screen.fill(WHITE)

        # draw menu title and buttons
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(
            screen,
            "Algorithms Module",
            title_font,
            BLACK,
            385,
            70
        )

        draw_text(
            screen,
            "Phase 2 and Phase 3 algorithms are combined here.",
            small_font,
            BLACK,
            325,
            120
        )

        draw_button(screen, "Sorting Algorithms", sorting_button, button_font, LIGHT_BLUE)
        draw_button(screen, "BST Algorithms", bst_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Graph Traversals BFS / DFS", graph_button, button_font, YELLOW)
        draw_button(screen, "Heap Priority Queue", heap_button, button_font, ORANGE)

        # short description for each parts
        draw_text(
            screen,
            "Sorting: Bubble Sort, Selection Sort, Merge Sort",
            small_font,
            BLACK,
            315,
            530
        )

        draw_text(
            screen,
            "BST: Insert, Delete, Search, In-order, Pre-order, Post-order",
            small_font,
            BLACK,
            260,
            560
        )

        draw_text(
            screen,
            "Graph: BFS / DFS traversal     Heap: Priority Queue event simulator",
            small_font,
            BLACK,
            250,
            590
        )

        # handle user click events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # go back to main page
                if back_button.collidepoint(mouse_pos):
                    running = False

                # open sorting
                elif sorting_button.collidepoint(mouse_pos):
                    run_sorting_algorithms_module(screen, clock)

                # open BST
                elif bst_button.collidepoint(mouse_pos):
                    run_graph_algorithms_module(screen, clock)

                # open BFS and DFS page
                elif graph_button.collidepoint(mouse_pos):
                    run_graph_traversal_module(screen, clock)

                # open heap
                elif heap_button.collidepoint(mouse_pos):
                    run_heap_priority_queue_module(screen, clock)


        pygame.display.update()
        clock.tick(60)