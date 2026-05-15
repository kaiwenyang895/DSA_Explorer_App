import pygame
import sys


# colours for this page
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)


def draw_text(screen, text, font, colour, x, y):
    # draw text on screen
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # draw button box
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # put text in button center
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_input_box(screen, input_box, input_text, input_active, font):
    # active input box is blue
    if input_active:
        pygame.draw.rect(screen, LIGHT_BLUE, input_box)
    else:
        pygame.draw.rect(screen, WHITE, input_box)

    pygame.draw.rect(screen, BLACK, input_box, 2)

    # show example when no input
    if input_text == "":
        draw_text(screen, "example: 7 3 10", font, LIGHT_GRAY, input_box.x + 8, input_box.y + 8)
    else:
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 8, input_box.y + 8))


def handle_target_input(event, input_text):
    # handle typing target numbers
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]

    else:
        # allow numbers, minus sign, space and comma
        if event.unicode.isdigit():
            input_text += event.unicode

        elif event.unicode == "-":
            input_text += event.unicode

        elif event.unicode == " ":
            input_text += event.unicode

        elif event.unicode == ",":
            input_text += event.unicode

    return input_text


def parse_targets(input_text):
    # allow input like: 7 3 10
    # also allow input like: 7,3,10
    cleaned_text = input_text.replace(",", " ")
    parts = cleaned_text.split()

    if len(parts) == 0:
        return None

    targets = []

    # change text parts into int numbers
    for part in parts:
        try:
            targets.append(int(part))
        except ValueError:
            return None

    return targets


def show_help_page(screen, clock):
    # help page tell user how to use it
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 24)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Linear Search Page", title_font, BLACK, 320, 50)

        draw_text(screen, "1. Linear search checks values one by one from left to right.", small_font, BLACK, 190, 130)
        draw_text(screen, "2. You can type one target number, such as 7.", small_font, BLACK, 190, 170)
        draw_text(screen, "3. You can also type multiple targets, such as 7 3 10.", small_font, BLACK, 190, 210)
        draw_text(screen, "4. Click Search to start the visual search.", small_font, BLACK, 190, 250)
        draw_text(screen, "5. The red cell is the value currently being checked.", small_font, BLACK, 190, 290)
        draw_text(screen, "6. The green cell means the target value is found.", small_font, BLACK, 190, 330)
        draw_text(screen, "7. Comparisons shows how many checks were made for the current target.", small_font, BLACK, 190, 370)
        draw_text(screen, "8. The program will search each target one after another.", small_font, BLACK, 190, 410)
        draw_text(screen, "9. Click Reset to clear the search result.", small_font, BLACK, 190, 450)

        # help page event check
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


