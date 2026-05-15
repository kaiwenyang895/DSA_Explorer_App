import pygame
import sys
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)


def draw_text(screen, text, font, colour, x, y):
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def create_random_array():
    # make random values for the sorting bars
    array = []

    for i in range(30):
        array.append(random.randint(40, 330))

    return array


def draw_array(screen, array, font, compare_indexes, swap_indexes, merge_indexes, message):
    start_x = 80
    base_y = 520
    max_height = 330
    bar_width = 28
    gap = 4

    pygame.draw.rect(screen, WHITE, pygame.Rect(50, 170, 1000, 380))

    for index, value in enumerate(array):
        x = start_x + index * (bar_width + gap)
        bar_height = value
        y = base_y - bar_height

        colour = LIGHT_BLUE

        # different colour shows what sorting is doing
        if index in compare_indexes:
            colour = LIGHT_RED

        if index in swap_indexes:
            colour = LIGHT_GREEN

        if index in merge_indexes:
            colour = YELLOW

        rect = pygame.Rect(x, y, bar_width, bar_height)

        pygame.draw.rect(screen, colour, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

    draw_text(screen, message, font, BLACK, 250, 555)


def make_bubble_steps(original_array):
    # save every bubble sort step for animation
    array = original_array[:]
    steps = []
    n = len(array)

    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append((array[:], [j, j + 1], [], [], "Bubble Sort: comparing two neighbouring bars."))

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                steps.append((array[:], [], [j, j + 1], [], "Bubble Sort: swapped two bars."))

    steps.append((array[:], [], [], [], "Bubble Sort finished."))
    return steps


def make_selection_steps(original_array):
    # selection sort finds the smallest value each round
    array = original_array[:]
    steps = []
    n = len(array)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            steps.append((array[:], [min_index, j], [], [], "Selection Sort: finding the smallest value."))

            if array[j] < array[min_index]:
                min_index = j
                steps.append((array[:], [min_index], [], [], "Selection Sort: new minimum found."))

        if min_index != i:
            array[i], array[min_index] = array[min_index], array[i]
            steps.append((array[:], [], [i, min_index], [], "Selection Sort: swapped minimum into correct position."))

    steps.append((array[:], [], [], [], "Selection Sort finished."))
    return steps


def make_merge_steps(original_array):
    # merge sort uses recursive split and merge
    array = original_array[:]
    steps = []

    def merge_sort(left, right):
        if right - left <= 1:
            return

        mid = (left + right) // 2

        split_indexes = list(range(left, right))
        steps.append((array[:], split_indexes, [], [], "Merge Sort: splitting the array."))

        merge_sort(left, mid)
        merge_sort(mid, right)

        temp = []
        i = left
        j = mid

        # compare left part and right part
        while i < mid and j < right:
            steps.append((array[:], [i, j], [], [], "Merge Sort: comparing left and right parts."))

            if array[i] <= array[j]:
                temp.append(array[i])
                i += 1
            else:
                temp.append(array[j])
                j += 1

        while i < mid:
            temp.append(array[i])
            i += 1

        while j < right:
            temp.append(array[j])
            j += 1

        # put sorted values back into array
        for k in range(len(temp)):
            array[left + k] = temp[k]
            steps.append((array[:], [], [], [left + k], "Merge Sort: merging values back."))

    merge_sort(0, len(array))

    steps.append((array[:], [], [], [], "Merge Sort finished."))
    return steps


def show_help_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 23)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Sorting Algorithms", title_font, BLACK, 315, 50)

        draw_text(screen, "1. Bubble Sort compares neighbouring values and swaps them.", small_font, BLACK, 180, 130)
        draw_text(screen, "2. Selection Sort finds the smallest value and moves it forward.", small_font, BLACK, 180, 170)
        draw_text(screen, "3. Merge Sort splits the list, then merges values back in order.", small_font, BLACK, 180, 210)
        draw_text(screen, "4. Red bars mean comparing values.", small_font, BLACK, 180, 250)
        draw_text(screen, "5. Green bars mean values are swapped.", small_font, BLACK, 180, 290)
        draw_text(screen, "6. Yellow bars mean merge process.", small_font, BLACK, 180, 330)
        draw_text(screen, "7. Click Reset Array to create a new random array.", small_font, BLACK, 180, 370)
        draw_text(screen, "8. Click Back to return to the Algorithms Menu.", small_font, BLACK, 180, 410)

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


def run_sorting_algorithms_module(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 22)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    bubble_button = pygame.Rect(120, 100, 130, 45)
    selection_button = pygame.Rect(270, 100, 140, 45)
    merge_button = pygame.Rect(430, 100, 130, 45)
    reset_button = pygame.Rect(580, 100, 130, 45)

    array = create_random_array()

    # steps list stores all animation frames
    steps = []
    step_index = 0
    sorting_active = False
    last_step_time = 0
    delay = 80

    compare_indexes = []
    swap_indexes = []
    merge_indexes = []

    message = "Choose a sorting algorithm."

    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()

        # play sorting animation step by step
        if sorting_active:
            if current_time - last_step_time > delay:
                last_step_time = current_time

                if step_index < len(steps):
                    array, compare_indexes, swap_indexes, merge_indexes, message = steps[step_index]
                    step_index += 1
                else:
                    sorting_active = False
                    compare_indexes = []
                    swap_indexes = []
                    merge_indexes = []
                    message = "Sorting finished."

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Sorting Algorithms Module", title_font, BLACK, 350, 35)

        draw_button(screen, "Bubble Sort", bubble_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Selection Sort", selection_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Merge Sort", merge_button, button_font, YELLOW)
        draw_button(screen, "Reset Array", reset_button, button_font, LIGHT_GRAY)

        draw_array(
            screen,
            array,
            small_font,
            compare_indexes,
            swap_indexes,
            merge_indexes,
            message
        )

        draw_text(
            screen,
            "Red = Compare     Green = Swap     Yellow = Merge",
            small_font,
            BLACK,
            315,
            620
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    running = False

                elif help_button.collidepoint(mouse_pos):
                    show_help_page(screen, clock)

                elif bubble_button.collidepoint(mouse_pos):
                    if not sorting_active:
                        # generate bubble sort animation frames
                        steps = make_bubble_steps(array)
                        step_index = 0
                        sorting_active = True
                        last_step_time = pygame.time.get_ticks()
                        message = "Bubble Sort started."

                elif selection_button.collidepoint(mouse_pos):
                    if not sorting_active:
                        # generate selection sort animation frames
                        steps = make_selection_steps(array)
                        step_index = 0
                        sorting_active = True
                        last_step_time = pygame.time.get_ticks()
                        message = "Selection Sort started."

                elif merge_button.collidepoint(mouse_pos):
                    if not sorting_active:
                        # generate merge sort animation frames
                        steps = make_merge_steps(array)
                        step_index = 0
                        sorting_active = True
                        last_step_time = pygame.time.get_ticks()
                        message = "Merge Sort started."

                elif reset_button.collidepoint(mouse_pos):
                    if not sorting_active:
                        # reset only when no sorting is running
                        array = create_random_array()
                        steps = []
                        step_index = 0
                        compare_indexes = []
                        swap_indexes = []
                        merge_indexes = []
                        message = "New random array created."

        pygame.display.update()
        clock.tick(60)