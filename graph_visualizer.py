import pygame
import sys
from collections import deque   # deque for BFS queue


# colours for drawing
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)


def draw_text(screen, text, font, colour, x, y):
    # make text img then put on screen
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # draw button bg and border
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # put txt in middle of button
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def bfs(graph, start):
    """
    Breadth First Search.
    Visits neighbours level by level.
    """
    # visited list save the order
    visited = []

    # BFS use queue, first in first out
    queue = deque()
    queue.append(start)

    # keep going while queue not empty
    while len(queue) > 0:
        # take first node from queue
        node = queue.popleft()

        # only visit if not visited before
        if node not in visited:
            visited.append(node)

            # add all neighbours into queue
            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)

    # return BFS order
    return visited


def dfs(graph, start):
    """
    Depth First Search.
    Goes as deep as possible before backtracking.
    """
    # visited list save the order
    visited = []

    # DFS use stack, last in first out
    stack = []
    stack.append(start)

    # keep going while stack not empty
    while len(stack) > 0:
        # take last node from stack
        node = stack.pop()

        # only visit node one time
        if node not in visited:
            visited.append(node)

            # reverse is used so visit order looks normal
            for neighbour in reversed(graph[node]):
                if neighbour not in visited:
                    stack.append(neighbour)

    # return DFS order
    return visited


def draw_graph(screen, font, positions, edges, selected_node, visited_nodes, current_node):
    """
    Draw graph nodes and edges.
    """
    # draw edges first, so lines not cover node text
    for node in edges:
        for neighbour in edges[node]:
            start_pos = positions[node]
            end_pos = positions[neighbour]
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    # draw every node
    for node, pos in positions.items():
        x, y = pos

        # choose node colour
        if node == current_node:
            colour = YELLOW          # now visiting
        elif node in visited_nodes:
            colour = LIGHT_GREEN     # already visited
        elif node == selected_node:
            colour = ORANGE          # start node
        else:
            colour = LIGHT_BLUE      # normal node

        # draw circle node
        pygame.draw.circle(screen, colour, (x, y), 30)
        pygame.draw.circle(screen, BLACK, (x, y), 30, 2)

        # draw node name
        text_surface = font.render(node, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)


def get_clicked_node(mouse_pos, positions):
    """
    Check whether the user clicked a graph node.
    """
    mouse_x, mouse_y = mouse_pos

    # check mouse distance to every node
    for node, pos in positions.items():
        node_x, node_y = pos

        # distance formula
        distance = ((mouse_x - node_x) ** 2 + (mouse_y - node_y) ** 2) ** 0.5

        # node radius is 30, so inside means clicked
        if distance <= 30:
            return node

    # no node clicked
    return None


def run_graph_module(screen, clock):
    """
    Main function for Graph Algorithms module.
    This module visualises BFS and DFS traversal.
    """
    # fonts
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    # graph using adjacency list
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"]
    }

    # node positions on screen
    positions = {
        "A": (450, 150),
        "B": (280, 260),
        "C": (620, 260),
        "D": (200, 410),
        "E": (370, 410),
        "F": (620, 410)
    }

    # default choices
    selected_node = "A"
    selected_algorithm = "BFS"

    # vars for animation
    traversal_order = []
    visited_nodes = []
    current_node = None

    is_running = False
    step_index = 0
    last_step_time = 0
    step_delay = 700

    message = "Click a node, choose BFS or DFS, then click Start."

    # buttons
    back_button = pygame.Rect(25, 25, 95, 40)

    bfs_button = pygame.Rect(160, 520, 100, 40)
    dfs_button = pygame.Rect(290, 520, 100, 40)
    start_button = pygame.Rect(420, 520, 100, 40)
    reset_button = pygame.Rect(550, 520, 100, 40)

    running = True

    while running:
        # clear screen each frame
        screen.fill(WHITE)

        # draw page info
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(
            screen,
            "Graph Algorithms Module",
            title_font,
            BLACK,
            260,
            35
        )

        draw_text(
            screen,
            "BFS and DFS Traversal Visualisation",
            small_font,
            BLACK,
            285,
            75
        )

        draw_text(
            screen,
            "Selected Start Node: " + selected_node,
            small_font,
            BLACK,
            120,
            105
        )

        draw_text(
            screen,
            "Selected Algorithm: " + selected_algorithm,
            small_font,
            BLACK,
            520,
            105
        )

        # draw graph with colours
        draw_graph(
            screen,
            small_font,
            positions,
            graph,
            selected_node,
            visited_nodes,
            current_node
        )

        # show msg
        draw_text(screen, message, small_font, BLACK, 170, 475)

        # show traversal order if have visited nodes
        if len(visited_nodes) > 0:
            order_text = "Traversal Order: " + " -> ".join(visited_nodes)
            draw_text(screen, order_text, small_font, BLACK, 170, 490)

        # draw buttons
        draw_button(screen, "BFS", bfs_button, button_font, LIGHT_BLUE)
        draw_button(screen, "DFS", dfs_button, button_font, LIGHT_GREEN)
        draw_button(screen, "Start", start_button, button_font, ORANGE)
        draw_button(screen, "Reset", reset_button, button_font, LIGHT_RED)

        # get time for animation
        current_time = pygame.time.get_ticks()

        # play traversal step by step
        if is_running:
            if current_time - last_step_time > step_delay:
                if step_index < len(traversal_order):
                    current_node = traversal_order[step_index]

                    if current_node not in visited_nodes:
                        visited_nodes.append(current_node)

                    message = selected_algorithm + " visiting node " + current_node

                    step_index += 1
                    last_step_time = current_time
                else:
                    # traversal done
                    is_running = False
                    current_node = None
                    message = selected_algorithm + " traversal completed."

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # go back main menu
                if back_button.collidepoint(mouse_pos):
                    running = False

                # choose BFS
                elif bfs_button.collidepoint(mouse_pos):
                    selected_algorithm = "BFS"
                    visited_nodes = []
                    current_node = None
                    is_running = False
                    step_index = 0
                    message = "BFS selected."

                # choose DFS
                elif dfs_button.collidepoint(mouse_pos):
                    selected_algorithm = "DFS"
                    visited_nodes = []
                    current_node = None
                    is_running = False
                    step_index = 0
                    message = "DFS selected."

                # start traversal
                elif start_button.collidepoint(mouse_pos):
                    if selected_algorithm == "BFS":
                        traversal_order = bfs(graph, selected_node)
                    else:
                        traversal_order = dfs(graph, selected_node)

                    visited_nodes = []
                    current_node = None
                    step_index = 0
                    is_running = True
                    last_step_time = pygame.time.get_ticks()
                    message = selected_algorithm + " started from node " + selected_node

                # reset graph view
                elif reset_button.collidepoint(mouse_pos):
                    traversal_order = []
                    visited_nodes = []
                    current_node = None
                    is_running = False
                    step_index = 0
                    message = "Graph traversal has been reset."

                # if not click button, maybe click node
                else:
                    clicked_node = get_clicked_node(mouse_pos, positions)

                    if clicked_node is not None:
                        selected_node = clicked_node
                        traversal_order = []
                        visited_nodes = []
                        current_node = None
                        is_running = False
                        step_index = 0
                        message = "Start node changed to " + selected_node

        # update screen
        pygame.display.update()

        # limit FPS
        clock.tick(60)