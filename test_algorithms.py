import os
import time
import unittest

#important!!!
# When testing the algorithm, we don't need to actually open a window, so here we set it to use a fake display driver without opening a real Pygame window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from data_structures import LinkedList, clamp
from sorting_visualizer import (
    bubble_sort_steps,
    selection_sort_steps,
    create_random_array
)
from graph_visualizer import bfs, dfs, get_clicked_node
from puzzle_module import (
    get_cell_from_mouse,
    get_neighbours,
    dijkstra_pathfinding,
    dynamic_programming_grid
)



def get_final_array(generator, original_data):
    # get the last array from sorting steps
    final_array = original_data[:]

    for step in generator:
        final_array = step[0][:]

    return final_array


def assert_valid_grid_path(testcase, path, start, end, rows, cols, obstacles):
    # check if path is inside grid and not going through wall
    testcase.assertIsInstance(path, list)
    testcase.assertGreater(len(path), 0)

    testcase.assertEqual(path[0], start)
    testcase.assertEqual(path[-1], end)

    for row, col in path:
        testcase.assertGreaterEqual(row, 0)
        testcase.assertLess(row, rows)
        testcase.assertGreaterEqual(col, 0)
        testcase.assertLess(col, cols)
        testcase.assertNotIn((row, col), obstacles)

    for index in range(len(path) - 1):
        row1, col1 = path[index]
        row2, col2 = path[index + 1]

        distance = abs(row1 - row2) + abs(col1 - col2)

        testcase.assertEqual(distance, 1)


#
# Phase 1: Linked List


class TestLinkedList(unittest.TestCase):


    def test_insert_end(self):
        linked_list = LinkedList()

        linked_list.insert_end(10)
        linked_list.insert_end(20)
        linked_list.insert_end(30)

        self.assertEqual(linked_list.to_list(), [10, 20, 30])
        self.assertEqual(linked_list.size, 3)

    def test_delete_head(self):
        linked_list = LinkedList()

        linked_list.insert_end(10)
        linked_list.insert_end(20)
        linked_list.insert_end(30)

        removed = linked_list.delete_head()

        self.assertEqual(removed, 10)
        self.assertEqual(linked_list.to_list(), [20, 30])
        self.assertEqual(linked_list.size, 2)

    def test_delete_from_empty_list(self):
        linked_list = LinkedList()

        removed = linked_list.delete_head()

        self.assertIsNone(removed)
        self.assertEqual(linked_list.to_list(), [])
        self.assertEqual(linked_list.size, 0)

    def test_reverse(self):
        linked_list = LinkedList()

        linked_list.insert_end(1)
        linked_list.insert_end(2)
        linked_list.insert_end(3)

        linked_list.reverse()

        self.assertEqual(linked_list.to_list(), [3, 2, 1])

    def test_reverse_empty_list(self):
        linked_list = LinkedList()

        linked_list.reverse()

        self.assertEqual(linked_list.to_list(), [])
        self.assertEqual(linked_list.size, 0)

    def test_clear(self):
        linked_list = LinkedList()

        linked_list.insert_end(1)
        linked_list.insert_end(2)
        linked_list.clear()

        self.assertEqual(linked_list.to_list(), [])
        self.assertEqual(linked_list.size, 0)