def draw_linear_search_grid(screen, numbers, font, search_index, found_index, searched_until):
    # draw number cells for linear search
    start_x = 170
    y = 270
    cell_width = 75
    cell_height = 65

    for index, number in enumerate(numbers):
        rect = pygame.Rect(start_x + index * cell_width, y, cell_width - 5, cell_height)

        # choose cell colour by search status
        if found_index == index:
            colour = LIGHT_GREEN

        elif search_index == index:
            colour = LIGHT_RED

        elif index < searched_until:
            colour = LIGHT_GRAY

        else:
            colour = WHITE

        pygame.draw.rect(screen, colour, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text_surface = font.render(str(number), True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        index_text = font.render(str(index), True, BLACK)
        screen.blit(index_text, (rect.x + 25, rect.y + 75))


def run_linear_search_page(screen, clock):
    # main linear search page
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    input_box = pygame.Rect(455, 115, 220, 35)

    search_button = pygame.Rect(390, 535, 120, 45)
    reset_button = pygame.Rect(535, 535, 120, 45)

    # sample number list
    numbers = [5, 3, 9, 1, 7, 4, 8, 2, 6, 10]

    input_text = ""
    input_active = False

    targets = []
    target_position = 0
    current_target = None

    search_index = None
    found_index = None
    searched_until = 0

    comparisons = 0
    total_comparisons = 0

    searching = False
    waiting_next = False

    last_step_time = 0
    next_start_time = 0

    results = []

    message = "Type one or more target numbers, like 7 3 10, then click Search."

    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()

        # wait a short time, then start next target search
        if waiting_next:
            if current_time - next_start_time > 900:
                target_position += 1

                if target_position < len(targets):
                    current_target = targets[target_position]
                    search_index = 0
                    found_index = None
                    searched_until = 0
                    comparisons = 0
                    searching = True
                    waiting_next = False
                    last_step_time = pygame.time.get_ticks()
                    message = "Searching for " + str(current_target) + "..."

                else:
                    waiting_next = False
                    searching = False
                    current_target = None
                    search_index = None
                    message = "All target searches finished."

        # searching animation
        if searching:
            if current_time - last_step_time > 500:
                last_step_time = current_time

                if search_index < len(numbers):
                    comparisons += 1
                    total_comparisons += 1

                    # check current cell value
                    if numbers[search_index] == current_target:
                        found_index = search_index
                        searched_until = search_index + 1
                        searching = False

                        result_text = (
                            str(current_target)
                            + " found at index "
                            + str(found_index)
                            + " with "
                            + str(comparisons)
                            + " comparisons."
                        )

                        results.append(result_text)

                        message = (
                            "Found "
                            + str(current_target)
                            + " at index "
                            + str(found_index)
                            + "."
                        )

                        waiting_next = True
                        next_start_time = pygame.time.get_ticks()

                    else:
                        search_index += 1
                        searched_until = search_index

                # target not found after checking all numbers
                if search_index >= len(numbers) and found_index is None:
                    searching = False
                    search_index = None

                    result_text = (
                        str(current_target)
                        + " was not found with "
                        + str(comparisons)
                        + " comparisons."
                    )

                    results.append(result_text)

                    message = str(current_target) + " was not found."

                    waiting_next = True
                    next_start_time = pygame.time.get_ticks()

        # draw page UI
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Linear Search Page", title_font, BLACK, 390, 45)

        draw_text(screen, "Target Numbers:", small_font, BLACK, 320, 123)
        draw_input_box(screen, input_box, input_text, input_active, small_font)

        draw_text(screen, "Numbers:", small_font, BLACK, 170, 230)

        draw_linear_search_grid(
            screen,
            numbers,
            small_font,
            search_index,
            found_index,
            searched_until
        )

        draw_text(screen, "Index numbers are shown below each cell.", small_font, BLACK, 380, 380)

        if current_target is None:
            draw_text(screen, "Current Target: None", small_font, BLACK, 430, 420)
        else:
            draw_text(screen, "Current Target: " + str(current_target), small_font, BLACK, 430, 420)

        if len(targets) == 0:
            draw_text(screen, "Target Progress: 0 / 0", small_font, BLACK, 430, 450)
        else:
            draw_text(
                screen,
                "Target Progress: " + str(target_position + 1) + " / " + str(len(targets)),
                small_font,
                BLACK,
                430,
                450
            )

        draw_text(screen, "Comparisons: " + str(comparisons), small_font, BLACK, 430, 480)
        draw_text(screen, "Total Comparisons: " + str(total_comparisons), small_font, BLACK, 430, 510)

        draw_button(screen, "Search", search_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_text(screen, message, small_font, BLACK, 270, 615)

        # show last few results
        result_y = 160
        draw_text(screen, "Search Results:", small_font, BLACK, 760, 120)

        recent_results = results[-5:]

        for result in recent_results:
            draw_text(screen, result, small_font, BLACK, 760, result_y)
            result_y += 30

        # handle keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    else:
                        input_text = handle_target_input(event, input_text)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if input_box.collidepoint(mouse_pos):
                    input_active = True
                else:
                    input_active = False

                if back_button.collidepoint(mouse_pos):
                    running = False

                elif help_button.collidepoint(mouse_pos):
                    show_help_page(screen, clock)

                elif search_button.collidepoint(mouse_pos):
                    parsed_targets = parse_targets(input_text)

                    if parsed_targets is None:
                        message = "Please type one or more valid target numbers."
                    else:
                        # start new searching process
                        targets = parsed_targets
                        target_position = 0
                        current_target = targets[target_position]

                        search_index = 0
                        found_index = None
                        searched_until = 0

                        comparisons = 0
                        total_comparisons = 0

                        searching = True
                        waiting_next = False

                        results = []

                        last_step_time = pygame.time.get_ticks()

                        message = "Searching for " + str(current_target) + "..."

                elif reset_button.collidepoint(mouse_pos):
                    # reset all search data
                    input_text = ""

                    targets = []
                    target_position = 0
                    current_target = None

                    search_index = None
                    found_index = None
                    searched_until = 0

                    comparisons = 0
                    total_comparisons = 0

                    searching = False
                    waiting_next = False

                    results = []

                    message = "Search has been reset."

        pygame.display.update()
        clock.tick(60)