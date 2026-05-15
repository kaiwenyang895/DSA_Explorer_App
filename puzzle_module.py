import pygame
import sys
import heapq  # Used to implement a priority queue for Dijkstra's algorithm

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 153)
ORANGE = (255, 204, 153)
DARK_GRAY = (80, 80, 80)


def draw_text(screen, text, font, colour, x, y):
    # change text into a Pygame surface
    text_surface = font.render(text, True, colour)


    screen.blit(text_surface, (x, y))


def draw_button(screen, text, rect, font, colour):
    # Draw the button background
    pygame.draw.rect(screen, colour, rect)


    pygame.draw.rect(screen, BLACK, rect, 2)

   #draw text
    text_surface = font.render(text, True, BLACK)

    # Centre the text inside the button
    text_rect = text_surface.get_rect(center=rect.center)

    # Draw the text on the button
    screen.blit(text_surface, text_rect)


def get_cell_from_mouse(mouse_pos, grid_x, grid_y, cell_size, rows, cols):
    # Get mouse position
    mouse_x, mouse_y = mouse_pos

    # Return None if the click is outside the grid area
    if mouse_x < grid_x or mouse_y < grid_y:
        return None

    # Convert mouse position into grid column and row
    col = (mouse_x - grid_x) // cell_size
    row = (mouse_y - grid_y) // cell_size

    # Check whether the clicked cell is inside the grid
    if 0 <= row < rows and 0 <= col < cols:
        return int(row), int(col)

    # Return None if the click is outside the grid
    return None

####Add obstacles.
#important
##important
#important
def get_neighbours(cell, rows, cols):
    # Get the row and column of the current cell
    row, col = cell


    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbours = []

    # Check each direction
    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        # Add the neighbour only if it is inside the grid
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbours.append((new_row, new_col))

    # Return all valid neighbour cells
    return neighbours

## Supporting Resources
#This part largely referenced and learned from coding video bloggers on YouTube.
# #Thanks to Arjun, Rahul, and Johann.
def dijkstra_pathfinding(rows, cols, start, end, obstacles):
    # Store the shortest distance from the start cell to each cell
    distances = {}

    # Store the previous cell for reconstructing the final path
    previous = {}

    # Store the order of visited cells for animation
    visited_order = []

    # Initialise all cell distances as infinity
    for row in range(rows):
        for col in range(cols):
            distances[(row, col)] = float("inf")

    # The distance from the start cell to itself is 0
    distances[start] = 0

    # Priority queue stores cells based on the current shortest distance
    priority_queue = []

    # Add the start cell to the priority queue
    heapq.heappush(priority_queue, (0, start))

    # Store cells that have already been visited
    visited = set()

    # Continue while there are cells in the priority queue
    while len(priority_queue) > 0:
        # Get the cell with the smallest current distance
        current_distance, current_cell = heapq.heappop(priority_queue)

        # Skip the cell if it has already been visited
        if current_cell in visited:
            continue

        # Mark the current cell as visited
        visited.add(current_cell)

        # Add the current cell to the visited order for visualisation
        visited_order.append(current_cell)

        # Stop the search if the end cell is reached
        if current_cell == end:
            break

        # Check all valid neighbouring cells
        for neighbour in get_neighbours(current_cell, rows, cols):
            # Skip obstacle cells
            if neighbour in obstacles:
                continue

            # Each movement has a cost of 1
            new_distance = current_distance + 1

            # Update the distance if a shorter path is found
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance

                # Record where this neighbour came from
                previous[neighbour] = current_cell

                # Add the neighbour to the priority queue
                heapq.heappush(priority_queue, (new_distance, neighbour))

    # Store the final shortest path
    path = []

    # Reconstruct the path if the end cell is reachable
    if end in previous or start == end:
        current = end
        path.append(current)

        # Trace backwards from the end cell to the start cell
        while current != start:
            current = previous[current]
            path.append(current)

        # Reverse the path so it goes from start to end
        path.reverse()

    # Return the visited order and the final path
    return visited_order, path


