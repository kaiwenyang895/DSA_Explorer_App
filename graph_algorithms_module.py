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


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        # insert value by following BST rule
        def insert_recursive(node, value):
            if node is None:
                return BSTNode(value)

            if value < node.value:
                node.left = insert_recursive(node.left, value)

            elif value > node.value:
                node.right = insert_recursive(node.right, value)

            return node

        self.root = insert_recursive(self.root, value)

    def inorder(self):
        result = []

        # left, root, right
        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result

    def preorder(self):
        result = []

        # root, left, right
        def visit(node):
            if node is not None:
                result.append(node.value)
                visit(node.left)
                visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        result = []

        # left, right, root
        def visit(node):
            if node is not None:
                visit(node.left)
                visit(node.right)
                result.append(node.value)

        visit(self.root)
        return result

    def search_path(self, value):
        # save path so UI can highlight it
        path = []
        current = self.root

        while current is not None:
            path.append(current.value)

            if value == current.value:
                return path, True

            elif value < current.value:
                current = current.left

            else:
                current = current.right

        return path, False

    def delete(self, value):
        def find_min(node):
            current = node

            # find smallest value in right subtree
            while current.left is not None:
                current = current.left

            return current

        def delete_recursive(node, value):
            if node is None:
                return node, False

            if value < node.value:
                node.left, deleted = delete_recursive(node.left, value)
                return node, deleted

            elif value > node.value:
                node.right, deleted = delete_recursive(node.right, value)
                return node, deleted

            else:
                # no child or one child
                if node.left is None:
                    return node.right, True

                if node.right is None:
                    return node.left, True

                # two children, use right subtree minimum
                successor = find_min(node.right)
                node.value = successor.value
                node.right, deleted = delete_recursive(node.right, successor.value)

                return node, True

        self.root, deleted = delete_recursive(self.root, value)
        return deleted


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


def draw_node(screen, x, y, value, font, highlight):
    radius = 22

    if highlight:
        colour = YELLOW
    else:
        colour = LIGHT_BLUE

    pygame.draw.circle(screen, colour, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x, y), radius, 2)

    text_surface = font.render(str(value), True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_edge(screen, start_pos, end_pos):
    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)


def draw_tree(screen, node, x, y, x_offset, font, highlight_values, parent_pos=None):
    if node is None:
        return

    # draw line from parent node to this node
    if parent_pos is not None:
        draw_edge(screen, parent_pos, (x, y))

    highlight = node.value in highlight_values

    draw_node(screen, x, y, node.value, font, highlight)

    if x_offset < 35:
        x_offset = 35

    # recursive draw left side
    draw_tree(
        screen,
        node.left,
        x - x_offset,
        y + 85,
        x_offset // 2,
        font,
        highlight_values,
        (x, y)
    )

    # recursive draw right side
    draw_tree(
        screen,
        node.right,
        x + x_offset,
        y + 85,
        x_offset // 2,
        font,
        highlight_values,
        (x, y)
    )


def show_help_page(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 23)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - BST Algorithms", title_font, BLACK, 345, 50)

        draw_text(screen, "1. This page visualises a Binary Search Tree.", small_font, BLACK, 180, 120)
        draw_text(screen, "2. BST rule: smaller values go left, larger values go right.", small_font, BLACK, 180, 155)
        draw_text(screen, "3. Type a number and click Insert to add a node.", small_font, BLACK, 180, 190)
        draw_text(screen, "4. Click Search to highlight the search path.", small_font, BLACK, 180, 225)
        draw_text(screen, "5. In-order traversal is left, root, right.", small_font, BLACK, 180, 260)
        draw_text(screen, "6. Pre-order traversal is root, left, right.", small_font, BLACK, 180, 295)
        draw_text(screen, "7. Post-order traversal is left, right, root.", small_font, BLACK, 180, 330)
        draw_text(screen, "8. Delete handles leaf, one-child and two-child cases.", small_font, BLACK, 180, 365)
        draw_text(screen, "9. Reset will rebuild the sample BST.", small_font, BLACK, 180, 400)

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


def create_sample_bst():
    # build default tree for demo
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80]

    for value in values:
        bst.insert(value)

    return bst


