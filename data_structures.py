import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)

#This line defines a class called Node.

#Node means
#In a linked list,
# each piece of data is not stored individually in an array,
# but is placed in separate nodes.
class Node:
#When we create a new node, it runs automatically.
    def __init__(self, value):
        self.value = value
        self.next = None
#That is to say, when a new node is just created:
#value has a value
#next has not yet connected to others


#Linked list node
class LinkedList:
    def __init__(self):
        # start with nothing#
        # at first, the linked list is empty size= 0 hed = none
        self.head = None
        self.size = 0

#Insert a new node at the end of the linked list.
    def insert_end(self, value):
        new_node = Node(value)
#Create a new node. Check if the linked list is empty.
        # If the linked list is empty, make the new node the first node. Otherwise,
        #create a variable current, starting from the head node.
        if self.head is None:
            self.head = new_node
        else:
            #The meaning of current is: the node that is currently being checked.
            current = self.head

            while current.next is not None:
                current = current.next

            current.next = new_node

        #Increase the number of linked list nodes by 1
        self.size += 1

    def delete_head(self):
       #Determine whether the linked list is empty
        if self.head is None:
            return None
# remove the head one
        removed_value = self.head.value
        self.head = self.head.next
        self.size -= 1

        return removed_value

    def reverse(self):
        previous = None
        current = self.head
#This means that as long as current
# is not null, the loop continues. Reverse one node at a time.
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
 #The original current node points to the next node,
        # now it is changed to point to the previous one
        self.head = previous
# delete
    def clear(self):
        self.head = None
        self.size = 0

    def to_list(self):
        values = []
        current = self.head
#This to_list() is not a core operation of a linked list.
        # However, to_list() is very useful, especially since this assignment
        # requires testing screenshots / automated tests;
        # it can help check whether the linked list results are correct.
        # This is the result of my research.
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

#Control the scroll wheel to prevent scrolling out of the numeric range
def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value

#Draw a line and then draw a triangle to make an arrow
def draw_arrow(screen, start_pos, end_pos):

    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    arrow_x, arrow_y = end_pos

    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (arrow_x, arrow_y),
            (arrow_x - 8, arrow_y - 5),
            (arrow_x - 8, arrow_y + 5)
        ]
    )