def dynamic_programming_grid(rows, cols, obstacles):
    # Create a 2D dynamic programming table
    dp = []

    # Fill the DP table with 0
    for row in range(rows):
        dp.append([])
        for col in range(cols):
            dp[row].append(0)

    # In DP mode, the start and end cells are fixed
    start = (0, 0)
    end = (rows - 1, cols - 1)

    # If the start or end cell is blocked, there is no valid path
    if start in obstacles or end in obstacles:
        return dp, 0, []

    # There is one way to stand on the start cell
    dp[0][0] = 1

    # Fill the DP table row by row
    for row in range(rows):
        for col in range(cols):
            # Obstacle cells cannot be used
            if (row, col) in obstacles:
                dp[row][col] = 0
                continue

            # Skip the start cell because it is already initialised
            if row == 0 and col == 0:
                continue

            from_top = 0
            from_left = 0

            # Number of paths coming from the cell above
            if row > 0:
                from_top = dp[row - 1][col]

            # Number of paths coming from the cell on the left
            if col > 0:
                from_left = dp[row][col - 1]

            # DP formula: paths to current cell = paths from top + paths from left
            dp[row][col] = from_top + from_left

    # Store one possible valid path for visualisation
    path = []

    # If the end cell has at least one valid path
    if dp[rows - 1][cols - 1] > 0:
        row = rows - 1
        col = cols - 1
        path.append((row, col))

        # Trace backwards from the end cell to the start cell
        while not (row == 0 and col == 0):
            # Prefer moving upwards if possible
            if row > 0 and dp[row - 1][col] > 0:
                row -= 1

            # Otherwise move left if possible
            elif col > 0 and dp[row][col - 1] > 0:
                col -= 1

            # Stop if no valid previous cell exists
            else:
                break

            path.append((row, col))

        # Reverse the path so it goes from start to end
        path.reverse()

    # Return the DP table, the total path count, and one valid path
    return dp, dp[rows - 1][cols - 1], path


def dynamic_programming_grid_steps(rows, cols, obstacles):
    dp = []

    for row in range(rows):
        dp.append([])
        for col in range(cols):
            dp[row].append(0)

    steps = []
    start = (0, 0)
    end = (rows - 1, cols - 1)

    if start in obstacles or end in obstacles:
        steps.append(([r[:] for r in dp], None, "No valid path because start or end is blocked."))
        return steps, dp, 0, []

    dp[0][0] = 1
    steps.append(([r[:] for r in dp], (0, 0), "DP start cell has 1 path."))

    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue

            if (row, col) in obstacles:
                dp[row][col] = 0
                steps.append(([r[:] for r in dp], (row, col), "Obstacle cell cannot be used."))
                continue

            from_top = 0
            from_left = 0

            if row > 0:
                from_top = dp[row - 1][col]

            if col > 0:
                from_left = dp[row][col - 1]

            dp[row][col] = from_top + from_left
            steps.append(([r[:] for r in dp], (row, col), "DP updating paths from top and left."))

    final_dp, path_count, path = dynamic_programming_grid(rows, cols, obstacles)
    return steps, final_dp, path_count, path


def coin_change_dp_steps(coins, amount):
    ways = []

    for i in range(amount + 1):
        ways.append(0)

    ways[0] = 1
    steps = []
    steps.append((ways[:], -1, "Coin Change DP started. ways[0] = 1."))

    for coin in coins:
        for value in range(coin, amount + 1):
            ways[value] = ways[value] + ways[value - coin]
            steps.append((ways[:], value, "Using coin " + str(coin) + " to update amount " + str(value) + "."))

    steps.append((ways[:], -1, "Coin Change completed. Total ways = " + str(ways[amount]) + "."))
    return steps, ways[amount]


