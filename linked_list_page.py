import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
ORANGE = (255, 204, 153)
YELLOW = (255, 255, 153)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_end(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head

            # move to the last node
            while current.next is not None:
                current = current.next

            current.next = new_node

        self.size += 1

    def insert_at_position(self, value, position):
        if position < 0 or position > self.size:
            return False

        new_node = Node(value)

        # insert before current head
        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            index = 0

            # stop at the node before target position
            while index < position - 1:
                current = current.next
                index += 1

            new_node.next = current.next
            current.next = new_node

        self.size += 1
        return True

    def delete_head(self):
        if self.head is None:
            return None

        removed_value = self.head.value
        self.head = self.head.next
        self.size -= 1

        return removed_value

    def delete_value(self, value):
        if self.head is None:
            return None

        if self.head.value == value:
            return self.delete_head()

        current = self.head

        # find the node before the value need delete
        while current.next is not None:
            if current.next.value == value:
                removed_value = current.next.value
                current.next = current.next.next
                self.size -= 1
                return removed_value

            current = current.next

        return None

    def reverse(self):
        previous = None
        current = self.head

        # reverse the next pointer one by one
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def clear(self):
        self.head = None
        self.size = 0

    def to_list(self):
        values = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        return values


def draw_text(screen, text, font, colour, x, y):
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_input_box(screen, input_box, input_text, active_field, field_name, font):
    if active_field == field_name:
        pygame.draw.rect(screen, LIGHT_BLUE, input_box)
    else:
        pygame.draw.rect(screen, WHITE, input_box)

    pygame.draw.rect(screen, BLACK, input_box, 2)

    if input_text == "":
        draw_text(screen, "type here", font, LIGHT_GRAY, input_box.x + 8, input_box.y + 8)
    else:
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 8, input_box.y + 8))


def handle_number_input(event, input_text, allow_minus):
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]

    else:
        if event.unicode.isdigit():
            input_text += event.unicode

        elif allow_minus and event.unicode == "-" and input_text == "":
            input_text += event.unicode

    return input_text


def get_value_from_input(input_text, auto_number):
    if input_text != "" and input_text != "-":
        value = int(input_text)
        return value, auto_number

    value = auto_number
    auto_number += 1

    return value, auto_number


def draw_arrow(screen, start_pos, end_pos):
    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    arrow_x, arrow_y = end_pos

    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (arrow_x, arrow_y),
            (arrow_x - 10, arrow_y - 6),
            (arrow_x - 10, arrow_y + 6)
        ]
    )


def get_node_positions(count, screen_width):
    positions = []
    y = 330
    gap = 95

    if count == 0:
        return positions

    total_width = (count - 1) * gap
    start_x = screen_width // 2 - total_width // 2

    for index in range(count):
        positions.append((start_x + index * gap, y))

    return positions


