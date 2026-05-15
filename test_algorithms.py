import os
import sys
import time
import unittest

# make pygame not open real window when testing
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

# let test file find project files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# import my modules, if some file name is missing then skip related tests
try:
    import stack_page as stack_module
except ImportError:
    stack_module = None

try:
    import queue_page as queue_module
except ImportError:
    queue_module = None

try:
    from linked_list_page import LinkedList
except ImportError:
    LinkedList = None

try:
    import sorting_algorithms_module as sorting_module
except ImportError:
    sorting_module = None

try:
    from graph_algorithms_module import BST
except ImportError:
    BST = None

try:
    import graph_traversal_module as graph_module
except ImportError:
    graph_module = None

try:
    import heap_priority_queue_module as heap_module
except ImportError:
    heap_module = None

try:
    import linear_search_page as linear_module
except ImportError:
    linear_module = None

try:
    import puzzle_module
except ImportError:
    puzzle_module = None


class TestStackAndQueue(unittest.TestCase):
    """Testing stack and queue simple logic."""

    @unittest.skipIf(stack_module is None, "stack_page.py not found")
    def test_stack_push_pop_order(self):
        stack = []

        stack.append(10)
        stack.append(20)
        stack.append(30)

        # stack is LIFO, last one goes out first
        self.assertEqual(stack.pop(), 30)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack, [10])

    @unittest.skipIf(stack_module is None, "stack_page.py not found")
    def test_stack_empty_check(self):
        stack = []

        # app should not pop when stack is empty
        self.assertEqual(len(stack), 0)
        self.assertTrue(len(stack) == 0)

    @unittest.skipIf(queue_module is None, "queue_page.py not found")
    def test_queue_enqueue_dequeue_order(self):
        queue = []

        queue.append(1)
        queue.append(2)
        queue.append(3)
        queue.append(4)

        # queue is FIFO, first one goes out first
        self.assertEqual(queue.pop(0), 1)
        self.assertEqual(queue.pop(0), 2)
        self.assertEqual(queue, [3, 4])

    @unittest.skipIf(queue_module is None, "queue_page.py not found")
    def test_queue_empty_check(self):
        queue = []

        # app should not dequeue when queue is empty
        self.assertEqual(len(queue), 0)
        self.assertTrue(len(queue) == 0)


class TestLinkedList(unittest.TestCase):
    """Testing linked list stuff."""

    @unittest.skipIf(LinkedList is None, "linked_list_page.py not found")
    def test_insert_end(self):
        ll = LinkedList()

        ll.insert_end(10)
        ll.insert_end(20)
        ll.insert_end(30)

        self.assertEqual(ll.to_list(), [10, 20, 30])

    @unittest.skipIf(LinkedList is None, "linked_list_page.py not found")
    def test_insert_at_position(self):
        ll = LinkedList()

        ll.insert_end(10)
        ll.insert_end(30)

        result = ll.insert_at_position(20, 1)

        self.assertTrue(result)
        self.assertEqual(ll.to_list(), [10, 20, 30])

    @unittest.skipIf(LinkedList is None, "linked_list_page.py not found")
    def test_delete_value(self):
        ll = LinkedList()

        ll.insert_end(5)
        ll.insert_end(10)
        ll.insert_end(15)

        removed = ll.delete_value(10)

        self.assertEqual(removed, 10)
        self.assertEqual(ll.to_list(), [5, 15])

    @unittest.skipIf(LinkedList is None, "linked_list_page.py not found")
    def test_reverse(self):
        ll = LinkedList()

        ll.insert_end(1)
        ll.insert_end(2)
        ll.insert_end(3)

        ll.reverse()

        self.assertEqual(ll.to_list(), [3, 2, 1])


class TestSortingAlgorithms(unittest.TestCase):
    #Testing sorting algorithm

    @unittest.skipIf(sorting_module is None, "sorting_algorithms_module.py not found")
    def test_bubble_sort_result(self):
        data = [5, 3, 8, 1, 2]

        steps = sorting_module.make_bubble_steps(data)
        final_array = steps[-1][0]

        self.assertEqual(final_array, [1, 2, 3, 5, 8])

    @unittest.skipIf(sorting_module is None, "sorting_algorithms_module.py not found")
    def test_selection_sort_result(self):
        data = [9, 4, 6, 1, 3]

        steps = sorting_module.make_selection_steps(data)
        final_array = steps[-1][0]

        self.assertEqual(final_array, [1, 3, 4, 6, 9])

    @unittest.skipIf(sorting_module is None, "sorting_algorithms_module.py not found")
    def test_merge_sort_result(self):
        data = [7, 2, 9, 1, 5]

        steps = sorting_module.make_merge_steps(data)
        final_array = steps[-1][0]

        self.assertEqual(final_array, [1, 2, 5, 7, 9])