def run_graph_algorithms_module(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 21)
    small_font = pygame.font.SysFont(None, 22)

    screen_width = screen.get_width()

    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen_width - 120, 25, 95, 40)

    input_box = pygame.Rect(455, 95, 180, 35)

    insert_button = pygame.Rect(95, 150, 100, 42)
    search_button = pygame.Rect(210, 150, 100, 42)
    delete_button = pygame.Rect(325, 150, 100, 42)

    inorder_button = pygame.Rect(460, 150, 100, 42)
    preorder_button = pygame.Rect(575, 150, 100, 42)
    postorder_button = pygame.Rect(690, 150, 110, 42)

    reset_button = pygame.Rect(835, 150, 100, 42)

    bst = create_sample_bst()

    input_text = ""
    input_active = False

    highlight_values = []

    # these variables are for traversal animation
    animation_values = []
    animation_index = 0
    animation_active = False
    last_animation_time = 0

    message = "BST sample created. Type a number to insert, search or delete."
    traversal_text = "Traversal Result:"

    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()

        # play traversal animation one node by one node
        if animation_active:
            if current_time - last_animation_time > 650:
                last_animation_time = current_time

                if animation_index < len(animation_values):
                    highlight_values = [animation_values[animation_index]]
                    animation_index += 1

                else:
                    animation_active = False
                    highlight_values = []
                    message = "Traversal animation finished."

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        draw_text(screen, "BST Algorithms Module", title_font, BLACK, 360, 35)

        draw_text(screen, "Value:", small_font, BLACK, 395, 103)
        draw_input_box(screen, input_box, input_text, input_active, small_font)

        draw_button(screen, "Insert", insert_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Search", search_button, button_font, LIGHT_BLUE)
        draw_button(screen, "Delete", delete_button, button_font, LIGHT_RED)

        draw_button(screen, "In-order", inorder_button, button_font, YELLOW)
        draw_button(screen, "Pre-order", preorder_button, button_font, YELLOW)
        draw_button(screen, "Post-order", postorder_button, button_font, YELLOW)

        draw_button(screen, "Reset", reset_button, button_font, LIGHT_GRAY)

        draw_tree(
            screen,
            bst.root,
            screen_width // 2,
            250,
            230,
            small_font,
            highlight_values
        )

        draw_text(screen, message, small_font, BLACK, 210, 610)
        draw_text(screen, traversal_text, small_font, BLACK, 210, 640)

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

                elif insert_button.collidepoint(mouse_pos):
                    if input_text != "" and input_text != "-":
                        value = int(input_text)
                        bst.insert(value)

                        input_text = ""
                        highlight_values = [value]
                        animation_active = False

                        message = "Inserted " + str(value) + " into the BST."

                    else:
                        message = "Please type a number first."

                elif search_button.collidepoint(mouse_pos):
                    if input_text != "" and input_text != "-":
                        value = int(input_text)

                        # get the search route and highlight it
                        path, found = bst.search_path(value)

                        highlight_values = path
                        animation_active = False

                        if found:
                            message = "Found " + str(value) + ". Search path is highlighted."
                        else:
                            message = str(value) + " was not found. Search path is highlighted."

                    else:
                        message = "Please type a number first."

                elif delete_button.collidepoint(mouse_pos):
                    if input_text != "" and input_text != "-":
                        value = int(input_text)

                        # delete node from BST
                        deleted = bst.delete(value)

                        input_text = ""
                        highlight_values = []
                        animation_active = False

                        if deleted:
                            message = "Deleted " + str(value) + " from the BST."
                        else:
                            message = str(value) + " was not found. Cannot delete."

                    else:
                        message = "Please type a number first."

                elif inorder_button.collidepoint(mouse_pos):
                    # make in-order result and animate it
                    animation_values = bst.inorder()
                    traversal_text = "Traversal Result: In-order = " + str(animation_values)

                    animation_index = 0
                    animation_active = True
                    last_animation_time = pygame.time.get_ticks()
                    message = "In-order traversal started."

                elif preorder_button.collidepoint(mouse_pos):
                    # make pre-order result and animate it
                    animation_values = bst.preorder()
                    traversal_text = "Traversal Result: Pre-order = " + str(animation_values)

                    animation_index = 0
                    animation_active = True
                    last_animation_time = pygame.time.get_ticks()
                    message = "Pre-order traversal started."

                elif postorder_button.collidepoint(mouse_pos):
                    # make post-order result and animate it
                    animation_values = bst.postorder()
                    traversal_text = "Traversal Result: Post-order = " + str(animation_values)

                    animation_index = 0
                    animation_active = True
                    last_animation_time = pygame.time.get_ticks()
                    message = "Post-order traversal started."

                elif reset_button.collidepoint(mouse_pos):
                    # rebuild the default BST
                    bst = create_sample_bst()

                    input_text = ""
                    highlight_values = []
                    animation_values = []
                    animation_index = 0
                    animation_active = False

                    message = "BST sample has been reset."
                    traversal_text = "Traversal Result:"

        pygame.display.update()
        clock.tick(60)