# Phase 1: Stack and Queue Tests
class TestStackAndQueue(unittest.TestCase):


    def test_stack_push_pop_lifo_order(self):
        stack = []

        stack.append(10)
        stack.append(20)
        stack.append(30)

        self.assertEqual(stack.pop(), 30)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack, [10])

    def test_stack_empty_condition(self):
        stack = []

        self.assertEqual(len(stack), 0)
        self.assertFalse(len(stack) > 0)

    def test_stack_multiple_operations(self):
        stack = []

        stack.append(1)
        stack.append(2)
        stack.append(3)

        removed = stack.pop()
        stack.append(4)

        self.assertEqual(removed, 3)
        self.assertEqual(stack, [1, 2, 4])

    def test_queue_enqueue_dequeue_fifo_order(self):
        queue = []

        queue.append(10)
        queue.append(20)
        queue.append(30)
        queue.append(40)

        self.assertEqual(queue.pop(0), 10)
        self.assertEqual(queue.pop(0), 20)
        self.assertEqual(queue, [30, 40])

    def test_queue_empty_condition(self):
        queue = []

        self.assertEqual(len(queue), 0)
        self.assertFalse(len(queue) > 0)

    def test_queue_multiple_operations(self):
        queue = []

        queue.append(1)
        queue.append(2)
        queue.append(3)

        removed = queue.pop(0)
        queue.append(4)

        self.assertEqual(removed, 1)
        self.assertEqual(queue, [2, 3, 4])

    def test_stack_and_queue_are_independent(self):
        stack = []
        queue = []

        stack.append(1)
        stack.append(2)

        queue.append(1)
        queue.append(2)

        self.assertEqual(stack.pop(), 2)
        self.assertEqual(queue.pop(0), 1)

    def test_reset_clears_stack_queue_and_linked_list(self):
        stack = [1, 2, 3]
        queue = [1, 2, 3]

        linked_list = LinkedList()
        linked_list.insert_end(1)
        linked_list.insert_end(2)
        linked_list.insert_end(3)

        stack.clear()
        queue.clear()
        linked_list.clear()

        self.assertEqual(stack, [])
        self.assertEqual(queue, [])
        self.assertEqual(linked_list.to_list(), [])
        self.assertEqual(linked_list.size, 0)



# Phase 2: Sorting Tests


class TestSortingAlgorithms(unittest.TestCase):


    def test_bubble_sort_correctness(self):
        data = [5, 3, 8, 1, 2]

        result = get_final_array(bubble_sort_steps(data), data)

        self.assertEqual(result, [1, 2, 3, 5, 8])

    def test_selection_sort_correctness(self):
        data = [5, 3, 8, 1, 2]

        result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(result, [1, 2, 3, 5, 8])

    def test_sorting_with_duplicates(self):
        data = [4, 2, 4, 1, 2]

        bubble_result = get_final_array(bubble_sort_steps(data), data)
        selection_result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(bubble_result, [1, 2, 2, 4, 4])
        self.assertEqual(selection_result, [1, 2, 2, 4, 4])

    def test_sorting_empty_array(self):
        data = []

        bubble_result = get_final_array(bubble_sort_steps(data), data)
        selection_result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(bubble_result, [])
        self.assertEqual(selection_result, [])

    def test_sorting_single_element(self):
        data = [10]

        bubble_result = get_final_array(bubble_sort_steps(data), data)
        selection_result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(bubble_result, [10])
        self.assertEqual(selection_result, [10])

    def test_sorting_already_sorted_array(self):
        data = [1, 2, 3, 4, 5]

        bubble_result = get_final_array(bubble_sort_steps(data), data)
        selection_result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(bubble_result, [1, 2, 3, 4, 5])
        self.assertEqual(selection_result, [1, 2, 3, 4, 5])

    def test_sorting_reverse_order_array(self):
        data = [5, 4, 3, 2, 1]

        bubble_result = get_final_array(bubble_sort_steps(data), data)
        selection_result = get_final_array(selection_sort_steps(data), data)

        self.assertEqual(bubble_result, [1, 2, 3, 4, 5])
        self.assertEqual(selection_result, [1, 2, 3, 4, 5])

    def test_original_array_not_modified(self):
        data = [3, 1, 2]
        original = data[:]

        get_final_array(bubble_sort_steps(data), data)
        get_final_array(selection_sort_steps(data), data)

        self.assertEqual(data, original)

    def test_create_random_array_length_and_range(self):
        data = create_random_array()

        self.assertEqual(len(data), 10)

        for value in data:
            self.assertGreaterEqual(value, 40)
            self.assertLessEqual(value, 250)


# =========================
# Phase 2: Graph Tests
# =========================

class TestGraphAlgorithms(unittest.TestCase):
    """Tests for BFS and DFS."""

    def setUp(self):
        self.graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"]
        }

    def test_bfs_from_a(self):
        result = bfs(self.graph, "A")

        self.assertEqual(result, ["A", "B", "C", "D", "E", "F"])

    def test_dfs_from_a(self):
        result = dfs(self.graph, "A")

        self.assertEqual(result, ["A", "B", "D", "E", "F", "C"])

    def test_bfs_from_c(self):
        result = bfs(self.graph, "C")

        self.assertEqual(result, ["C", "A", "F", "B", "E", "D"])

    def test_dfs_from_c(self):
        result = dfs(self.graph, "C")

        self.assertEqual(result, ["C", "A", "B", "D", "E", "F"])

    def test_bfs_visits_all_reachable_nodes(self):
        result = bfs(self.graph, "A")

        self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})
        self.assertEqual(result[0], "A")

    def test_dfs_visits_all_reachable_nodes(self):
        result = dfs(self.graph, "A")

        self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})
        self.assertEqual(result[0], "A")