class TestBSTAlgorithms(unittest.TestCase):
    #Testing BST

    @unittest.skipIf(BST is None, "graph_algorithms_module.py not found")
    def test_bst_inorder(self):
        bst = BST()

        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 70, 80])

    @unittest.skipIf(BST is None, "graph_algorithms_module.py not found")
    def test_bst_preorder_and_postorder(self):
        bst = BST()

        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        self.assertEqual(bst.preorder(), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(bst.postorder(), [20, 40, 30, 60, 80, 70, 50])

    @unittest.skipIf(BST is None, "graph_algorithms_module.py not found")
    def test_bst_search_path(self):
        bst = BST()

        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        path, found = bst.search_path(60)

        self.assertTrue(found)
        self.assertEqual(path, [50, 70, 60])

    @unittest.skipIf(BST is None, "graph_algorithms_module.py not found")
    def test_bst_delete_leaf_node(self):
        bst = BST()

        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        deleted = bst.delete(20)

        self.assertTrue(deleted)
        self.assertEqual(bst.inorder(), [30, 40, 50, 60, 70, 80])

    @unittest.skipIf(BST is None, "graph_algorithms_module.py not found")
    def test_bst_delete_two_child_node(self):
        bst = BST()

        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        deleted = bst.delete(70)

        self.assertTrue(deleted)
        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 80])


class TestGraphTraversal(unittest.TestCase):
    #Testing graph BFS  DFS

    @unittest.skipIf(graph_module is None, "graph_traversal_module.py not found")
    def test_bfs_order(self):
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"]
        }

        if hasattr(graph_module, "bfs"):
            result = graph_module.bfs(graph, "A")
            self.assertEqual(result, ["A", "B", "C", "D", "E", "F"])

        elif hasattr(graph_module, "make_bfs_steps"):
            steps = graph_module.make_bfs_steps("A")
            result = steps[-1]["order"]
            self.assertEqual(result, ["A", "B", "C", "D", "E", "F"])

        else:
            self.fail("No BFS function found")

    @unittest.skipIf(graph_module is None, "graph_traversal_module.py not found")
    def test_dfs_order_starts_correctly(self):
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"]
        }

        if hasattr(graph_module, "dfs"):
            result = graph_module.dfs(graph, "A")

            # not checking every dfs way too hard, just basic right
            self.assertEqual(result[0], "A")
            self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})

        elif hasattr(graph_module, "make_dfs_steps"):
            steps = graph_module.make_dfs_steps("A")
            result = steps[-1]["order"]

            self.assertEqual(result[0], "A")
            self.assertEqual(set(result), {"A", "B", "C", "D", "E", "F"})

        else:
            self.fail("No DFS function found")


class TestHeapPriorityQueue(unittest.TestCase):
    #Testing heap

    @unittest.skipIf(heap_module is None, "heap_priority_queue_module.py not found")
    def test_heap_extract_min_order(self):
        heap = []

        # event item = time, counter, description
        heap_module.heap_insert(heap, (5, 0, "Email"))
        heap_module.heap_insert(heap, (2, 1, "Meeting"))
        heap_module.heap_insert(heap, (8, 2, "Backup"))
        heap_module.heap_insert(heap, (1, 3, "Urgent"))

        first, _ = heap_module.heap_extract_min(heap)
        second, _ = heap_module.heap_extract_min(heap)

        self.assertEqual(first[0], 1)
        self.assertEqual(first[2], "Urgent")

        self.assertEqual(second[0], 2)
        self.assertEqual(second[2], "Meeting")

    @unittest.skipIf(heap_module is None, "heap_priority_queue_module.py not found")
    def test_heap_empty_extract(self):
        heap = []

        result, highlight = heap_module.heap_extract_min(heap)

        self.assertIsNone(result)
        self.assertEqual(highlight, [])


class TestLinearSearchInput(unittest.TestCase):
    #"Testing target input

    @unittest.skipIf(linear_module is None, "linear_search_page.py not found")
    def test_parse_multiple_targets_with_space(self):
        if not hasattr(linear_module, "parse_targets"):
            self.skipTest("parse_targets function not found")

        result = linear_module.parse_targets("7 3 10")

        self.assertEqual(result, [7, 3, 10])

    @unittest.skipIf(linear_module is None, "linear_search_page.py not found")
    def test_parse_multiple_targets_with_comma(self):
        if not hasattr(linear_module, "parse_targets"):
            self.skipTest("parse_targets function not found")

        result = linear_module.parse_targets("7,3,10")

        self.assertEqual(result, [7, 3, 10])


