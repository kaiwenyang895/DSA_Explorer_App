import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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


def show_help_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 24)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Queue Page", title_font, BLACK, 365, 50)

        draw_text(screen, "1. Queue uses FIFO: First In, First Out.", small_font, BLACK, 210, 130)
        draw_text(screen, "2. Type a number in the input box.", small_font, BLACK, 210, 170)
        draw_text(screen, "3. Click Enqueue to add the number to the rear.", small_font, BLACK, 210, 210)
        draw_text(screen, "4. Click Dequeue to remove the front value.", small_font, BLACK, 210, 250)
        draw_text(screen, "5. Enqueue animation: block slides in from the right.", small_font, BLACK, 210, 290)
        draw_text(screen, "6. Dequeue animation: front block slides out to the left.", small_font, BLACK, 210, 330)
        draw_text(screen, "7. The yellow block shows the current front value.", small_font, BLACK, 210, 370)
        draw_text(screen, "8. Click Reset to clear the queue.", small_font, BLACK, 210, 410)

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


def draw_queue_blocks(
        screen,
        queue,
        font,
        moving_active,
        moving_type,
        moving_value,
        moving_x,
        moving_y
):
    start_x = 260
    y = 300
    box_width = 75
    box_height = 45
    gap = 8

    for index, value in enumerate(queue):
        # When dequeue animation is running,
        # skip the first block because it is moving out separately.
        if moving_active and moving_type == "dequeue" and index == 0:
            continue

        x = start_x + index * (box_width + gap)
        rect = pygame.Rect(x, y, box_width, box_height)

        if index == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, LIGHT_GREEN, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        text_surface = font.render(str(value), True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Draw the moving block
    if moving_active:
        moving_rect = pygame.Rect(moving_x, moving_y, box_width, box_height)

        if moving_type == "dequeue":
            pygame.draw.rect(screen, YELLOW, moving_rect)
        else:
            pygame.draw.rect(screen, LIGHT_GREEN, moving_rect)

        pygame.draw.rect(screen, BLACK, moving_rect, 2)

        text_surface = font.render(str(moving_value), True, BLACK)
        text_rect = text_surface.get_rect(center=moving_rect.center)
        screen.blit(text_surface, text_rect)

    draw_text(screen, "Front", font, BLACK, start_x, y - 35)
    draw_text(screen, "Rear", font, BLACK, start_x + 6 * (box_width + gap), y - 35)


def run_queue_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    input_box = pygame.Rect(455, 115, 180, 35)

    enqueue_button = pygame.Rect(350, 535, 130, 45)
    dequeue_button = pygame.Rect(505, 535, 130, 45)
    reset_button = pygame.Rect(660, 535, 120, 45)

    queue = []
    auto_number = 1

    input_text = ""
    input_active = False

    message = "Type a number or leave it empty to use automatic numbers."

    # Queue drawing settings
    start_x = 260
    y = 300
    box_width = 75
    gap = 8
    max_items = 7

    # Animation variables
    moving_active = False
    moving_type = None
    moving_value = None
    moving_x = 0
    moving_y = y
    target_x = 0

    # Smaller = slower animation, bigger = faster animation
    speed = 10

    running = True

    while running:
        screen.fill(WHITE)

        # Enqueue animation:
        # block slides from right side to the rear position
        if moving_active and moving_type == "enqueue":
            if moving_x > target_x:
                moving_x -= speed

                if moving_x < target_x:
                    moving_x = target_x

            else:
                queue.append(moving_value)
                moving_active = False
                moving_type = None
                moving_value = None
                message = "Enqueued value into the queue."

        # Dequeue animation:
        # front block slides out to the left side
        elif moving_active and moving_type == "dequeue":
            moving_x -= speed

            if moving_x < -100:
                if len(queue) > 0:
                    removed = queue.pop(0)
                    message = "Dequeued " + str(removed) + " from the queue."

                moving_active = False
                moving_type = None
                moving_value = None

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Queue Page", title_font, BLACK, 455, 45)

        draw_text(screen, "Input Number:", small_font, BLACK, 340, 123)
        draw_input_box(screen, input_box, input_text, input_active, small_font)

        draw_text(screen, "Queue Visualization", small_font, BLACK, 455, 200)
        draw_text(screen, "FIFO: First In, First Out", small_font, BLACK, 435, 230)

        if len(queue) == 0 and not moving_active:
            draw_text(screen, "Empty Queue", small_font, BLACK, 485, 320)

        draw_queue_blocks(
            screen,
            queue,
            small_font,
            moving_active,
            moving_type,
            moving_value,
            moving_x,
            moving_y
        )

        draw_button(screen, "Enqueue", enqueue_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Dequeue", dequeue_button, button_font, LIGHT_RED)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_text(screen, message, small_font, BLACK, 300, 615)

        for event in pygame.event.get():
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

                elif enqueue_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    elif len(queue) >= max_items:
                        message = "Queue display limit reached. Please dequeue or reset."

                    else:
                        value, auto_number = get_value_from_input(input_text, auto_number)

                        moving_value = value
                        moving_type = "enqueue"
                        moving_active = True

                        # start from outside the right side of the screen
                        moving_x = screen_width + 80
                        moving_y = y

                        # target position is the rear of the queue
                        target_x = start_x + len(queue) * (box_width + gap)

                        input_text = ""

                        message = "Enqueue animation started."

                elif dequeue_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    elif len(queue) > 0:
                        moving_value = queue[0]
                        moving_type = "dequeue"
                        moving_active = True

                        # start from the front of the queue
                        moving_x = start_x
                        moving_y = y

                        message = "Dequeue animation started."

                    else:
                        message = "Queue is empty. Cannot dequeue."

                elif reset_button.collidepoint(mouse_pos):
                    if moving_active:
                        message = "Please wait for the animation to finish."

                    else:
                        queue.clear()
                        auto_number = 1
                        input_text = ""
                        message = "Queue has been reset."

        pygame.display.update()
        clock.tick(60)