def draw_coin_change(screen, font, coins, amount, ways, highlight_amount):
    start_x = 280
    start_y = 165
    cell_width = 50
    cell_height = 45

    draw_text(screen, "Coin Change DP", font, BLACK, start_x, 120)
    draw_text(screen, "Coins: " + str(coins), font, BLACK, start_x, 140)

    for value in range(amount + 1):
        x = start_x + value * cell_width

        amount_rect = pygame.Rect(x, start_y, cell_width, cell_height)
        ways_rect = pygame.Rect(x, start_y + cell_height, cell_width, cell_height)

        if value == highlight_amount:
            colour = YELLOW
        else:
            colour = WHITE

        pygame.draw.rect(screen, LIGHT_GRAY, amount_rect)
        pygame.draw.rect(screen, colour, ways_rect)

        pygame.draw.rect(screen, BLACK, amount_rect, 1)
        pygame.draw.rect(screen, BLACK, ways_rect, 1)

        amount_text = font.render(str(value), True, BLACK)
        amount_rect_text = amount_text.get_rect(center=amount_rect.center)
        screen.blit(amount_text, amount_rect_text)

        if value < len(ways):
            ways_text = font.render(str(ways[value]), True, BLACK)
        else:
            ways_text = font.render("0", True, BLACK)

        ways_rect_text = ways_text.get_rect(center=ways_rect.center)
        screen.blit(ways_text, ways_rect_text)

    draw_text(screen, "Amount", font, BLACK, start_x - 75, start_y + 13)
    draw_text(screen, "Ways", font, BLACK, start_x - 75, start_y + cell_height + 13)


def show_puzzle_help(screen, clock):
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 22)

    back_button = pygame.Rect(25, 25, 95, 40)

    running = True

    while running:
        screen.fill(WHITE)

        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)

        draw_text(screen, "Help - Puzzle Challenges", title_font, BLACK, 260, 45)

        draw_text(screen, "Pathfinding mode:", small_font, BLACK, 160, 120)
        draw_text(screen, "1. Choose Start, End, or Obstacle.", small_font, BLACK, 190, 150)
        draw_text(screen, "2. Click the grid to place it.", small_font, BLACK, 190, 180)
        draw_text(screen, "3. Click Run to show Dijkstra shortest path.", small_font, BLACK, 190, 210)

        draw_text(screen, "DP mode:", small_font, BLACK, 160, 260)
        draw_text(screen, "1. Click cells to add obstacles.", small_font, BLACK, 190, 290)
        draw_text(screen, "2. Start is top-left and end is bottom-right.", small_font, BLACK, 190, 320)
        draw_text(screen, "3. Click Run to count paths and draw one valid path.", small_font, BLACK, 190, 350)

        draw_text(screen, "Coin DP:", small_font, BLACK, 160, 400)
        draw_text(screen, "1. Click Coin DP on the right side.", small_font, BLACK, 190, 430)
        draw_text(screen, "2. Use - and + to change the amount.", small_font, BLACK, 190, 460)
        draw_text(screen, "3. Click Run to visualise another DP example.", small_font, BLACK, 190, 490)

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