class TestPuzzleAndDynamicProgramming(unittest.TestCase):
    #Test puzzle

    @unittest.skipIf(puzzle_module is None, "puzzle_module.py not found")
    def test_dijkstra_pathfinding_basic(self):
        if not hasattr(puzzle_module, "dijkstra_pathfinding"):
            self.skipTest("dijkstra_pathfinding function not found")

        visited_order, path = puzzle_module.dijkstra_pathfinding(
            3,
            3,
            (0, 0),
            (2, 2),
            set()
        )

        self.assertGreater(len(visited_order), 0)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))

    @unittest.skipIf(puzzle_module is None, "puzzle_module.py not found")
    def test_dp_grid_path_count_no_obstacles(self):
        if not hasattr(puzzle_module, "dynamic_programming_grid"):
            self.skipTest("dynamic_programming_grid function not found")

        dp, path_count, path = puzzle_module.dynamic_programming_grid(
            3,
            3,
            set()
        )

        self.assertEqual(path_count, 6)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))

    @unittest.skipIf(puzzle_module is None, "puzzle_module.py not found")
    def test_dp_grid_with_obstacle(self):
        if not hasattr(puzzle_module, "dynamic_programming_grid"):
            self.skipTest("dynamic_programming_grid function not found")

        obstacles = {(1, 1)}

        dp, path_count, path = puzzle_module.dynamic_programming_grid(
            3,
            3,
            obstacles
        )

        self.assertEqual(path_count, 2)
        self.assertEqual(dp[1][1], 0)

        if path_count > 0:
            self.assertEqual(path[0], (0, 0))
            self.assertEqual(path[-1], (2, 2))

    @unittest.skipIf(puzzle_module is None, "puzzle_module.py not found")
    def test_coin_change_dp_result(self):
        if not hasattr(puzzle_module, "coin_change_dp_steps"):
            self.skipTest("coin_change_dp_steps function not found")

        steps, result = puzzle_module.coin_change_dp_steps([1, 2, 5], 5)

        self.assertEqual(result, 4)
        self.assertGreater(len(steps), 0)


class TestBenchmarks(unittest.TestCase):
    #Small benchmark, just for report screenshot

    def test_stack_queue_benchmark(self):
        stack = []
        queue = []

        start = time.perf_counter()

        for i in range(1000):
            stack.append(i)

        for i in range(1000):
            stack.pop()

        stack_time = time.perf_counter() - start

        start = time.perf_counter()

        for i in range(1000):
            queue.append(i)

        for i in range(1000):
            queue.pop(0)

        queue_time = time.perf_counter() - start

        print("\nBenchmark - Stack push/pop 1000 values:", round(stack_time, 6), "seconds")
        print("Benchmark - Queue enqueue/dequeue 1000 values:", round(queue_time, 6), "seconds")

        self.assertGreaterEqual(stack_time, 0)
        self.assertGreaterEqual(queue_time, 0)

    def test_sorting_benchmark(self):
        if sorting_module is None:
            self.skipTest("sorting module not found")

        data = [9, 4, 6, 2, 8, 1, 5, 3, 7]

        start = time.perf_counter()
        sorting_module.make_bubble_steps(data)
        bubble_time = time.perf_counter() - start

        start = time.perf_counter()
        sorting_module.make_selection_steps(data)
        selection_time = time.perf_counter() - start

        start = time.perf_counter()
        sorting_module.make_merge_steps(data)
        merge_time = time.perf_counter() - start

        print("\nBenchmark - Bubble Sort:", round(bubble_time, 6), "seconds")
        print("Benchmark - Selection Sort:", round(selection_time, 6), "seconds")
        print("Benchmark - Merge Sort:", round(merge_time, 6), "seconds")

        self.assertGreaterEqual(bubble_time, 0)
        self.assertGreaterEqual(selection_time, 0)
        self.assertGreaterEqual(merge_time, 0)

    def test_heap_benchmark(self):
        if heap_module is None:
            self.skipTest("heap module not found")

        heap = []

        start = time.perf_counter()

        for i in range(1000):
            heap_module.heap_insert(heap, (i, i, "Event"))

        for i in range(1000):
            heap_module.heap_extract_min(heap)

        elapsed = time.perf_counter() - start

        print("\nBenchmark - Heap insert/extract 1000 events:", round(elapsed, 6), "seconds")

        self.assertGreaterEqual(elapsed, 0)


if __name__ == "__main__":
    unittest.main()