def draw_stack(screen, stack, font, stack_scroll):
    draw_text(screen, "Stack", font, BLACK, 140, 115)
    #Last In, First Out
    draw_text(screen, "LIFO", font, BLACK, 145, 140)

    x = 110
    y = 180
    box_width = 100
    box_height = 35
    ## 3
    visible_count = 3

    if len(stack) == 0:
        draw_text(screen, "Empty", font, BLACK, 130, 220)

    stack_view = list(reversed(stack))
    visible_stack = stack_view[stack_scroll:stack_scroll + visible_count]

    for index, value in enumerate(visible_stack):
        rect = pygame.Rect(x, y + index * box_height, box_width, box_height)

        if stack_scroll == 0 and index == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, LIGHT_BLUE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        text_surface = font.render(str(value), True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    draw_text(screen, "Top", font, BLACK, 65, 185)


def draw_queue(screen, queue, font, queue_scroll):
    # draw queue title
    draw_text(screen, "Queue", font, BLACK, 580, 115)
    draw_text(screen, "FIFO", font, BLACK, 590, 140)

    x = 430
    y = 215
    box_width = 60
    box_height = 40
    visible_count = 6

    # show empty msg
    if len(queue) == 0:
        draw_text(screen, "Empty Queue", font, BLACK, 540, 220)

    # only show part of queue if too long
    visible_queue = queue[queue_scroll:queue_scroll + visible_count]

    for index, value in enumerate(visible_queue):
        rect = pygame.Rect(x + index * box_width, y, box_width, box_height)

        # first item is front
        if queue_scroll == 0 and index == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, LIGHT_GREEN, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        # draw value in box
        text_surface = font.render(str(value), True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    draw_text(screen, "Front", font, BLACK, 430, 185)
    draw_text(screen, "Rear", font, BLACK, 735, 185)


def draw_linked_list(screen, linked_list, font):
    # draw linked list title
    draw_text(screen, "Linked List", font, BLACK, 370, 330)
    draw_text(screen, "Each node points to the next node", font, BLACK, 295, 355)

    # convert linked list to normal list for drawing
    values = linked_list.to_list()

    if len(values) == 0:
        draw_text(screen, "Empty Linked List", font, BLACK, 350, 420)
        return

    start_x = 80
    y = 405
    node_width = 70
    node_height = 45
    gap = 30

    # only draw first 8 nodes
    for index, value in enumerate(values[:8]):
        x = start_x + index * (node_width + gap)

        node_rect = pygame.Rect(x, y, node_width, node_height)
        value_rect = pygame.Rect(x, y, 45, node_height)
        next_rect = pygame.Rect(x + 45, y, 25, node_height)

        # draw node box
        pygame.draw.rect(screen, ORANGE, node_rect)
        pygame.draw.rect(screen, BLACK, node_rect, 2)

        # split value and next part
        pygame.draw.line(
            screen,
            BLACK,
            (x + 45, y),
            (x + 45, y + node_height),
            2
        )

        # draw node value
        value_surface = font.render(str(value), True, BLACK)
        value_text_rect = value_surface.get_rect(center=value_rect.center)
        screen.blit(value_surface, value_text_rect)

        # draw n for next
        next_surface = font.render("n", True, BLACK)
        next_text_rect = next_surface.get_rect(center=next_rect.center)
        screen.blit(next_surface, next_text_rect)

        # draw arrow to next node
        if index < len(values[:8]) - 1:
            arrow_start = (x + node_width, y + node_height // 2)
            arrow_end = (x + node_width + gap - 5, y + node_height // 2)
            draw_arrow(screen, arrow_start, arrow_end)
        else:
            draw_text(screen, "None", font, BLACK, x + node_width + 8, y + 12)

    draw_text(screen, "head", font, BLACK, start_x, y - 25)


def run_data_structures_module(screen, clock):
    """
    Main function for the Data Structures module.
    This module visualises Stack, Queue, and Linked List.
    """
    # fonts
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    # data used in this page
    stack = []
    queue = []
    linked_list = LinkedList()

    # scroll pos
    stack_scroll = 0
    queue_scroll = 0

    # next numbers to add
    stack_next_number = 1
    queue_next_number = 1
    list_next_number = 1
    message = "Use the buttons to interact with Stack, Queue, and Linked List."

    # button rects
    back_button = pygame.Rect(25, 25, 95, 40)

    push_button = pygame.Rect(70, 300, 100, 40)
    pop_button = pygame.Rect(185, 300, 100, 40)

    enqueue_button = pygame.Rect(495, 300, 120, 40)
    dequeue_button = pygame.Rect(635, 300, 120, 40)

    insert_button = pygame.Rect(90, 535, 135, 40)
    delete_button = pygame.Rect(250, 535, 135, 40)
    reverse_button = pygame.Rect(410, 535, 135, 40)
    reset_button = pygame.Rect(620, 535, 100, 40)

    running = True

    while running:
        # clear page
        screen.fill(WHITE)

        # max scroll values
        max_stack_scroll = max(0, len(stack) - 3)
        max_queue_scroll = max(0, len(queue) - 3)

        stack_scroll = clamp(stack_scroll, 0, max_stack_scroll)
        queue_scroll = clamp(queue_scroll, 0, max_queue_scroll)

        # draw page title
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(
            screen,
            "Data Structures Module",
            title_font,
            BLACK,
            270,
            35
        )

        draw_text(
            screen,
            "Stack, Queue and Linked List visualisation",
            small_font,
            BLACK,
            275,
            75
        )

        # draw structures
        draw_stack(screen, stack, small_font, stack_scroll)
        draw_queue(screen, queue, small_font, queue_scroll)
        draw_linked_list(screen, linked_list, small_font)

        # draw buttons
        draw_button(screen, "Push", push_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Pop", pop_button, button_font, LIGHT_RED)

        draw_button(screen, "Enqueue", enqueue_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Dequeue", dequeue_button, button_font, LIGHT_RED)

        draw_button(screen, "Insert Node", insert_button, button_font, ORANGE)
        draw_button(screen, "Delete Head", delete_button, button_font, LIGHT_RED)
        draw_button(screen, "Reverse", reverse_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        # show msg
        draw_text(screen, message, small_font, BLACK, 80, 500)

        for event in pygame.event.get():
            # mouse wheel scroll
            if event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if mouse_x < 350 and mouse_y < 330:
                    stack_scroll -= event.y

                elif mouse_x > 350 and mouse_y < 330:
                    queue_scroll -= event.y

                stack_scroll = clamp(stack_scroll, 0, max_stack_scroll)
                queue_scroll = clamp(queue_scroll, 0, max_queue_scroll)

            # close window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    running = False

                # stack push
                elif push_button.collidepoint(mouse_pos):
                    stack.append(stack_next_number)
                    stack_scroll = 0
                    message = "Pushed " + str(stack_next_number) + " into the stack."
                    stack_next_number += 1

                # stack pop
                elif pop_button.collidepoint(mouse_pos):
                    if len(stack) > 0:
                        removed = stack.pop()
                        stack_scroll = 0
                        message = "Popped " + str(removed) + " from the stack."
                    else:
                        message = "Stack is empty. Cannot pop."

                # queue add
                elif enqueue_button.collidepoint(mouse_pos):
                    queue.append(queue_next_number)
                    message = "Enqueued " + str(queue_next_number) + " into the queue."
                    queue_next_number += 1

                # queue remove
                elif dequeue_button.collidepoint(mouse_pos):
                    if len(queue) > 0:
                        removed = queue.pop(0)
                        queue_scroll = 0
                        message = "Dequeued " + str(removed) + " from the queue."
                    else:
                        message = "Queue is empty. Cannot dequeue."

                # linked list insert
                elif insert_button.collidepoint(mouse_pos):
                    if linked_list.size < 8:
                        linked_list.insert_end(list_next_number)
                        message = "Inserted node " + str(list_next_number) + " at the end of the linked list."
                        list_next_number += 1
                    else:
                        message = "Linked list display limit reached. Please reset or delete nodes."

                # delete linked list head
                elif delete_button.collidepoint(mouse_pos):
                    removed = linked_list.delete_head()

                    if removed is None:
                        message = "Linked list is empty. Cannot delete."
                    else:
                        message = "Deleted head node " + str(removed) + " from the linked list."

                # reverse linked list
                elif reverse_button.collidepoint(mouse_pos):
                    linked_list.reverse()
                    message = "Linked list has been reversed."

                # reset all
                elif reset_button.collidepoint(mouse_pos):
                    stack.clear()
                    queue.clear()
                    linked_list.clear()

                    stack_scroll = 0
                    queue_scroll = 0

                    stack_next_number = 1
                    queue_next_number = 1
                    list_next_number = 1

                    message = "All data structures have been reset."


        pygame.display.update()
        clock.tick(60)