def draw_grid(
    screen,
    font,
    rows,
    cols,
    grid_x,
    grid_y,
    cell_size,
    mode,
    start,
    end,
    obstacles,
    visited_cells,
    path_cells,
    dp_table,
    highlight_cell=None
):
    # Loop through every cell
    for row in range(rows):
        for col in range(cols):
            cell = (row, col)

            # Calculate the p
            x = grid_x + col * cell_size
            y = grid_y + row * cell_size

            # Create a rectangle
            rect = pygame.Rect(x, y, cell_size, cell_size)

            # the top-left cell as start and bottom-right cell as end
            if mode == "DP":
                display_start = (0, 0)
                display_end = (rows - 1, cols - 1)
            else:
                display_start = start
                display_end = end

            #cell colour
            if cell in obstacles:
                colour = DARK_GRAY
            elif cell == display_start:
                colour = LIGHT_GREEN
            elif cell == display_end:
                colour = LIGHT_RED
            elif cell in path_cells:
                colour = YELLOW
            elif cell == highlight_cell:
                colour = ORANGE
            elif cell in visited_cells:
                colour = LIGHT_BLUE
            else:
                colour = WHITE

            # Draw background
            pygame.draw.rect(screen, colour, rect)

            #cell border
            pygame.draw.rect(screen, BLACK, rect, 1)

            # start
            if cell == display_start:
                text_surface = font.render("S", True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

            # end cell
            elif cell == display_end:
                text_surface = font.render("E", True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

            #show the number of path for each cell
            elif mode == "DP" and dp_table is not None and cell not in obstacles:
                value = dp_table[row][col]

                if value > 0:
                    text_surface = font.render(str(value), True, BLACK)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)


def run_puzzle_module(screen, clock):
    #fonts
    title_font = pygame.font.SysFont(None, 42)
    button_font = pygame.font.SysFont(None, 20)
    small_font = pygame.font.SysFont(None, 20)


    rows = 8
    cols = 8
    cell_size = 45

    # Grid position
    grid_x = 270
    grid_y = 120


    mode = "Pathfinding"
    tool = "Obstacle"

    #start and end cells
    start = (0, 0)
    end = (7, 7)

    # Store obstacle cells,visited order from Dijkstra's algorithm，
    # cells that have been displayed during animation，final path cells
    obstacles = set()


    visited_order = []


    visited_cells = set()


    path_cells = []


    dp_table = None
    path_count = 0

    dp_steps = []
    highlight_cell = None
    final_path_cells = []

    coins = [1, 2, 5]
    coin_amount = 10
    coin_steps = []
    coin_table = []
    for i in range(coin_amount + 1):
        coin_table.append(0)
    coin_result = 0
    coin_highlight = -1

    # Animation control
    is_animating = False
    animation_index = 0
    last_step_time = 0
    step_delay = 80
    animation_type = None

    # Message for user
    message = "Pathfinding mode: choose Start, End or Obstacle, then click grid."

    # Button
    back_button = pygame.Rect(25, 25, 95, 40)
    help_button = pygame.Rect(screen.get_width() - 120, 25, 95, 40)
    coin_button = pygame.Rect(screen.get_width() - 145, 115, 115, 40)

    pathfinding_button = pygame.Rect(50, 520, 120, 40)
    dp_button = pygame.Rect(180, 520, 70, 40)

    start_button = pygame.Rect(375, 520, 75, 40)
    end_button = pygame.Rect(460, 520, 65, 40)
    obstacle_button = pygame.Rect(535, 520, 90, 40)

    amount_down_button = pygame.Rect(screen.get_width() - 145, 430, 45, 35)
    amount_up_button = pygame.Rect(screen.get_width() - 90, 430, 45, 35)

    run_button = pygame.Rect(635, 520, 70, 40)
    clear_button = pygame.Rect(715, 520, 75, 40)

    # Main
    running = True

    while running:

        screen.fill(WHITE)

        #back button
        draw_button(screen, "Back", back_button, button_font, LIGHT_GRAY)
        draw_button(screen, "Help", help_button, button_font, LIGHT_GRAY)

        #title
        draw_text(
            screen,
            "Puzzle Challenges Module",
            title_font,
            BLACK,
            245,
            35
        )

        #subtitle
        draw_text(
            screen,
            "Dijkstra Pathfinding and Dynamic Programming Grid Puzzle",
            small_font,
            BLACK,
            215,
            75
        )

        draw_button(screen, "Coin DP", coin_button, button_font, YELLOW)

        draw_text(
            screen,
            "Another DP example.",
            small_font,
            BLACK,
            screen.get_width() - 165,
            160
        )

        draw_text(
            screen,
            "Click to open it.",
            small_font,
            BLACK,
            screen.get_width() - 165,
            180
        )

        #current mode
        draw_text(
            screen,
            "Mode: " + mode,
            small_font,
            BLACK,
            90,
            120
        )

        #current tool
        draw_text(
            screen,
            "Tool: " + tool,
            small_font,
            BLACK,
            90,
            150
        )

        #instructions
        if mode == "DP":
            draw_text(
                screen,
                "DP (right and down).",
                small_font,
                BLACK,
                90,
                190
            )

            draw_text(
                screen,
                "Start = top-left",
                small_font,
                BLACK,
                90,
                220
            )

            draw_text(
                screen,
                "End = bottom-right",
                small_font,
                BLACK,
                90,
                250
            )

            draw_text(
                screen,
                "Path Count: " + str(path_count),
                small_font,
                BLACK,
                90,
                280
            )

        elif mode == "Coin Change":
            draw_text(
                screen,
                "Coin Change DP.",
                small_font,
                BLACK,
                90,
                190
            )

            draw_text(
                screen,
                "Amount = " + str(coin_amount),
                small_font,
                BLACK,
                90,
                220
            )

            draw_text(
                screen,
                "Coins = " + str(coins),
                small_font,
                BLACK,
                90,
                250
            )

            draw_text(
                screen,
                "Ways = " + str(coin_result),
                small_font,
                BLACK,
                90,
                280
            )

        else:
            draw_text(
                screen,
                "Dijkstra (the shortest path).",
                small_font,
                BLACK,
                90,
                190
            )

            draw_text(
                screen,
                "Green = Start",
                small_font,
                BLACK,
                90,
                220
            )

            draw_text(
                screen,
                "Red = End",
                small_font,
                BLACK,
                90,
                250
            )

            draw_text(
                screen,
                "Black = Obstacle",
                small_font,
                BLACK,
                90,
                280
            )

        #grid
        if mode == "Coin Change":
            draw_coin_change(
                screen,
                small_font,
                coins,
                coin_amount,
                coin_table,
                coin_highlight
            )
        else:
            draw_grid(
                screen,
                small_font,
                rows,
                cols,
                grid_x,
                grid_y,
                cell_size,
                mode,
                start,
                end,
                obstacles,
                visited_cells,
                path_cells,
                dp_table,
                highlight_cell
            )

        #message
        draw_text(screen, message, small_font, BLACK, 225, 485)

        #buttons
        draw_button(screen, "Pathfinding", pathfinding_button, button_font, LIGHT_BLUE)
        draw_button(screen, "DP", dp_button, button_font, LIGHT_GREEN)

        if mode != "Coin Change":
            draw_button(screen, "Start", start_button, button_font, LIGHT_GREEN)
            draw_button(screen, "End", end_button, button_font, LIGHT_RED)
            draw_button(screen, "Obstacle", obstacle_button, button_font, LIGHT_GRAY)

        if mode == "Coin Change":
            draw_text(screen, "Change amount", small_font, BLACK, screen.get_width() - 150, 405)
            draw_button(screen, "-", amount_down_button, button_font, LIGHT_RED)
            draw_button(screen, "+", amount_up_button, button_font, LIGHT_GREEN)

        draw_button(screen, "Run", run_button, button_font, ORANGE)
        draw_button(screen, "Clear", clear_button, button_font, LIGHT_RED)

        #dipict time
        current_time = pygame.time.get_ticks()

        # Animat
        if is_animating:
            if current_time - last_step_time > step_delay:
                if animation_type == "Pathfinding":
                    # Show the next visited cell
                    if animation_index < len(visited_order):
                        visited_cells.add(visited_order[animation_index])
                        animation_index += 1
                        last_step_time = current_time

                    # Stop animation
                    else:
                        is_animating = False
                        path_cells = final_path_cells

                        if len(path_cells) > 0:
                            message = "Shortest path found using Dijkstra."
                        else:
                            message = "No path found."

                elif animation_type == "DP":
                    if animation_index < len(dp_steps):
                        dp_table, highlight_cell, message = dp_steps[animation_index]
                        animation_index += 1
                        last_step_time = current_time
                    else:
                        is_animating = False
                        path_cells = final_path_cells
                        highlight_cell = None
                        message = "DP completed. Path count = " + str(path_count)

                elif animation_type == "Coin Change":
                    if animation_index < len(coin_steps):
                        coin_table, coin_highlight, message = coin_steps[animation_index]
                        animation_index += 1
                        last_step_time = current_time
                    else:
                        is_animating = False
                        coin_highlight = -1
                        message = "Coin Change completed. Total ways = " + str(coin_result)


        for event in pygame.event.get():
            # Quit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mouse click fuuction
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Return back to menu
                if back_button.collidepoint(mouse_pos):
                    running = False

                elif help_button.collidepoint(mouse_pos):
                    show_puzzle_help(screen, clock)

                #Pathfinding mode
                elif pathfinding_button.collidepoint(mouse_pos):
                    mode = "Pathfinding"
                    tool = "Obstacle"
                    visited_order = []
                    visited_cells = set()
                    path_cells = []
                    final_path_cells = []
                    dp_table = None
                    path_count = 0
                    dp_steps = []
                    highlight_cell = None
                    is_animating = False
                    animation_type = None
                    message = "Pathfinding mode selected."

                #DP mode
                elif dp_button.collidepoint(mouse_pos):
                    mode = "DP"
                    tool = "Obstacle"

                    # DP mode uses fixed start and end cells(0,0)
                    start = (0, 0)
                    end = (rows - 1, cols - 1)

                    #the start and end cells are not obstacles (bug fixing)
                    obstacles.discard(start)
                    obstacles.discard(end)

                    visited_order = []
                    visited_cells = set()
                    path_cells = []
                    final_path_cells = []
                    dp_table = None
                    path_count = 0
                    dp_steps = []
                    highlight_cell = None
                    is_animating = False
                    animation_type = None
                    message = "DP mode selected. Click cells to add obstacles."

                elif coin_button.collidepoint(mouse_pos):
                    mode = "Coin Change"
                    tool = "None"
                    visited_order = []
                    visited_cells = set()
                    path_cells = []
                    final_path_cells = []
                    dp_table = None
                    path_count = 0
                    dp_steps = []
                    highlight_cell = None
                    coin_steps = []
                    coin_table = []
                    for i in range(coin_amount + 1):
                        coin_table.append(0)
                    coin_result = 0
                    coin_highlight = -1
                    is_animating = False
                    animation_type = None
                    message = "Coin Change DP selected. Click Run."

                #Start tool
                elif start_button.collidepoint(mouse_pos) and mode != "Coin Change":
                    tool = "Start"
                    message = "Click a grid cell to place the start point."

                #End tool
                elif end_button.collidepoint(mouse_pos) and mode != "Coin Change":
                    tool = "End"
                    message = "Click a grid cell to place the end point."

                # Obstacle tool
                elif obstacle_button.collidepoint(mouse_pos) and mode != "Coin Change":
                    tool = "Obstacle"
                    message = "Click grid cells to add or remove obstacles."

                elif amount_down_button.collidepoint(mouse_pos) and mode == "Coin Change":
                    if coin_amount > 1:
                        coin_amount -= 1
                        coin_table = []
                        for i in range(coin_amount + 1):
                            coin_table.append(0)

                        coin_steps = []
                        coin_result = 0
                        coin_highlight = -1
                        is_animating = False
                        animation_type = None
                        message = "Coin amount decreased."

                elif amount_up_button.collidepoint(mouse_pos) and mode == "Coin Change":
                    if coin_amount < 15:
                        coin_amount += 1
                        coin_table = []
                        for i in range(coin_amount + 1):
                            coin_table.append(0)

                        coin_steps = []
                        coin_result = 0
                        coin_highlight = -1
                        is_animating = False
                        animation_type = None
                        message = "Coin amount increased."

                # Run
                elif run_button.collidepoint(mouse_pos):

                    if mode == "Pathfinding":
                        visited_order, final_path_cells = dijkstra_pathfinding(
                            rows,
                            cols,
                            start,
                            end,
                            obstacles
                        )

                        # Reset animation variables
                        visited_cells = set()
                        path_cells = []
                        animation_index = 0
                        is_animating = True
                        animation_type = "Pathfinding"
                        last_step_time = pygame.time.get_ticks()
                        dp_table = None
                        highlight_cell = None
                        message = "Running Dijkstra pathfinding..."

                    # Run Dynamic Programming
                    elif mode == "DP":
                        dp_steps, dp_table, path_count, final_path_cells = dynamic_programming_grid_steps(
                            rows,
                            cols,
                            obstacles
                        )

                        visited_cells = set()
                        visited_order = []
                        path_cells = []
                        animation_index = 0
                        is_animating = True
                        animation_type = "DP"
                        last_step_time = pygame.time.get_ticks()
                        message = "Running DP grid path counting..."

                    else:
                        coin_steps, coin_result = coin_change_dp_steps(coins, coin_amount)
                        coin_table = []
                        for i in range(coin_amount + 1):
                            coin_table.append(0)
                        coin_highlight = -1
                        animation_index = 0
                        is_animating = True
                        animation_type = "Coin Change"
                        last_step_time = pygame.time.get_ticks()
                        message = "Running Coin Change DP..."

                # Clear the grid
                elif clear_button.collidepoint(mouse_pos):
                    obstacles.clear()
                    visited_order = []
                    visited_cells = set()
                    path_cells = []
                    final_path_cells = []
                    dp_table = None
                    path_count = 0
                    dp_steps = []
                    highlight_cell = None
                    coin_steps = []
                    coin_table = []
                    for i in range(coin_amount + 1):
                        coin_table.append(0)
                    coin_result = 0
                    coin_highlight = -1
                    is_animating = False
                    animation_type = None
                    start = (0, 0)
                    end = (rows - 1, cols - 1)
                    message = "Grid cleared."

                #grid cell click
                else:
                    if mode != "Coin Change":
                        clicked_cell = get_cell_from_mouse(
                            mouse_pos,
                            grid_x,
                            grid_y,
                            cell_size,
                            rows,
                            cols
                        )


                        if clicked_cell is not None:
                            # Clear previous results whenever the grid changes
                            visited_order = []
                            visited_cells = set()
                            path_cells = []
                            final_path_cells = []
                            dp_table = None
                            path_count = 0
                            dp_steps = []
                            highlight_cell = None
                            is_animating = False
                            animation_type = None

                            #dp model
                            if mode == "DP":
                                if clicked_cell != (0, 0) and clicked_cell != (rows - 1, cols - 1):

                                    if clicked_cell in obstacles:
                                        obstacles.remove(clicked_cell)
                                    else:
                                        obstacles.add(clicked_cell)

                                    message = "Obstacle updated for DP puzzle."

                            # In Pathfinding mode, start, end and obstacles can be changed
                            else:
                                if tool == "Start":

                                    if clicked_cell != end and clicked_cell not in obstacles:
                                        start = clicked_cell
                                        message = "Start point updated."

                                elif tool == "End":

                                    if clicked_cell != start and clicked_cell not in obstacles:
                                        end = clicked_cell
                                        message = "End point updated."

                                elif tool == "Obstacle":
                                    # Obstacles cannot be placed on the start or end cell( bug fixing)
                                    if clicked_cell != start and clicked_cell != end:

                                        if clicked_cell in obstacles:
                                            obstacles.remove(clicked_cell)
                                        else:
                                            obstacles.add(clicked_cell)

                                        message = "Obstacle updated."


        pygame.display.update()


        clock.tick(60)
