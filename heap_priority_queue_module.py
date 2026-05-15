import pygame
import sys
import math


# colours used in this heap page
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)


def draw_text(screen, text, font, colour, x, y):
    # draw text to screen
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # draw button box
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # put button text in center
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_input_box(screen, input_box, input_text, input_active, font):
    # active input box use blue colour
    if input_active:
        pygame.draw.rect(screen, LIGHT_BLUE, input_box)
    else:
        pygame.draw.rect(screen, WHITE, input_box)

    pygame.draw.rect(screen, BLACK, input_box, 2)

    # show hint text if nothing typed
    if input_text == "":
        draw_text(screen, "type here", font, LIGHT_GRAY, input_box.x + 8, input_box.y + 8)
    else:
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 8, input_box.y + 8))


def handle_number_input(event, input_text):
    # allow delete number
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]

    else:
        # only number can type here
        if event.unicode.isdigit():
            input_text += event.unicode

    return input_text


def handle_text_input(event, input_text):
    # remove last char
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]

    else:
        # limit text length, so it not too long
        if len(input_text) < 20 and event.unicode != "":
            input_text += event.unicode

    return input_text


def heapify_up(heap, index):
    # move new item up if priority is smaller
    highlight_indices = []

    while index > 0:
        parent = (index - 1) // 2

        if heap[parent][0] > heap[index][0]:
            heap[parent], heap[index] = heap[index], heap[parent]
            highlight_indices = [parent, index]
            index = parent
        else:
            break

    return highlight_indices


def heapify_down(heap, index):
    # move item down after extract min
    highlight_indices = []

    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(heap) and heap[left][0] < heap[smallest][0]:
            smallest = left

        if right < len(heap) and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            highlight_indices = [index, smallest]
            index = smallest

        else:
            break

    return highlight_indices


def heap_insert(heap, event_item):
    # add item then fix heap order
    heap.append(event_item)
    return heapify_up(heap, len(heap) - 1)


def heap_extract_min(heap):
    # take the smallest time event out
    if len(heap) == 0:
        return None, []

    min_event = heap[0]

    if len(heap) == 1:
        heap.pop()
        return min_event, []

    heap[0] = heap[-1]
    heap.pop()

    highlight_indices = heapify_down(heap, 0)

    return min_event, highlight_indices


def get_heap_positions(heap, screen_width):
    # calculate where every heap node should draw
    positions = []

    if len(heap) == 0:
        return positions

    for index in range(len(heap)):
        level = int(math.floor(math.log2(index + 1)))
        index_in_level = index - (2 ** level - 1)

        gap = screen_width // (2 ** level + 1)
        x = gap * (index_in_level + 1)
        y = 250 + level * 80

        positions.append((x, y))

    return positions


def draw_heap(screen, heap, font, highlight_indices):
    # draw heap as tree view
    positions = get_heap_positions(heap, screen.get_width())

    # draw lines first
    for index in range(len(heap)):
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(heap):
            pygame.draw.line(screen, BLACK, positions[index], positions[left], 2)

        if right < len(heap):
            pygame.draw.line(screen, BLACK, positions[index], positions[right], 2)

    # draw each heap node
    for index, event_item in enumerate(heap):
        event_time = event_item[0]
        description = event_item[2]

        x, y = positions[index]

        if index in highlight_indices:
            colour = YELLOW
        else:
            colour = LIGHT_BLUE

        pygame.draw.circle(screen, colour, (x, y), 26)
        pygame.draw.circle(screen, BLACK, (x, y), 26, 2)

        text_surface = font.render(str(event_time), True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

        small_text = font.render(description[:10], True, BLACK)
        screen.blit(small_text, (x - 35, y + 35))


def draw_upcoming_events(screen, heap, font):
    # show sorted event list on right side
    start_x = screen.get_width() - 190

    draw_text(screen, "Upcoming Events:", font, BLACK, start_x, 220)

    sorted_events = sorted(heap, key=lambda item: item[0])

    y = 255

    for item in sorted_events[:8]:
        event_time = item[0]
        description = item[2]

        draw_text(
            screen,
            "T" + str(event_time) + ": " + description,
            font,
            BLACK,
            start_x,
            y
        )

        y += 30


def show_help_page(screen, clock):
    # help page for user guide
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 23)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Heap Priority Queue", title_font, BLACK, 300, 50)

        draw_text(screen, "1. This page simulates event scheduling with a min-heap.", small_font, BLACK, 180, 130)
        draw_text(screen, "2. Smaller time value means higher priority.", small_font, BLACK, 180, 170)
        draw_text(screen, "3. Type event time and description, then click Add Event.", small_font, BLACK, 180, 210)
        draw_text(screen, "4. Add Sample adds an automatic example event.", small_font, BLACK, 180, 250)
        draw_text(screen, "5. Process Next extracts one earliest event.", small_font, BLACK, 180, 290)
        draw_text(screen, "6. Run All automatically processes all events by time.", small_font, BLACK, 180, 330)
        draw_text(screen, "7. Upcoming Events shows events sorted by time.", small_font, BLACK, 180, 370)
        draw_text(screen, "8. Reset clears the priority queue.", small_font, BLACK, 180, 410)

        # check help page events
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


