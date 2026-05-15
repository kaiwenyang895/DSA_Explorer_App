import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
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


def draw_input_box(screen, input_box, input_text, input_active, font):
    if input_active:
        pygame.draw.rect(screen, LIGHT_BLUE, input_box)
    else:
        pygame.draw.rect(screen, WHITE, input_box)

    pygame.draw.rect(screen, BLACK, input_box, 2)

    if input_text == "":
        draw_text(screen, "type here", font, LIGHT_GRAY, input_box.x + 8, input_box.y + 8)
    else:
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 8, input_box.y + 8))


def handle_number_input(event, input_text):
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]

    else:
        if event.unicode.isdigit():
            input_text += event.unicode

        elif event.unicode == "-" and input_text == "":
            input_text += event.unicode

    return input_text


def get_value_from_input(input_text, auto_number):
    if input_text != "" and input_text != "-":
        value = int(input_text)
        return value, auto_number

    value = auto_number
    auto_number += 1

    return value, auto_number


def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def show_help_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 24)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Stack Page", title_font, BLACK, 365, 50)

        draw_text(screen, "1. Stack uses LIFO: Last In, First Out.", small_font, BLACK, 210, 130)
        draw_text(screen, "2. Type a number in the input box.", small_font, BLACK, 210, 170)
        draw_text(screen, "3. Click Push to add the number to the top of the stack.", small_font, BLACK, 210, 210)
        draw_text(screen, "4. Push animation: the block slides in from the right.", small_font, BLACK, 210, 250)
        draw_text(screen, "5. Click Pop to remove the top value from the stack.", small_font, BLACK, 210, 290)
        draw_text(screen, "6. Pop animation: the top block slides out to the right.", small_font, BLACK, 210, 330)
        draw_text(screen, "7. The yellow block shows the current top value.", small_font, BLACK, 210, 370)
        draw_text(screen, "8. Click Reset to clear the stack.", small_font, BLACK, 210, 410)

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


def draw_stack_blocks(
        screen,
        stack,
        font,
        stack_scroll,
        moving_active,
        moving_type,
        moving_value,
        moving_x,
        moving_y
):
    draw_text(screen, "Stack", font, BLACK, 515, 160)
    draw_text(screen, "LIFO: Last In, First Out", font, BLACK, 455, 190)

    x = 490
    y = 260
    box_width = 120
    box_height = 40
    gap = 5
    visible_count = 6

    if len(stack) == 0 and not moving_active:
        draw_text(screen, "Empty Stack", font, BLACK, 495, 330)

    stack_view = list(reversed(stack))
    visible_stack = stack_view[stack_scroll:stack_scroll + visible_count]

    for index, value in enumerate(visible_stack):
        # When pop animation is running, skip the top block.
        # The top block is drawn separately as the moving block.
        if moving_active and moving_type == "pop" and stack_scroll == 0 and index == 0:
            continue

        draw_index = index

        # When push animation is running, leave the top space for the moving block.
        if moving_active and moving_type == "push" and stack_scroll == 0:
            draw_index = index + 1

        rect = pygame.Rect(
            x,
            y + draw_index * (box_height + gap),
            box_width,
            box_height
        )

        if stack_scroll == 0 and index == 0 and not (moving_active and moving_type == "push"):
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        text_surface = font.render(str(value), True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Draw moving block for push or pop animation
    if moving_active:
        moving_rect = pygame.Rect(moving_x, moving_y, box_width, box_height)

        pygame.draw.rect(screen, YELLOW, moving_rect)
        pygame.draw.rect(screen, BLACK, moving_rect, 2)

        text_surface = font.render(str(moving_value), True, BLACK)
        text_rect = text_surface.get_rect(center=moving_rect.center)
        screen.blit(text_surface, text_rect)

    draw_text(screen, "Top", font, BLACK, 440, 270)


def run_stack_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    input_box = pygame.Rect(455, 115, 180, 35)

    push_button = pygame.Rect(390, 535, 120, 45)
    pop_button = pygame.Rect(535, 535, 120, 45)
    reset_button = pygame.Rect(680, 535, 120, 45)

    stack = []
    stack_scroll = 0
    auto_number = 1

    input_text = ""
    input_active = False

    message = "Type a number or leave it empty to use automatic numbers."

    # Stack drawing settings
    stack_x = 490
    stack_y = 260
    max_items = 8

    # Animation variables
    moving_active = False
    moving_type = None
    moving_value = None
    moving_x = 0
    moving_y = stack_y
    target_x = stack_x

    # Smaller = slower animation, bigger = faster animation
    speed = 10

    running = True

    while running:
        screen.fill(WHITE)

        max_stack_scroll = max(0, len(stack) - 6)
        stack_scroll = clamp(stack_scroll, 0, max_stack_scroll)

        # Push animation:
        # new block slides from right side into the top of the stack
        if moving_active and moving_type == "push":
            if moving_x > target_x:
                moving_x -= speed

                if moving_x < target_x:
                    moving_x = target_x

            else:
                stack.append(moving_value)
                stack_scroll = 0
                moving_active = False
                moving_type = None
                moving_value = None
                message = "Pushed value into the stack."

        # Pop animation:
        # top block slides out to the right side
        elif moving_active and moving_type == "pop":
            moving_x += speed

            if moving_x > screen_width + 100:
                if len(stack) > 0:
                    removed = stack.pop()
                    stack_scroll = 0
                    message = "Popped " + str(removed) + " from the stack."

                moving_active = False
                moving_type = None
                moving_value = None

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Stack Page", title_font, BLACK, 455, 45)

        draw_text(screen, "Input Number:", small_font, BLACK, 340, 123)
        draw_input_box(screen, input_box, input_text, input_active, small_font)

        draw_stack_blocks(
            screen,
            stack,
            small_font,
            stack_scroll,
            moving_active,
            moving_type,
            moving_value,
            moving_x,
            moving_y
        )

        draw_button(screen, "Push", push_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Pop", pop_button, button_font, LIGHT_RED)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_text(screen, message, small_font, BLACK, 310, 615)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if not moving_active:
                    stack_scroll -= event.y
                    stack_scroll = clamp(stack_scroll, 0, max_stack_scroll)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    else:
                        input_text = handle_number_input(event, input_text)

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

                elif push_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    elif len(stack) >= max_items:
                        message = "Stack display limit reached. Please pop or reset."

                    else:
                        value, auto_number = get_value_from_input(input_text, auto_number)

                        moving_value = value
                        moving_type = "push"
                        moving_active = True

                        # start from outside the right side of the screen
                        moving_x = screen_width + 80
                        moving_y = stack_y

                        # target position is the top of the stack
                        target_x = stack_x

                        input_text = ""
                        stack_scroll = 0

                        message = "Push animation started."

                elif pop_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    elif len(stack) > 0:
                        moving_value = stack[-1]
                        moving_type = "pop"
                        moving_active = True

                        # start from the top of the stack
                        moving_x = stack_x
                        moving_y = stack_y
                        stack_scroll = 0

                        message = "Pop animation started."

                    else:
                        message = "Stack is empty. Cannot pop."

                elif reset_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    else:
                        stack.clear()
                        stack_scroll = 0
                        auto_number = 1
                        input_text = ""
                        message = "Stack has been reset."

        pygame.display.update()
        clock.tick(60)