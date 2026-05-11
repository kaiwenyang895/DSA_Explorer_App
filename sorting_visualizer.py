import pygame
import sys
#Generate a random number array
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)


def draw_text(screen, text, font, colour, x, y):
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

#It means: generate a list with 10 numbers.
def create_random_array():
    return [random.randint(40, 250) for _ in range(10)]

#visualisation visualisation visualisation
def bubble_sort_steps(data):

    arr = data[:]
    n = len(arr)
#yield: a pause function that gives up the current step, can't use return
    for i in range(n):
        for j in range(0, n - i - 1):
            yield arr[:], j, j + 1, "Comparing " + str(arr[j]) + " and " + str(arr[j + 1])

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr[:], j, j + 1, "Swapped " + str(arr[j]) + " and " + str(arr[j + 1])

    yield arr[:], -1, -1, "Bubble Sort completed."


def selection_sort_steps(data):

    arr = data[:]
    n = len(arr)

    for i in range(n):
        min_index = i
        yield arr[:], i, min_index, "Starting position " + str(i)

        for j in range(i + 1, n):
            yield arr[:], min_index, j, "Comparing current minimum with " + str(arr[j])

            if arr[j] < arr[min_index]:
                min_index = j
                yield arr[:], min_index, j, "New minimum found: " + str(arr[min_index])

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            yield arr[:], i, min_index, "Swapped into correct position."

    yield arr[:], -1, -1, "Selection Sort completed."

#This function is responsible for drawing the array as individual bars.
def draw_array_bars(screen, array, font, highlight_one, highlight_two):

    start_x = 110
    base_y = 430
    bar_width = 45
    gap = 20

    for index, value in enumerate(array):
        x = start_x + index * (bar_width + gap)
        y = base_y - value

        rect = pygame.Rect(x, y, bar_width, value)

        if index == highlight_one or index == highlight_two:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        value_surface = font.render(str(value), True, BLACK)
        value_rect = value_surface.get_rect(center=(x + bar_width // 2, base_y + 18))
        screen.blit(value_surface, value_rect)


def run_sorting_module(screen, clock):

    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    original_array = create_random_array()
    current_array = original_array[:]

    selected_algorithm = "Bubble Sort"
    #Save sorting progress
    sort_generator = None

    is_sorting = False
    highlight_one = -1
    highlight_two = -1
    message = "Choose an algorithm and click Start."

    last_step_time = 0
    step_delay = 400

    back_button = pygame.Rect(25, 25, 95, 40)

    bubble_button = pygame.Rect(100, 500, 130, 40)
    selection_button = pygame.Rect(250, 500, 150, 40)
    start_button = pygame.Rect(430, 500, 100, 40)
    reset_button = pygame.Rect(550, 500, 100, 40)
    new_array_button = pygame.Rect(670, 500, 130, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(
            screen,
            "Sorting Algorithms Module",
            title_font,
            BLACK,
            250,
            35
        )

        draw_text(
            screen,
            "Visualising Bubble Sort and Selection Sort",
            small_font,
            BLACK,
            265,
            75
        )

        draw_text(
            screen,
            "Selected Algorithm: " + selected_algorithm,
            small_font,
            BLACK,
            320,
            110
        )

        draw_text(
            screen,
            message,
            small_font,
            BLACK,
            230,
            455
        )

        draw_array_bars(screen, current_array, small_font, highlight_one, highlight_two)

        draw_button(screen, "Bubble Sort", bubble_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Selection Sort", selection_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Start", start_button, button_font, ORANGE)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_RED)
        draw_button(screen, "New Array", new_array_button, button_font, LIGHT_GRAY)

        current_time = pygame.time.get_ticks()

        if is_sorting and sort_generator is not None:
            if current_time - last_step_time > step_delay:
                try:
                    current_array, highlight_one, highlight_two, message = next(sort_generator)
                    last_step_time = current_time
                except StopIteration:
                    is_sorting = False
                    highlight_one = -1
                    highlight_two = -1
                    message = selected_algorithm + " finished."
# same as the main
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    running = False

                elif bubble_button.collidepoint(mouse_pos):
                    selected_algorithm = "Bubble Sort"
                    current_array = original_array[:]
                    sort_generator = None
                    is_sorting = False
                    highlight_one = -1
                    highlight_two = -1
                    message = "Bubble Sort selected."

                elif selection_button.collidepoint(mouse_pos):
                    selected_algorithm = "Selection Sort"
                    current_array = original_array[:]
                    sort_generator = None
                    is_sorting = False
                    highlight_one = -1
                    highlight_two = -1
                    message = "Selection Sort selected."

                elif start_button.collidepoint(mouse_pos):
                    if selected_algorithm == "Bubble Sort":
                        sort_generator = bubble_sort_steps(current_array)
                    elif selected_algorithm == "Selection Sort":
                        sort_generator = selection_sort_steps(current_array)

                    is_sorting = True
                    last_step_time = pygame.time.get_ticks()
                    message = selected_algorithm + " started."

                elif reset_button.collidepoint(mouse_pos):
                    current_array = original_array[:]
                    sort_generator = None
                    is_sorting = False
                    highlight_one = -1
                    highlight_two = -1
                    message = "Array reset."

                elif new_array_button.collidepoint(mouse_pos):
                    original_array = create_random_array()
                    current_array = original_array[:]
                    sort_generator = None
                    is_sorting = False
                    highlight_one = -1
                    highlight_two = -1
                    message = "New random array generated."

#start
        pygame.display.update()
        clock.tick(60)