# Phase 3: Puzzle Helper Tests


class TestPuzzleHelpers(unittest.TestCase):
    """Tests for puzzle helper functions."""

    def test_get_cell_from_mouse_inside_grid(self):
        result = get_cell_from_mouse(
            mouse_pos=(315, 165),
            grid_x=270,
            grid_y=120,
            cell_size=45,
            rows=8,
            cols=8
        )

        self.assertEqual(result, (1, 1))

    def test_get_cell_from_mouse_outside_grid(self):
        result = get_cell_from_mouse(
            mouse_pos=(100, 100),
            grid_x=270,
            grid_y=120,
            cell_size=45,
            rows=8,
            cols=8
        )

        self.assertIsNone(result)

    def test_get_neighbours_corner_cell(self):
        result = get_neighbours((0, 0), 3, 3)

        self.assertEqual(set(result), {(1, 0), (0, 1)})

    def test_get_neighbours_middle_cell(self):
        result = get_neighbours((1, 1), 3, 3)

        self.assertEqual(
            set(result),
            {(0, 1), (2, 1), (1, 0), (1, 2)}
        )



# Phase 3: Dijkstra Pathfinding Tests


class TestDijkstraPathfinding(unittest.TestCase):
    """Tests for Dijkstra pathfinding."""

    def test_dijkstra_path_exists(self):
        rows = 3
        cols = 3
        start = (0, 0)
        end = (2, 2)
        obstacles = {(1, 0), (1, 1)}

        visited_order, path = dijkstra_pathfinding(
            rows,
            cols,
            start,
            end,
            obstacles
        )

        self.assertGreater(len(visited_order), 0)
        assert_valid_grid_path(
            self,
            path,
            start,
            end,
            rows,
            cols,
            obstacles
        )

    def test_dijkstra_no_path(self):
        rows = 3
        cols = 3
        start = (0, 0)
        end = (2, 2)
        obstacles = {(0, 1), (1, 0)}

        visited_order, path = dijkstra_pathfinding(
            rows,
            cols,
            start,
            end,
            obstacles
        )

        self.assertEqual(path, [])
        self.assertGreaterEqual(len(visited_order), 1)

    def test_dijkstra_start_equals_end(self):
        rows = 3
        cols = 3
        start = (1, 1)
        end = (1, 1)
        obstacles = set()

        visited_order, path = dijkstra_pathfinding(
            rows,
            cols,
            start,
            end,
            obstacles
        )

        self.assertEqual(path, [(1, 1)])
        self.assertEqual(visited_order[0], (1, 1))

    def test_dijkstra_path_avoids_obstacles(self):
        rows = 4
        cols = 4
        start = (0, 0)
        end = (3, 3)
        obstacles = {(0, 1), (1, 1), (2, 1)}

        visited_order, path = dijkstra_pathfinding(
            rows,
            cols,
            start,
            end,
            obstacles
        )

        assert_valid_grid_path(
            self,
            path,
            start,
            end,
            rows,
            cols,
            obstacles
        )

        for cell in obstacles:
            self.assertNotIn(cell, path)



# Phase 3: Dynamic Programming Tests


class TestDynamicProgrammingGrid(unittest.TestCase):
    """Tests for DP grid puzzle."""

    def test_dp_grid_no_obstacles_2_by_2(self):
        dp_table, path_count, path = dynamic_programming_grid(
            rows=2,
            cols=2,
            obstacles=set()
        )

        self.assertEqual(path_count, 2)
        self.assertEqual(dp_table[1][1], 2)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (1, 1))

    def test_dp_grid_no_obstacles_3_by_3(self):
        dp_table, path_count, path = dynamic_programming_grid(
            rows=3,
            cols=3,
            obstacles=set()
        )

        self.assertEqual(path_count, 6)
        self.assertEqual(dp_table[2][2], 6)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))

    def test_dp_grid_with_center_obstacle(self):
        obstacles = {(1, 1)}

        dp_table, path_count, path = dynamic_programming_grid(
            rows=3,
            cols=3,
            obstacles=obstacles
        )

        self.assertEqual(path_count, 2)
        self.assertEqual(dp_table[1][1], 0)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))

    def test_dp_grid_start_blocked(self):
        obstacles = {(0, 0)}

        dp_table, path_count, path = dynamic_programming_grid(
            rows=3,
            cols=3,
            obstacles=obstacles
        )

        self.assertEqual(path_count, 0)
        self.assertEqual(path, [])

    def test_dp_grid_end_blocked(self):
        obstacles = {(2, 2)}

        dp_table, path_count, path = dynamic_programming_grid(
            rows=3,
            cols=3,
            obstacles=obstacles
        )

        self.assertEqual(path_count, 0)
        self.assertEqual(path, [])