def run_heap_priority_queue_module(screen, clock):
    # main heap priority queue page
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 21)
    small_font = pygame.font.SysFont(None, 21)

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # top buttons
    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    # input boxes
    time_input_box = pygame.Rect(325, 95, 120, 35)
    desc_input_box = pygame.Rect(580, 95, 220, 35)

    # action buttons
    add_button = pygame.Rect(120, 150, 105, 42)
    sample_button = pygame.Rect(240, 150, 115, 42)
    process_button = pygame.Rect(370, 150, 125, 42)
    run_all_button = pygame.Rect(510, 150, 100, 42)
    reset_button = pygame.Rect(625, 150, 100, 42)

    # heap data
    heap = []
    counter = 0
    sample_index = 0

    # sample events for quick demo
    sample_events = [
        (2, "Mail"),
        (5, "Parcel"),
        (8, "Close"),
        (1, "Call"),
        (7, "Report"),
        (3, "Staff")
    ]

    time_text = ""
    desc_text = ""
    active_input = None

    highlight_indices = []

    # auto run setting
    auto_running = False
    auto_last_time = 0
    auto_delay = 700

    message = "Add events with time and description."
    processed_message = "Processed Event: None"

    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()

        # process events automatically by time order
        if auto_running:
            if current_time - auto_last_time > auto_delay:
                min_event, highlight_indices = heap_extract_min(heap)
                auto_last_time = current_time

                if min_event is None:
                    auto_running = False
                    message = "All events have been processed."
                    processed_message = "Processed Event: None"

                else:
                    processed_message = (
                        "Processed Event: Time "
                        + str(min_event[0])
                        + " - "
                        + min_event[2]
                    )

                    if len(heap) == 0:
                        auto_running = False
                        message = "Run All completed."
                    else:
                        message = "Run All processing events by earliest time."

        # draw top area
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Heap Priority Queue Module", title_font, BLACK, 330, 35)

        draw_text(screen, "Time:", small_font, BLACK, 270, 103)
        draw_input_box(screen, time_input_box, time_text, active_input == "time", small_font)

        draw_text(screen, "Description:", small_font, BLACK, 480, 103)
        draw_input_box(screen, desc_input_box, desc_text, active_input == "desc", small_font)

        draw_button(screen, "Add Event", add_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Add Sample", sample_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Process Next", process_button, button_font, ORANGE)
        draw_button(screen, "Run All", run_all_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Min-Heap Tree", small_font, BLACK, 485, 210)

        # draw heap or empty message
        if len(heap) == 0:
            draw_text(screen, "Heap is empty.", small_font, BLACK, 480, 350)
        else:
            draw_heap(screen, heap, small_font, highlight_indices)

        draw_upcoming_events(screen, heap, small_font)

        draw_text(screen, message, small_font, BLACK, 220, screen_height - 70)
        draw_text(screen, processed_message, small_font, BLACK, 220, screen_height - 40)

        # handle keyboard and mouse input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active_input == "time":
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    else:
                        time_text = handle_number_input(event, time_text)

                elif active_input == "desc":
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    else:
                        desc_text = handle_text_input(event, desc_text)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # choose which input box is active
                if time_input_box.collidepoint(mouse_pos):
                    active_input = "time"

                elif desc_input_box.collidepoint(mouse_pos):
                    active_input = "desc"

                else:
                    active_input = None

                if back_button.collidepoint(mouse_pos):
                    running = False

                elif help_button.collidepoint(mouse_pos):
                    show_help_page(screen, clock)

                elif add_button.collidepoint(mouse_pos):
                    auto_running = False

                    if time_text == "":
                        message = "Please type an event time first."

                    else:
                        event_time = int(time_text)

                        if desc_text == "":
                            description = "Event " + str(counter + 1)
                        else:
                            description = desc_text

                        # tuple save time, counter and description
                        event_item = (event_time, counter, description)
                        counter += 1

                        highlight_indices = heap_insert(heap, event_item)

                        time_text = ""
                        desc_text = ""

                        message = "Added event: " + description + " at time " + str(event_time)

                elif sample_button.collidepoint(mouse_pos):
                    auto_running = False

                    sample = sample_events[sample_index % len(sample_events)]
                    sample_index += 1

                    event_time = sample[0]
                    description = sample[1]

                    event_item = (event_time, counter, description)
                    counter += 1

                    highlight_indices = heap_insert(heap, event_item)

                    message = "Added sample event: " + description

                elif process_button.collidepoint(mouse_pos):
                    auto_running = False

                    # process one earliest event
                    min_event, highlight_indices = heap_extract_min(heap)

                    if min_event is None:
                        message = "Priority queue is empty."
                        processed_message = "Processed Event: None"

                    else:
                        processed_message = (
                            "Processed Event: Time "
                            + str(min_event[0])
                            + " - "
                            + min_event[2]
                        )

                        message = "Earliest event has been processed."

                elif run_all_button.collidepoint(mouse_pos):
                    # start automatic processing
                    if len(heap) == 0:
                        message = "Priority queue is empty."
                        processed_message = "Processed Event: None"

                    else:
                        auto_running = True
                        auto_last_time = pygame.time.get_ticks() - auto_delay
                        message = "Run All started."

                elif reset_button.collidepoint(mouse_pos):
                    # clear everything back to start
                    heap.clear()
                    counter = 0
                    sample_index = 0
                    time_text = ""
                    desc_text = ""
                    highlight_indices = []

                    auto_running = False
                    auto_last_time = 0

                    message = "Priority queue has been reset."
                    processed_message = "Processed Event: None"

        pygame.display.update()
        clock.tick(60)


def run_heap_module(screen, clock):
    # another name for running this module
    run_heap_priority_queue_module(screen, clock)