def draw_node_circle(screen, value, x, y, radius, font, colour):
    pygame.draw.circle(screen, colour, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x, y), radius, 2)

    text_surface = font.render(str(value), True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_linked_list_visual(screen, linked_list, font, highlight_index):
    draw_text(screen, "Linked List", font, BLACK, 505, 185)
    draw_text(screen, "Circle = Node     Arrow = next pointer", font, BLACK, 380, 215)

    values = linked_list.to_list()

    if len(values) == 0:
        draw_text(screen, "head -> None", font, BLACK, 485, 330)
        return

    radius = 28
    positions = get_node_positions(len(values), screen.get_width())

    draw_text(screen, "head", font, BLACK, positions[0][0] - 18, positions[0][1] - 70)
    pygame.draw.line(
        screen,
        BLACK,
        (positions[0][0], positions[0][1] - 45),
        (positions[0][0], positions[0][1] - radius),
        2
    )

    # arrows show the next pointers between nodes
    for index in range(len(values) - 1):
        start_x, start_y = positions[index]
        end_x, end_y = positions[index + 1]

        arrow_start = (start_x + radius, start_y)
        arrow_end = (end_x - radius, end_y)

        draw_arrow(screen, arrow_start, arrow_end)

    for index, value in enumerate(values):
        x, y = positions[index]

        if highlight_index == index:
            colour = YELLOW
        else:
            colour = ORANGE

        draw_node_circle(screen, value, x, y, radius, font, colour)

        index_surface = font.render("pos " + str(index), True, BLACK)
        screen.blit(index_surface, (x - 25, y + 45))

    last_x, last_y = positions[-1]
    draw_text(screen, "None", font, BLACK, last_x + 45, last_y - 10)


def draw_reverse_animation(screen, before_values, progress, font):
    draw_text(screen, "Reverse Animation", font, BLACK, 465, 185)
    draw_text(screen, "Nodes are moving to reversed positions.", font, BLACK, 375, 215)

    count = len(before_values)
    radius = 28

    if count == 0:
        return

    old_positions = get_node_positions(count, screen.get_width())
    new_positions = list(reversed(old_positions))

    # move nodes from old place to reversed place
    for index, value in enumerate(before_values):
        old_x, old_y = old_positions[index]
        new_x, new_y = new_positions[index]

        current_x = old_x + int((new_x - old_x) * progress)
        current_y = old_y + int((new_y - old_y) * progress)

        draw_node_circle(screen, value, current_x, current_y, radius, font, LIGHT_BLUE)

    draw_text(screen, "After animation, the next pointers will be reversed.", font, BLACK, 340, 430)


def show_help_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 23)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Linked List Page", title_font, BLACK, 330, 50)

        draw_text(screen, "1. A linked list is made of nodes.", small_font, BLACK, 180, 120)
        draw_text(screen, "2. Each node stores a value and points to the next node.", small_font, BLACK, 180, 155)
        draw_text(screen, "3. Type a value in the Value box.", small_font, BLACK, 180, 190)
        draw_text(screen, "4. Insert End adds the value to the end of the linked list.", small_font, BLACK, 180, 225)
        draw_text(screen, "5. Insert At Position uses the Position box. Position starts from 0.", small_font, BLACK, 180, 260)
        draw_text(screen, "6. Delete removes the first matching value. Empty value deletes head.", small_font, BLACK, 180, 295)
        draw_text(screen, "7. Traverse highlights nodes from head to tail.", small_font, BLACK, 180, 330)
        draw_text(screen, "8. Reverse reverses the linked list and shows animation.", small_font, BLACK, 180, 365)
        draw_text(screen, "9. Keyboard: A add end, I insert position, D delete, T traverse, R reverse, C clear.", small_font, BLACK, 180, 400)

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