# Benchmarking Tests


class TestBenchmarking(unittest.TestCase):


    def show_time(self, test_name, running_time):
        print(test_name + " runtime: " + format(running_time, ".6f") + " seconds")

    # Phase 1 benchmark

    def test_stack_benchmark(self):
        stack = []

        start_time = time.perf_counter()

        for value in range(5000):
            stack.append(value)

        for value in range(5000):
            stack.pop()

        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Stack push/pop benchmark", running_time)

        self.assertEqual(stack, [])
        self.assertLess(running_time, 1.0)

    def test_queue_benchmark(self):
        queue = []

        start_time = time.perf_counter()

        for value in range(1500):
            queue.append(value)

        removed_values = []

        for value in range(1500):
            removed_values.append(queue.pop(0))

        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Queue enqueue/dequeue benchmark", running_time)

        self.assertEqual(queue, [])
        self.assertEqual(removed_values[0], 0)
        self.assertEqual(removed_values[-1], 1499)
        self.assertLess(running_time, 2.0)

    def test_linked_list_benchmark(self):
        linked_list = LinkedList()

        start_time = time.perf_counter()

        for value in range(1000):
            linked_list.insert_end(value)

        linked_list.reverse()

        for value in range(500):
            linked_list.delete_head()

        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Linked list benchmark", running_time)

        self.assertEqual(linked_list.size, 500)
        self.assertLess(running_time, 3.0)

    # Phase 2 benchmark

    def test_bubble_sort_benchmark(self):
        data = list(range(80, 0, -1))

        start_time = time.perf_counter()
        result = get_final_array(bubble_sort_steps(data), data)
        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Bubble sort benchmark", running_time)

        self.assertEqual(result, sorted(data))
        self.assertLess(running_time, 2.0)

    def test_selection_sort_benchmark(self):
        data = list(range(80, 0, -1))

        start_time = time.perf_counter()
        result = get_final_array(selection_sort_steps(data), data)
        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Selection sort benchmark", running_time)

        self.assertEqual(result, sorted(data))
        self.assertLess(running_time, 2.0)

    def test_bfs_benchmark(self):
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"]
        }

        start_time = time.perf_counter()
        result = bfs(graph, "A")
        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("BFS benchmark", running_time)

        self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})
        self.assertLess(running_time, 1.0)

    def test_dfs_benchmark(self):
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"]
        }

        start_time = time.perf_counter()
        result = dfs(graph, "A")
        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("DFS benchmark", running_time)

        self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})
        self.assertLess(running_time, 1.0)

    # Phase 3 benchmark

    def test_dijkstra_benchmark(self):
        rows = 8
        cols = 8
        start = (0, 0)
        end = (7, 7)
        obstacles = {(1, 1), (2, 2), (3, 3), (4, 4)}

        start_time = time.perf_counter()

        visited_order, path = dijkstra_pathfinding(
            rows,
            cols,
            start,
            end,
            obstacles
        )

        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("Dijkstra benchmark", running_time)

        self.assertGreater(len(visited_order), 0)
        self.assertGreater(len(path), 0)
        self.assertLess(running_time, 1.0)

    def test_dynamic_programming_benchmark(self):
        rows = 8
        cols = 8
        obstacles = {(1, 1), (2, 2), (3, 3)}

        start_time = time.perf_counter()

        dp_table, path_count, path = dynamic_programming_grid(
            rows,
            cols,
            obstacles
        )

        end_time = time.perf_counter()

        running_time = end_time - start_time
        self.show_time("DP grid benchmark", running_time)

        self.assertIsInstance(dp_table, list)
        self.assertGreaterEqual(path_count, 0)
        self.assertLess(running_time, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)