def run_linked_list_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 23)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    value_input_box = pygame.Rect(380, 115, 160, 35)
    position_input_box = pygame.Rect(675, 115, 100, 35)

    insert_end_button = pygame.Rect(110, 535, 125, 45)
    insert_pos_button = pygame.Rect(250, 535, 150, 45)
    delete_button = pygame.Rect(415, 535, 115, 45)
    traverse_button = pygame.Rect(545, 535, 120, 45)
    reverse_button = pygame.Rect(680, 535, 120, 45)
    reset_button = pygame.Rect(815, 535, 110, 45)

    linked_list = LinkedList()
    auto_number = 1

    value_text = ""
    position_text = ""
    active_field = None

    message = "Type a value. Use Position for Insert At Position."

    max_nodes = 9

    traverse_active = False
    traverse_index = None
    last_traverse_time = 0

    reverse_active = False
    reverse_progress = 0
    reverse_before_values = []

    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()

        # highlight linked list nodes from head to tail
        if traverse_active and not reverse_active:
            if current_time - last_traverse_time > 600:
                last_traverse_time = current_time

                if traverse_index is None:
                    traverse_index = 0
                else:
                    traverse_index += 1

                if traverse_index >= linked_list.size:
                    traverse_active = False
                    traverse_index = None
                    message = "Traversal finished from head to tail."

        # play reverse animation before really reverse the list
        if reverse_active:
            reverse_progress += 0.025

            if reverse_progress >= 1:
                linked_list.reverse()
                reverse_active = False
                reverse_progress = 0
                reverse_before_values = []
                message = "Linked list has been reversed."

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Linked List Page", title_font, BLACK, 410, 45)

        draw_text(screen, "Value:", small_font, BLACK, 325, 123)
        draw_input_box(screen, value_input_box, value_text, active_field, "value", small_font)

        draw_text(screen, "Position:", small_font, BLACK, 600, 123)
        draw_input_box(screen, position_input_box, position_text, active_field, "position", small_font)

        if reverse_active:
            draw_reverse_animation(screen, reverse_before_values, reverse_progress, small_font)
        else:
            draw_linked_list_visual(screen, linked_list, small_font, traverse_index)

        draw_button(screen, "Insert End", insert_end_button, button_font, ORANGE)
        draw_button(screen, "Insert At Pos", insert_pos_button, button_font, ORANGE)
        draw_button(screen, "Delete", delete_button, button_font, LIGHT_RED)
        draw_button(screen, "Traverse", traverse_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Reverse", reverse_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_text(screen, message, small_font, BLACK, 260, 615)



        for event in pygame.event.get():
            action = None

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active_field == "value":
                    if event.key == pygame.K_RETURN:
                        active_field = None
                    else:
                        value_text = handle_number_input(event, value_text, True)

                elif active_field == "position":
                    if event.key == pygame.K_RETURN:
                        active_field = None
                    else:
                        position_text = handle_number_input(event, position_text, False)

                else:
                    if event.key == pygame.K_a:
                        action = "insert_end"

                    elif event.key == pygame.K_i:
                        action = "insert_position"

                    elif event.key == pygame.K_d:
                        action = "delete"

                    elif event.key == pygame.K_t:
                        action = "traverse"

                    elif event.key == pygame.K_r:
                        action = "reverse"

                    elif event.key == pygame.K_c:
                        action = "reset"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if value_input_box.collidepoint(mouse_pos):
                    active_field = "value"

                elif position_input_box.collidepoint(mouse_pos):
                    active_field = "position"

                else:
                    active_field = None

                if back_button.collidepoint(mouse_pos):
                    running = False

                elif help_button.collidepoint(mouse_pos):
                    show_help_page(screen, clock)

                elif insert_end_button.collidepoint(mouse_pos):
                    action = "insert_end"

                elif insert_pos_button.collidepoint(mouse_pos):
                    action = "insert_position"

                elif delete_button.collidepoint(mouse_pos):
                    action = "delete"

                elif traverse_button.collidepoint(mouse_pos):
                    action = "traverse"

                elif reverse_button.collidepoint(mouse_pos):
                    action = "reverse"

                elif reset_button.collidepoint(mouse_pos):
                    action = "reset"

            if action == "insert_end":
                if reverse_active:
                    message = "Please wait for the reverse animation to finish."

                elif linked_list.size >= max_nodes:
                    message = "Linked list display limit reached. Please delete or reset."

                else:
                    value, auto_number = get_value_from_input(value_text, auto_number)
                    linked_list.insert_end(value)

                    value_text = ""
                    traverse_active = False
                    traverse_index = None

                    message = "Inserted " + str(value) + " at the end."

            elif action == "insert_position":
                if reverse_active:
                    message = "Please wait for the reverse animation to finish."

                elif linked_list.size >= max_nodes:
                    message = "Linked list display limit reached. Please delete or reset."

                elif position_text == "":
                    message = "Please type a position first."

                else:
                    position = int(position_text)

                    if position < 0 or position > linked_list.size:
                        message = "Invalid position. Use 0 to " + str(linked_list.size) + "."

                    else:
                        value, auto_number = get_value_from_input(value_text, auto_number)
                        linked_list.insert_at_position(value, position)

                        value_text = ""
                        position_text = ""
                        traverse_active = False
                        traverse_index = None

                        message = "Inserted " + str(value) + " at position " + str(position) + "."

            elif action == "delete":
                if reverse_active:
                    message = "Please wait for the reverse animation to finish."

                elif linked_list.size == 0:
                    message = "Linked list is empty. Cannot delete."

                else:
                    if value_text != "" and value_text != "-":
                        value = int(value_text)
                        removed = linked_list.delete_value(value)

                        if removed is None:
                            message = str(value) + " was not found in the linked list."
                        else:
                            message = "Deleted value " + str(removed) + " from the linked list."

                        value_text = ""

                    else:
                        removed = linked_list.delete_head()
                        message = "Deleted head node " + str(removed) + "."

                    traverse_active = False
                    traverse_index = None

            elif action == "traverse":
                if reverse_active:
                    message = "Please wait for the reverse animation to finish."

                elif linked_list.size == 0:
                    message = "Linked list is empty. Cannot traverse."

                else:
                    traverse_active = True
                    traverse_index = 0
                    last_traverse_time = pygame.time.get_ticks()
                    message = "Traversing from head to tail."

            elif action == "reverse":
                if reverse_active:
                    message = "Reverse animation is already running."

                elif linked_list.size <= 1:
                    message = "Need at least two nodes to reverse."

                else:
                    traverse_active = False
                    traverse_index = None

                    reverse_before_values = linked_list.to_list()
                    reverse_progress = 0
                    reverse_active = True

                    message = "Reverse animation started."

            elif action == "reset":
                if reverse_active:
                    message = "Please wait for the reverse animation to finish."

                else:
                    linked_list.clear()
                    auto_number = 1

                    value_text = ""
                    position_text = ""

                    traverse_active = False
                    traverse_index = None

                    message = "Linked list has been reset."

        pygame.display.update()
        clock.tick(60)