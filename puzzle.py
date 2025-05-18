import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
from collections import deque
import time
import random
from random import choice
import math
import logging
from tkinter import messagebox
import csv
import os

def log_to_csv(algorithm_name, map_name, time_taken, steps, status="OK"):
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Algorithm", "Map", "Time (s)", "Steps", "Status"])
        writer.writerow([algorithm_name, map_name, f"{time_taken:.3f}", steps, status])

def get_current_map_name():
    if initial_state == [1, 2, 3, 4, 5, 6, 0, 7, 8]:
        return "Easy"
    elif initial_state == [1, 2, 3, 4, 0, 5, 6, 7, 8]:
        return "Medium"
    elif initial_state == [8, 6, 7, 2, 5, 4, 3, 0, 1]:
        return "Hard"
    else:
        return "Custom"


# ------------------------------
# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def bfs_solver(start_state, goal_state):
    queue = deque([(start_state, [])])  # Thay Queue bằng deque
    visited = set()
    visited.add(tuple(start_state))
    
    while queue:
        state, path = queue.popleft()  # popleft thay vì get
        if state == goal_state:
            return path
        for move, new_state in get_possible_moves(state):
            if tuple(new_state) not in visited:
                queue.append((new_state, path + [move]))
                visited.add(tuple(new_state))
    return None

def dfs_solver(start_state, goal_state, max_depth=30):
    stack = [(start_state, [], 0)]  # Thêm biến độ sâu
    visited = set()
    visited.add(tuple(start_state))

    while stack:
        state, path, depth = stack.pop()
        if state == goal_state:
            return path
        if depth >= max_depth:
            continue

        # Sắp xếp các bước theo heuristic tăng dần để ưu tiên nước đi tốt
        moves = get_possible_moves(state)
        moves.sort(key=lambda x: heuristic(x[1], goal_state))

        for move, new_state in reversed(moves):  # reversed vì DFS dùng stack
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                stack.append((new_state, path + [move], depth + 1))

    return None

def ucs_solver(start_state, goal_state):
    pq = PriorityQueue()
    pq.put((0, start_state, []))
    visited = set()
    visited.add(tuple(start_state))
    
    while not pq.empty():
        cost, state, path = pq.get()
        if state == goal_state:
            return path
        for move, new_state in get_possible_moves(state):
            if tuple(new_state) not in visited:
                pq.put((cost + 1, new_state, path + [move]))
                visited.add(tuple(new_state))
    return None

def heuristic(state, goal_state):
    total_distance = 0
    for i in range(9):
        if state[i] != 0:
            current_row, current_col = i // 3, i % 3
            goal_pos = goal_state.index(state[i])
            goal_row, goal_col = goal_pos // 3, goal_pos % 3
            total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return total_distance

def greedy_best_first_search(start_state, goal_state):
    pq = PriorityQueue()
    pq.put((heuristic(start_state, goal_state), start_state, []))
    visited = set()
    
    while not pq.empty():
        h, state, path = pq.get()  # Unpack đầy đủ: heuristic, state, path
        if state == goal_state:
            return path
        if tuple(state) not in visited:
            visited.add(tuple(state))
            for move, new_state in get_possible_moves(state):
                if tuple(new_state) not in visited:
                    pq.put((heuristic(new_state, goal_state), new_state, path + [move]))
    return None

def a_star_solver(start_state, goal_state):
    pq = PriorityQueue()
    pq.put((heuristic(start_state, goal_state), 0, start_state, []))
    visited = set()
    
    while not pq.empty():
        _, cost, state, path = pq.get()
        if state == goal_state:
            return path
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        for move, new_state in get_possible_moves(state):
            pq.put((cost + heuristic(new_state, goal_state), cost + 1, new_state, path + [move]))
    return None

def ida_star_solver(start_state, goal_state):
    def search(state, g, threshold, path):
        nonlocal visited  # Khai báo nonlocal để sử dụng visited từ scope ngoài
        f = g + heuristic(state, goal_state)
        if f > threshold:
            return f, None
        if state == goal_state:
            return f, path
        min_cost = float('inf')
        for move, new_state in get_possible_moves(state):
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                t, res_path = search(new_state, g + 1, threshold, path + [move])
                if res_path is not None:
                    return t, res_path
                if t < min_cost:
                    min_cost = t
                visited.remove(tuple(new_state))
        return min_cost, None
    
    threshold = heuristic(start_state, goal_state)
    while True:
        visited = {tuple(start_state)}
        t, result = search(start_state, 0, threshold, [])
        if result is not None:
            return result
        if t == float('inf'):
            return None
        threshold = t

def ids_solver(start_state, goal_state):
    def dls(state, path, depth, depth_limit, visited):
        if state == goal_state:
            return path
        if depth > depth_limit:
            return None
        
        for move, new_state in get_possible_moves(state):
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                result = dls(new_state, path + [move], depth + 1, depth_limit, visited)
                if result is not None:
                    return result
                visited.remove(tuple(new_state))
        return None
    
    depth_limit = 0
    while True:
        visited = {tuple(start_state)}
        result = dls(start_state, [], 0, depth_limit, visited)
        if result is not None:
            return result
        depth_limit += 1

def simple_hill_climbing_solver(start_state, goal_state):
    current_state = start_state[:]
    path = []
    max_iterations = 1000
    iterations = 0
    
    while current_state != goal_state and iterations < max_iterations:
        possible_moves = get_possible_moves(current_state)
        best_move = None
        best_heuristic = heuristic(current_state, goal_state)
        
        for move, new_state in possible_moves:
            h = heuristic(new_state, goal_state)
            if h < best_heuristic:
                best_move = (move, new_state)
                best_heuristic = h
        
        if best_move is None:
            return None  # Không tìm thấy nước đi tốt hơn, dừng lại
        
        move_text, current_state = best_move
        path.append(move_text)
        iterations += 1
    
    return path if current_state == goal_state else None

def steepest_ascent_hill_climbing_solver(start_state, goal_state):
    current_state = start_state[:]
    path = []
    max_iterations = 1000
    iterations = 0
    
    while current_state != goal_state and iterations < max_iterations:
        possible_moves = get_possible_moves(current_state)
        best_move = None
        best_heuristic = heuristic(current_state, goal_state)
        
        for move, new_state in possible_moves:
            h = heuristic(new_state, goal_state)
            if h < best_heuristic:
                best_move = (move, new_state)
                best_heuristic = h
        
        if best_move is None:
            return None
        
        move_text, current_state = best_move
        path.append(move_text)
        iterations += 1
    
    return path if current_state == goal_state else None

def stochastic_hill_climbing_solver(start_state, goal_state):
    current_state = start_state[:]
    path = []
    max_iterations = 2000  # Tăng số lần lặp để khám phá nhiều hơn
    iterations = 0
    random_move_prob = 0.2  # Xác suất chọn nước đi ngẫu nhiên khi kẹt
    
    while current_state != goal_state and iterations < max_iterations:
        possible_moves = get_possible_moves(current_state)
        current_heuristic = heuristic(current_state, goal_state)
        # Chỉ chọn các nước đi cải thiện heuristic
        better_moves = [(move, new_state) for move, new_state in possible_moves if heuristic(new_state, goal_state) < current_heuristic]
        
        if better_moves:
            move_text, current_state = random.choice(better_moves)
        else:
            # Nếu không có nước đi cải thiện, thử ngẫu nhiên với xác suất
            if random.random() < random_move_prob and possible_moves:
                move_text, current_state = random.choice(possible_moves)
            else:
                return None
        
        path.append(move_text)
        iterations += 1
    
    return path if current_state == goal_state else None

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    # Tăng khả năng chấp nhận trạng thái tệ hơn ở nhiệt độ cao
    return math.exp(-((new_cost - old_cost) / temperature) * 0.5)  # Nhân với 0.5 để tăng xác suất

def simulated_annealing_solver(start_state, goal_state):
    current_state = start_state[:]
    path = []
    T = 20.0
    T_min = 0.001
    alpha = 0.95
    max_iterations_per_temp = 300
    max_total_steps = 3000

    visited = set()
    current_heuristic = heuristic(current_state, goal_state)
    total_steps = 0

    while T > T_min:
        i = 1
        while i <= max_iterations_per_temp:
            if total_steps >= max_total_steps:
                print("SA dừng vì vượt quá tổng số bước cho phép.")
                return None

            possible_moves = get_possible_moves(current_state)
            if not possible_moves:
                return None

            move_text, next_state = random.choice(possible_moves)
            next_heuristic = heuristic(next_state, goal_state)
            ap = acceptance_probability(current_heuristic, next_heuristic, T)

            if ap > random.random():
                current_state = next_state
                current_heuristic = next_heuristic
                path.append(move_text)

                if current_state == goal_state:
                    return path

            i += 1
            total_steps += 1
        T *= alpha

    return path if current_state == goal_state else None


# Sau các hàm như bfs_solver, a_star_solver, v.v.
def beam_search_solver(start_state, goal_state, beam_width=3):
    current_states = [(start_state, [])]
    visited = set()
    visited.add(tuple(start_state))
    
    while current_states:
        next_states = []
        for state, path in current_states:
            if state == goal_state:
                return path
            for move, new_state in get_possible_moves(state):
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    next_states.append((new_state, path + [move]))
        next_states.sort(key=lambda x: heuristic(x[0], goal_state))
        current_states = next_states[:beam_width]
    
    return None

def belief_state_heuristic(belief_state, goal_state):
    if not belief_state:
        return float('inf')
    heuristics = [heuristic(list(state), goal_state) for state in belief_state]
    return sum(heuristics) / len(heuristics)

def belief_state_solver(start_state, goal_state, beam_width=3):
    """
    Belief State Search cho 8-Puzzle, sử dụng trạng thái duy nhất làm belief state ban đầu.
    """
    logger.info(f"Starting belief state search with initial state: {start_state}")
    pq = PriorityQueue()
    initial_belief_state = {tuple(start_state)}
    pq.put((belief_state_heuristic(initial_belief_state, goal_state), initial_belief_state, []))
    visited = set()
    nodes_expanded = 0
    max_nodes = 5000
    
    while not pq.empty():
        h, current_belief_state, path = pq.get()
        nodes_expanded += 1
        logger.info(f"Expanding node {nodes_expanded}, belief state size: {len(current_belief_state)}")
        
        if nodes_expanded > max_nodes:
            logger.warning("Reached maximum nodes limit")
            return None
            
        belief_state_key = frozenset(current_belief_state)
        if belief_state_key in visited:
            continue
        visited.add(belief_state_key)
        
        for state in current_belief_state:
            if list(state) == goal_state:
                logger.info(f"Solution found with path: {path}")
                return path
        
        next_belief_states = {}
        for state in current_belief_state:
            for move, new_state in get_possible_moves(list(state)):
                if is_solvable(new_state, goal_state):
                    if move not in next_belief_states:
                        next_belief_states[move] = set()
                    next_belief_states[move].add(tuple(new_state))
        
        for move, new_belief_state in next_belief_states.items():
            if len(new_belief_state) > beam_width:
                new_belief_state_list = list(new_belief_state)
                new_belief_state_list.sort(key=lambda x: heuristic(list(x), goal_state))
                new_belief_state = set(new_belief_state_list[:beam_width])
            h_value = belief_state_heuristic(new_belief_state, goal_state)
            pq.put((h_value, new_belief_state, path + [move]))
        
        if pq.qsize() > 5000:
            logger.warning("Priority queue size exceeded limit")
            return None
    
    logger.info("No solution found")
    return None


def backtracking_solver(start_state, goal_state):
    start_time = time.time()
    timeout = 30  # Giới hạn 30 giây
    def backtrack(state, path, visited, depth, max_depth=50):
        if time.time() - start_time > timeout:
            logger.warning("Timeout reached")
            return None
        logger.info(f"Depth {depth}, state: {state}")
        if state == goal_state:
            logger.info("Solution found at depth: {}".format(depth))
            return path
        if depth > max_depth:
            logger.info("Reached max depth: {}".format(max_depth))
            return None
        
        for move, new_state in get_possible_moves(state):
            if tuple(new_state) not in visited and is_solvable(new_state, goal_state):
                visited.add(tuple(new_state))
                result = backtrack(new_state, path + [move], visited, depth + 1, max_depth)
                if result is not None:
                    return result
                visited.remove(tuple(new_state))
        return None
    
    visited = {tuple(start_state)}
    depth_limit = 0
    max_iterations = 50
    while depth_limit <= max_iterations:
        logger.info(f"Exploring depth limit: {depth_limit}")
        result = backtrack(start_state, [], visited, 0, depth_limit)
        if result is not None:
            logger.info(f"Solution found with path length: {len(result)}")
            return result
        if time.time() - start_time > timeout:
            logger.warning("Timeout reached")
            return None
        depth_limit += 1
        visited = {tuple(start_state)}
    logger.warning("No solution found within depth limit")
    return None

def backtracking_for_checking_solver(start_state, goal_state):
    def is_valid_state(state, visited):
        # Kiểm tra ràng buộc: trạng thái phải khả giải và chưa được thăm
        return is_solvable(state, goal_state) and tuple(state) not in visited

    def backtrack(state, path, visited):
        if state == goal_state:
            logger.info(f"Solution found with path: {path}")
            return path
        
        visited.add(tuple(state))
        possible_moves = get_possible_moves(state)
        for move, new_state in possible_moves:
            if is_valid_state(new_state, visited):
                result = backtrack(new_state, path + [move], visited)
                if result is not None:
                    return result
        visited.remove(tuple(state))
        return None

    logger.info(f"Starting backtracking for checking with initial state: {start_state}")
    return backtrack(start_state, [], set())

def and_or_search_solver(start_state, goal_state):
    """
    AND-OR Search cho 8-Puzzle.
    """
    logger.info(f"Starting AND-OR search with initial state: {start_state}")
    
    def solve_node(state, visited, path, depth=0, max_depth=30):
        if state == goal_state:
            return {"state": state, "move": None, "children": []}
        
        if depth > max_depth:
            return None

        state_tuple = tuple(state)
        if state_tuple in visited:
            return None

        visited.add(state_tuple)

        for move, new_state in get_possible_moves(state):
            if not is_solvable(new_state, goal_state):
                continue
            if tuple(new_state) in visited:
                continue

            child_solution = solve_node(new_state, visited, path + [move], depth + 1, max_depth)
            if child_solution:
                return {
                    "state": state,
                    "move": move,
                    "children": [child_solution]
                }

        visited.remove(state_tuple)
        return None


    def extract_path(solution):
        path = []
        def traverse(node):
            if node["move"]:
                path.append(node["move"])
            for child in node["children"]:
                traverse(child)
        if solution:
            traverse(solution)
        return path

    visited = set()
    solution_tree = solve_node(start_state, visited, [], depth=0, max_depth=30)
    if solution_tree:
        logger.info(f"Solution found with path: {extract_path(solution_tree)}")
    else:
        logger.info("No solution found")
    return extract_path(solution_tree)

    
def partially_observable_search_solver(start_state, goal_state, beam_width=3):
    """
    Tìm kiếm trong môi trường quan sát không đầy đủ cho 8-Puzzle.
    Sử dụng trạng thái duy nhất làm belief state ban đầu.
    """
    logger.info(f"Starting partially observable search with initial state: {start_state}")
    pq = PriorityQueue()
    initial_belief_state = {tuple(start_state)}
    pq.put((belief_state_heuristic(initial_belief_state, goal_state), initial_belief_state, []))
    visited = set()
    nodes_expanded = 0
    max_nodes = 5000
    
    while not pq.empty():
        h, current_belief_state, path = pq.get()
        nodes_expanded += 1
        logger.info(f"Expanding node {nodes_expanded}, belief state size: {len(current_belief_state)}")
        
        if nodes_expanded > max_nodes:
            logger.warning("Reached maximum nodes limit")
            return None
            
        belief_state_key = frozenset(current_belief_state)
        if belief_state_key in visited:
            continue
        visited.add(belief_state_key)
        
        for state in current_belief_state:
            if list(state) == goal_state:
                logger.info(f"Solution found with path: {path}")
                return path
        
        next_belief_states = {}
        for state in current_belief_state:
            for move, new_state in get_possible_moves(list(state)):
                if is_solvable(new_state, goal_state):
                    if move not in next_belief_states:
                        next_belief_states[move] = set()
                    next_belief_states[move].add(tuple(new_state))
        
        for move, new_belief_state in next_belief_states.items():
            if len(new_belief_state) > beam_width:
                new_belief_state_list = list(new_belief_state)
                new_belief_state_list.sort(key=lambda x: heuristic(list(x), goal_state))
                new_belief_state = set(new_belief_state_list[:beam_width])
            h_value = belief_state_heuristic(new_belief_state, goal_state)
            pq.put((h_value, new_belief_state, path + [move]))
        
        if pq.qsize() > 5000:
            logger.warning("Priority queue size exceeded limit")
            return None
    
    logger.info("No solution found")
    return None

def solve_puzzle_belief_state():
    global current_state
    logger.info(f"Current state: {current_state}")
    if not is_solvable(current_state, goal_state):
        messagebox.showerror("Lỗi", "Trạng thái ban đầu không khả giải!")
        logger.error("Initial state is not solvable")
        return
    
    start_time = time.time()
    solution = belief_state_solver(current_state, goal_state, beam_width=3)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time:.3f} seconds")
    # --- Ghi log CSV ---
    steps_count = len(solution) if solution else 0
    log_to_csv(
        algorithm_name="Belief State Search",
        map_name=get_current_map_name(),
        time_taken=execution_time,
        steps=steps_count,
        status="OK" if solution else "Fail",
    )
    
    time_label.config(text=f"Thời gian thực thi: {execution_time:.3f} giây")
    steps_count_label.config(text=f"Số bước đi: {steps_count}")
    
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    
    if solution:
        def show_step(index):
            global current_state
            if index >= len(solution):
                steps_text.config(state=tk.DISABLED)
                logger.info("Finished displaying solution")
                return
            move = solution[index]
            logger.info(f"Attempting move {index + 1}: {move}")
            valid_moves = get_possible_moves(current_state)
            valid_move_descs = [desc for desc, _ in valid_moves]
            if move not in valid_move_descs:
                messagebox.showerror("Lỗi", f"Bước đi không hợp lệ: {move}\nValid moves: {valid_move_descs}")
                logger.error(f"Invalid move: {move}, valid moves: {valid_move_descs}")
                return
            current_state = next(new for desc, new in valid_moves if desc == move)
            update_ui(current_state, move)
            steps_text.insert(tk.END, f"{move}\n")
            steps_text.see(tk.END)
            root.update()
            root.after(500, show_step, index + 1)
        
        show_step(0)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy lời giải!")
        logger.error("No solution found")

def solve_puzzle_and_or():
    global current_state
    logger.info(f"Current state: {current_state}")
    if not is_solvable(current_state, goal_state):
        messagebox.showerror("Lỗi", "Trạng thái ban đầu không khả giải!")
        logger.error("Initial state is not solvable")
        return
    
    start_time = time.time()
    solution = and_or_search_solver(current_state, goal_state)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time:.3f} seconds")

        # Ghi log vào CSV
    steps_count = len(solution) if solution else 0
    log_to_csv(
        algorithm_name="AND-OR Search",
        map_name=get_current_map_name(),
        time_taken=execution_time,
        steps=steps_count,
        status="OK" if solution else "Fail",
    )
    
    time_label.config(text=f"Thời gian thực thi: {execution_time:.3f} giây")
    steps_count_label.config(text=f"Số bước đi: {steps_count}")

    
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    
    if solution:
        def show_step(index):
            global current_state
            if index >= len(solution):
                steps_text.config(state=tk.DISABLED)
                logger.info("Finished displaying solution")
                return
            move = solution[index]
            logger.info(f"Attempting move {index + 1}: {move}")
            valid_moves = get_possible_moves(current_state)
            valid_move_descs = [desc for desc, _ in valid_moves]
            if move not in valid_move_descs:
                messagebox.showerror("Lỗi", f"Bước đi không hợp lệ: {move}\nValid moves: {valid_move_descs}")
                logger.error(f"Invalid move: {move}, valid moves: {valid_move_descs}")
                return
            current_state = next(new for desc, new in valid_moves if desc == move)
            update_ui(current_state, move)
            steps_text.insert(tk.END, f"{move}\n")
            steps_text.see(tk.END)
            root.update()
            root.after(500, show_step, index + 1)
        
        show_step(0)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy lời giải!")
        logger.error("No solution found")

def solve_puzzle_partially_observable():
    global current_state
    logger.info(f"Current state: {current_state}")
    if not is_solvable(current_state, goal_state):
        messagebox.showerror("Lỗi", "Trạng thái ban đầu không khả giải!")
        logger.error("Initial state is not solvable")
        return
    
    start_time = time.time()
    solution = partially_observable_search_solver(current_state, goal_state, beam_width=3)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time:.3f} seconds")

    steps_count = len(solution) if solution else 0
    log_to_csv(
        algorithm_name="Partially Observable Search",
        map_name=get_current_map_name(),
        time_taken=execution_time,
        steps=steps_count,
        status="OK" if solution else "Fail",
    )
    
    time_label.config(text=f"Thời gian thực thi: {execution_time:.3f} giây")
    steps_count_label.config(text=f"Số bước đi: {steps_count}")

    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    
    if solution:
        def show_step(index):
            global current_state
            if index >= len(solution):
                steps_text.config(state=tk.DISABLED)
                logger.info("Finished displaying solution")
                return
            move = solution[index]
            logger.info(f"Attempting move {index + 1}: {move}")
            valid_moves = get_possible_moves(current_state)
            valid_move_descs = [desc for desc, _ in valid_moves]
            if move not in valid_move_descs:
                messagebox.showerror("Lỗi", f"Bước đi không hợp lệ: {move}\nValid moves: {valid_move_descs}")
                logger.error(f"Invalid move: {move}, valid moves: {valid_move_descs}")
                return
            current_state = next(new for desc, new in valid_moves if desc == move)
            update_ui(current_state, move)
            steps_text.insert(tk.END, f"{move}\n")
            steps_text.see(tk.END)
            root.update()
            root.after(500, show_step, index + 1)
        
        show_step(0)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy lời giải!")
        logger.error("No solution found")

def solve_puzzle_backtracking():
    global current_state
    logger.info(f"Current state: {current_state}")
    if not is_solvable(current_state, goal_state):
        messagebox.showerror("Lỗi", "Trạng thái ban đầu không khả giải!")
        logger.error("Initial state is not solvable")
        return
    
    start_time = time.time()
    solution = backtracking_solver(current_state, goal_state)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time:.3f} seconds")
    steps_count = len(solution) if solution else 0
    log_to_csv(
        algorithm_name="Backtracking",
        map_name=get_current_map_name(),
        time_taken=execution_time,
        steps=steps_count,
        status="OK" if solution else "Fail",
    )
    
    time_label.config(text=f"Thời gian thực thi: {execution_time:.3f} giây")
    
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
  
    if solution:
        def show_step(index):
            global current_state
            if index >= len(solution):
                steps_text.config(state=tk.DISABLED)
                logger.info("Finished displaying solution")
                return
            move = solution[index]
            logger.info(f"Attempting move {index + 1}: {move}")
            valid_moves = get_possible_moves(current_state)
            valid_move_descs = [desc for desc, _ in valid_moves]
            if move not in valid_move_descs:
                messagebox.showerror("Lỗi", f"Bước đi không hợp lệ: {move}\nValid moves: {valid_move_descs}")
                logger.error(f"Invalid move: {move}, valid moves: {valid_move_descs}")
                return
            current_state = next(new for desc, new in valid_moves if desc == move)
            update_ui(current_state, move)
            steps_text.insert(tk.END, f"{move}\n")
            steps_text.see(tk.END)
            root.update()
            root.after(500, show_step, index + 1)
        
        show_step(0)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy lời giải trong giới hạn độ sâu!")
        logger.error("No solution found within depth limit")

def q_learning_solver(start_state, goal_state, episodes=5000, alpha=0.1, gamma=0.9, epsilon=0.1):
    # Khởi tạo bảng Q
    Q = {}
    
    def get_q_value(state, action):
        state_tuple = tuple(state)
        if (state_tuple, action) not in Q:
            Q[(state_tuple, action)] = 0.0
        return Q[(state_tuple, action)]
    
    def choose_action(state, possible_moves, epsilon):
        if random.random() < epsilon:  # Khám phá
            return random.choice(possible_moves)[0]
        else:  # Khai thác
            q_values = [(get_q_value(state, move), move) for move, _ in possible_moves]
            return max(q_values, key=lambda x: x[0])[1]
    
    # Huấn luyện Q-learning
    for episode in range(episodes):
        current_state = start_state[:]
        while current_state != goal_state:
            possible_moves = get_possible_moves(current_state)
            if not possible_moves:
                break
            
            # Chọn hành động
            action = choose_action(current_state, possible_moves, epsilon)
            _, next_state = next((move, new_state) for move, new_state in possible_moves if move == action)
            
            # Tính phần thưởng
            reward = -heuristic(next_state, goal_state)  # Phần thưởng âm dựa trên heuristic
            if next_state == goal_state:
                reward = 100  # Phần thưởng lớn khi đạt mục tiêu
            
            # Cập nhật Q-value
            future_q = max([get_q_value(next_state, move) for move, _ in get_possible_moves(next_state)], default=0)
            current_q = get_q_value(current_state, action)
            Q[(tuple(current_state), action)] = current_q + alpha * (reward + gamma * future_q - current_q)
            
            current_state = next_state
        
        # Giảm epsilon để giảm khám phá theo thời gian
        epsilon = max(0.01, epsilon * 0.995)
    
    # Sử dụng bảng Q để tìm đường đi
    current_state = start_state[:]
    path = []
    max_steps = 100  # Giới hạn số bước để tránh vòng lặp vô hạn
    
    for _ in range(max_steps):
        if current_state == goal_state:
            break
        
        possible_moves = get_possible_moves(current_state)
        if not possible_moves:
            return None
        
        # Chọn hành động tốt nhất từ bảng Q
        q_values = [(get_q_value(current_state, move), move) for move, _ in possible_moves]
        action = max(q_values, key=lambda x: x[0])[1]
        move_text, next_state = next((move, new_state) for move, new_state in possible_moves if move == action)
        
        path.append(move_text)
        current_state = next_state
    
    return path if current_state == goal_state else None

# ------------------------------
# Hàm hỗ trợ xử lý di chuyển trong 8-Puzzle
# ------------------------------

def get_possible_moves(state):
    moves = []
    index = state.index(0)  # Ô trống
    row, col = index // 3, index % 3
    directions = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}
    action_map = {'L': 'sang phải.', 'R': 'sang trái.', 'U': 'xuống dưới.', 'D': 'lên trên.'}
    
    for move, (dr, dc) in directions.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = state[:]
            new_index = new_row * 3 + new_col
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            moves.append((f"Số {new_state[index]} {action_map[move]}", new_state))
    
    return moves

# ------------------------------
# Xây dựng giao diện Tkinter
# ------------------------------

def update_ui(state, move_text=""):
    for i in range(9):
        text = "" if state[i] == 0 else str(state[i])
        border_color = "#FF9999"  # Hồng đậm cho viền (giữ nguyên)
        fill_color = "#FF9999"    # Hồng đậm cho ô có số (đổi từ #FFE6E6)
        empty_color = "#FFCCCC"   # Hồng trung bình cho ô trống (đổi từ #FFF5F5)

        buttons[i].config(
            text=text,
            bg=empty_color if state[i] == 0 else fill_color,
            fg="black",  # Có thể đổi thành "white" nếu muốn tương phản hơn
            font=("Arial", 14, "bold"),
            borderwidth=3,
            relief="ridge",
            highlightbackground=border_color,
        )
    move_label.config(text=move_text)

# Hàm để thay đổi màu nút khi hover
def on_enter(btn, original_color, hover_color):
    btn.config(bg=hover_color)

def on_leave(btn, original_color, hover_color):
    btn.config(bg=original_color)

def solve_puzzle(algorithm):
    global current_state
    logger.info(f"Current state: {current_state}")
    if not is_solvable(current_state, goal_state):
        messagebox.showerror("Lỗi", "Trạng thái ban đầu không khả giải!")
        logger.error("Initial state is not solvable")
        return
    
    start_time = time.time()
    solution = algorithm(initial_state, goal_state)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Execution time: {execution_time:.3f} seconds")

    # Ghi log vào CSV
    algorithm_name = algorithm.__name__ if hasattr(algorithm, '__name__') else str(algorithm)
    map_name = get_current_map_name()  # bạn sẽ tạo hàm nhỏ này bên dưới
    steps_count = len(solution) if solution else 0
    log_to_csv(algorithm_name, map_name, execution_time, steps_count, status="OK" if solution else "Fail")

    
    time_label.config(text=f"Thời gian thực thi: {execution_time:.3f} giây")
    steps_count_label.config(text="Số bước đi: 0")  # Reset số bước
    
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    
    if solution:
        step_count = 0  # Khởi tạo biến đếm
        def show_step(index):
            nonlocal step_count  # Sử dụng biến đếm
            global current_state
            if index >= len(solution):
                steps_text.config(state=tk.DISABLED)
                logger.info("Finished displaying solution")
                return
            move = solution[index]
            logger.info(f"Attempting move {index + 1}: {move}")
            valid_moves = get_possible_moves(current_state)
            valid_move_descs = [desc for desc, _ in valid_moves]
            if move not in valid_move_descs:
                messagebox.showerror("Lỗi", f"Bước đi không hợp lệ: {move}\nValid moves: {valid_move_descs}")
                logger.error(f"Invalid move: {move}, valid moves: {valid_move_descs}")
                return
            current_state = next(new for desc, new in valid_moves if desc == move)
            update_ui(current_state, move)
            step_count += 1  # Tăng số bước
            steps_count_label.config(text=f"Số bước đi: {step_count}")  # Cập nhật label
            steps_text.insert(tk.END, f"{move}\n")
            steps_text.see(tk.END)
            root.update()
            root.after(500, show_step, index + 1)
        
        show_step(0)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy lời giải!")
        logger.error("No solution found")

def reset_puzzle():
    global current_state
    current_state = initial_state[:]
    update_ui(current_state, "Reset về trạng thái ban đầu.")
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    steps_text.config(state=tk.DISABLED)

# ------------------------------
# Hàm tạo ma trận hiển thị
# ------------------------------
def create_matrix_display(frame, state):
    labels = []
    for i in range(9):
        text = "" if state[i] == 0 else str(state[i])
        label = tk.Label(
            frame,
            text=text,
            font=("Arial", 12, "bold"),
            width=4,
            height=2,
            relief="ridge",
            bg="#FFE6E6" if state[i] == 0 else "#FFD6D6",
            fg="black",
            borderwidth=2,
            highlightbackground="#FF9999",
        )
        label.grid(row=i // 3, column=i % 3, padx=2, pady=2)
        labels.append(label)
    return labels

# ------------------------------
# Hàm kiểm tra tính khả giải
# ------------------------------
def is_solvable(state, goal_state):
    def count_inversions(state):
        flat_state = [num for num in state if num != 0]  # Loại bỏ ô trống
        inversions = sum(
            1 for i in range(len(flat_state)) for j in range(i + 1, len(flat_state)) if flat_state[i] > flat_state[j]
        )
        return inversions
    
    # Tính số hoán vị của trạng thái ban đầu và đích
    initial_inversions = count_inversions(state)
    goal_inversions = count_inversions(goal_state)
    
    # Trạng thái khả giải nếu số hoán vị có cùng tính chẵn lẻ
    return (initial_inversions % 2) == (goal_inversions % 2)

# ------------------------------
# Hàm nhập trạng thái ban đầu
# ------------------------------
def input_initial_state():
    def submit_state():
        try:
            input_values = [int(entry.get()) for entry in entries]
            if len(input_values) != 9:
                messagebox.showerror("Lỗi", "Phải nhập đúng 9 số!")
                return
            if sorted(input_values) != list(range(9)):
                messagebox.showerror("Lỗi", "Phải nhập các số từ 0 đến 8, mỗi số xuất hiện đúng một lần!")
                return
            if not is_solvable(input_values):
                messagebox.showerror("Lỗi", "Trạng thái không thể giải được!")
                return
            global initial_state, current_state
            initial_state = input_values[:]
            current_state = initial_state[:]
            # Cập nhật initial_labels
            for i in range(9):
                text = "" if initial_state[i] == 0 else str(initial_state[i])
                initial_labels[i].config(
                    text=text,
                    bg="#FFCCCC" if initial_state[i] == 0 else "#FF9999",  # Đồng bộ màu
                    fg="black"
                )
            update_ui(current_state, "Đã nhập trạng thái mới")
            steps_text.config(state=tk.NORMAL)
            steps_text.delete("1.0", tk.END)
            steps_text.config(state=tk.DISABLED)
            input_window.destroy()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập các số hợp lệ (0-8)!")
    
    input_window = tk.Toplevel(root)
    input_window.title("Nhập trạng thái ban đầu")
    input_window.geometry("300x400")
    input_window.configure(bg="#FFE6E6")

    tk.Label(input_window, text="Nhập trạng thái ban đầu (9 số từ 0-8):", font=("Arial", 12, "bold"), bg="#FFE6E6", fg="black").pack(pady=10)

    entries = []
    entry_frame = tk.Frame(input_window, bg="#FFE6E6")
    entry_frame.pack(pady=10)
    for i in range(3):
        for j in range(3):
            entry = tk.Entry(entry_frame, width=5, font=("Arial", 14), bg="#FFF5F5", fg="black", bd=1, relief="sunken")
            entry.grid(row=i, column=j, padx=5, pady=5)
            entries.append(entry)

    submit_btn = tk.Button(input_window, text="Xác nhận", command=submit_state, bg=button_color, font=("Arial", 12))
    submit_btn.pack(pady=10)
    submit_btn.bind("<Enter>", lambda e: on_enter(submit_btn, button_color, hover_color))
    submit_btn.bind("<Leave>", lambda e: on_leave(submit_btn, button_color, hover_color))

# ------------------------------
# Hàm xử lý chọn map
# ------------------------------
def select_map_easy():
    global initial_state, current_state
    initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # Trạng thái Dễ: 123456078
    current_state = initial_state[:]
    for i in range(9):
        text = "" if initial_state[i] == 0 else str(initial_state[i])
        color = "#FFE6E6" if initial_state[i] == 0 else "#FFD6D6"
        initial_labels[i].config(text=text, bg=color, fg="black")

    update_ui(current_state, "Easy map selected")
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    steps_text.config(state=tk.DISABLED)

def select_map_medium():
    global initial_state, current_state
    initial_state = [1, 2, 3, 4, 0, 5, 6, 7, 8]  # Trạng thái Trung bình: 123405678
    current_state = initial_state[:]
    for i in range(9):
        text = "" if initial_state[i] == 0 else str(initial_state[i])
        color = "#FFE6E6" if initial_state[i] == 0 else "#FFD6D6"
        initial_labels[i].config(text=text, bg=color, fg="black")
    update_ui(current_state, "Medium map selected")
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    steps_text.config(state=tk.DISABLED)

def select_map_hard():
    global initial_state, current_state
    initial_state = [8, 6, 7, 2, 5, 4, 3, 0, 1]  # Trạng thái Khó mới: 867254301 (~20 bước)
    current_state = initial_state[:]
    for i in range(9):
        text = "" if initial_state[i] == 0 else str(initial_state[i])
        color = "#FFE6E6" if initial_state[i] == 0 else "#FFD6D6"
        initial_labels[i].config(text=text, bg=color, fg="black")
    update_ui(current_state, "Hard map selected")
    steps_text.config(state=tk.NORMAL)
    steps_text.delete("1.0", tk.END)
    steps_text.config(state=tk.DISABLED)

# ------------------------------
# Khởi tạo giao diện
# ------------------------------
root = tk.Tk()
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
root.title("8-Puzzle Solver")
root.geometry("600x650")
root.configure(bg="#FFE6E6")

# Trạng thái ban đầu & Trạng thái đích
initial_state = [1, 2, 3, 4, 0, 5, 6, 7, 8]  # Mặc định là trạng thái Trung bình
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
current_state = initial_state[:]

# Chia giao diện thành 2 cột
main_container = tk.Frame(root, bg="#FFE6E6")
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# Cột trái: Các ma trận
left_frame = tk.Frame(main_container, bg="#FFE6E6", width=200)
left_frame.pack(side=tk.LEFT, fill="y", padx=(0, 10))

# Cột phải: Nút, thời gian, bước đi
right_frame = tk.Frame(main_container, bg="#FFE6E6")
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

# Cột trái: Các ma trận
initial_label = tk.Label(left_frame, text="Trạng thái ban đầu", font=("Arial", 12, "bold"), bg="#FFE6E6", fg="black")
initial_label.pack(pady=(0, 2))

initial_frame = tk.Frame(left_frame, bg="#FFE6E6")
initial_frame.pack()

initial_labels = create_matrix_display(initial_frame, initial_state)

goal_label = tk.Label(left_frame, text="Trạng thái đích", font=("Arial", 12, "bold"), bg="#FFE6E6", fg="black")
goal_label.pack(pady=(10, 2))

goal_frame = tk.Frame(left_frame, bg="#FFE6E6")
goal_frame.pack()

goal_labels = create_matrix_display(goal_frame, goal_state)

main_label = tk.Label(left_frame, text="Trạng thái hiện tại", font=("Arial", 12, "bold"), bg="#FFE6E6", fg="black")
main_label.pack(pady=(10, 2))

main_frame = tk.Frame(left_frame, bg="#FFE6E6")
main_frame.pack()

buttons = []
for i in range(9):
    btn = tk.Button(
        main_frame,
        text=str(initial_state[i]) if initial_state[i] != 0 else "",
        font=("Arial", 14, "bold"),
        width=3,
        height=2,
        relief="ridge",
        bg="#ADD8E6",
        fg="black",
        borderwidth=3,
    )
    btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
    buttons.append(btn)

# Cột phải: Nút, thời gian, bước đi
control_frame = tk.Frame(right_frame, bg="#FFE6E6", bd=2, relief="groove")
control_frame.pack(fill="x", pady=(0, 10))

button_color = "#FFCCCC"
hover_color = "#FF8080"

# Thêm menu cho các thuật toán
uninformed_menu = tk.Menu(menu_bar, tearoff=0)
informed_menu = tk.Menu(menu_bar, tearoff=0)
local_menu = tk.Menu(menu_bar, tearoff=0)
csp_menu = tk.Menu(menu_bar, tearoff=0)
complex_env_menu = tk.Menu(menu_bar, tearoff=0)
reinforcement_menu = tk.Menu(menu_bar, tearoff=0)  # Menu mới cho Reinforcement Learning


def show_complex_env_warning():
    messagebox.showwarning(
        "Lưu ý về bản chất thuật toán",
        "Thuật toán này được thiết kế cho môi trường không xác định hoặc quan sát không đầy đủ.\n"
        "Kết quả có thể không phản ánh đúng bản chất hoặc hiệu suất thật sự."
    )

def show_backtracking_warning():
    messagebox.showwarning(
        "Cảnh báo",
        "Thuật toán Backtracking có thể giải 8-Puzzle nhưng không phải là lựa chọn tối ưu do độ phức tạp cao và yêu cầu bộ nhớ lớn."
    )

uninformed_menu.add_command(label="BFS", command=lambda: solve_puzzle(bfs_solver))
uninformed_menu.add_command(label="DFS", command=lambda: solve_puzzle(lambda s, g: dfs_solver(s, g, max_depth=30)))
uninformed_menu.add_command(label="UCS", command=lambda: solve_puzzle(ucs_solver))
uninformed_menu.add_command(label="IDS", command=lambda: solve_puzzle(ids_solver))

informed_menu.add_command(label="Greedy", command=lambda: solve_puzzle(greedy_best_first_search))
informed_menu.add_command(label="A*", command=lambda: solve_puzzle(a_star_solver))
informed_menu.add_command(label="IDA*", command=lambda: solve_puzzle(ida_star_solver))

local_menu.add_command(label="Simple Hill Climbing", command=lambda: solve_puzzle(simple_hill_climbing_solver))
local_menu.add_command(label="Steepest Hill Climbing", command=lambda: solve_puzzle(steepest_ascent_hill_climbing_solver))
local_menu.add_command(label="Stochastic Hill Climbing", command=lambda: solve_puzzle(stochastic_hill_climbing_solver))
local_menu.add_command(label="Simulated Annealing", command=lambda: solve_puzzle(simulated_annealing_solver))
local_menu.add_command(label="Beam Search", command=lambda: solve_puzzle(lambda s, g: beam_search_solver(s, g, beam_width=5)))

csp_menu.add_command(label="Backtracking", command=lambda: (show_backtracking_warning(), solve_puzzle_backtracking()))
csp_menu.add_command(label="Backtracking for Checking", command=lambda: solve_puzzle(backtracking_for_checking_solver))

complex_env_menu.add_command(label="Belief State Search", command=lambda: (show_complex_env_warning(), solve_puzzle_belief_state()))
complex_env_menu.add_command(label="AND-OR Search", command=lambda: (show_complex_env_warning(), solve_puzzle_and_or()))
complex_env_menu.add_command(label="Partially Observable Search", command=lambda: (show_complex_env_warning(),solve_puzzle_partially_observable()))

reinforcement_menu.add_command(label="Q-learning", command=lambda: solve_puzzle(q_learning_solver))  # Thêm Q-learning vào menu

menu_bar.add_cascade(label="Uninformed Search", menu=uninformed_menu)
menu_bar.add_cascade(label="Informed Search", menu=informed_menu)
menu_bar.add_cascade(label="Local Search", menu=local_menu)
menu_bar.add_cascade(label="CSPs", menu=csp_menu)
menu_bar.add_cascade(label="Complex Environment", menu=complex_env_menu)
menu_bar.add_cascade(label="Reinforcement Learning", menu=reinforcement_menu)  # Thêm menu vào menu_bar

# Hàng 1: Các nút chọn map
control_row1 = tk.Frame(control_frame, bg="#FFE6E6")
control_row1.pack(pady=5)

easy_btn = tk.Button(control_row1, text="Map Dễ", command=select_map_easy, bg=button_color, width=8, font=("Arial", 9))
easy_btn.pack(side=tk.LEFT, padx=2)
easy_btn.bind("<Enter>", lambda e: on_enter(easy_btn, button_color, hover_color))
easy_btn.bind("<Leave>", lambda e: on_leave(easy_btn, button_color, hover_color))

medium_btn = tk.Button(control_row1, text="Map Trung bình", command=select_map_medium, bg=button_color, width=10, font=("Arial", 9))
medium_btn.pack(side=tk.LEFT, padx=2)
medium_btn.bind("<Enter>", lambda e: on_enter(medium_btn, button_color, hover_color))
medium_btn.bind("<Leave>", lambda e: on_leave(medium_btn, button_color, hover_color))

hard_btn = tk.Button(control_row1, text="Map Khó", command=select_map_hard, bg=button_color, width=8, font=("Arial", 9))
hard_btn.pack(side=tk.LEFT, padx=2)
hard_btn.bind("<Enter>", lambda e: on_enter(hard_btn, button_color, hover_color))
hard_btn.bind("<Leave>", lambda e: on_leave(hard_btn, button_color, hover_color))

# Hàng 2: Nút nhập trạng thái và reset
control_row2 = tk.Frame(control_frame, bg="#FFE6E6")
control_row2.pack(pady=5)

input_btn = tk.Button(control_row2, text="Nhập trạng thái", command=input_initial_state, bg=button_color, width=12, font=("Arial", 9))
input_btn.pack(side=tk.LEFT, padx=2)
input_btn.bind("<Enter>", lambda e: on_enter(input_btn, button_color, hover_color))
input_btn.bind("<Leave>", lambda e: on_leave(input_btn, button_color, hover_color))

reset_btn = tk.Button(control_row2, text="Reset", command=reset_puzzle, bg=button_color, width=8, font=("Arial", 9))
reset_btn.pack(side=tk.LEFT, padx=2)
reset_btn.bind("<Enter>", lambda e: on_enter(reset_btn, button_color, hover_color))
reset_btn.bind("<Leave>", lambda e: on_leave(reset_btn, button_color, hover_color))

# Nhãn hiển thị bước đi hiện tại
move_label = tk.Label(right_frame, text="", font=("Arial", 12, "bold"), fg="black", bg="#FFE6E6")
move_label.pack(pady=(0, 5))

# Khung hiển thị thông tin (Thời gian và Bước đi)
info_frame = tk.Frame(right_frame, bg="#FFE6E6", bd=2, relief="groove")
info_frame.pack(fill="both", expand=True)

time_label = tk.Label(info_frame, text="Thời gian thực thi: 0.000 giây", font=("Arial", 11, "bold"), bg="#FFF5F5", fg="black")
time_label.pack(pady=5)

steps_count_label = tk.Label(info_frame, text="Số bước đi: 0", font=("Arial", 11, "bold"), bg="#FFF5F5", fg="black")
steps_count_label.pack(pady=5)

steps_label = tk.Label(info_frame, text="Chi tiết các bước đi:", font=("Arial", 11, "bold"), bg="#FFE6E6", fg="black")
steps_label.pack(pady=(5, 2))

steps_frame = tk.Frame(info_frame, bg="#FFE6E6")
steps_frame.pack(fill="both", expand=True, padx=5, pady=5)

steps_text = tk.Text(steps_frame, height=10, width=40, font=("Arial", 10), bg="#FFF5F5", fg="black", bd=1, relief="sunken")
steps_text.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = tk.Scrollbar(steps_frame, orient=tk.VERTICAL, command=steps_text.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
steps_text.config(yscrollcommand=scrollbar.set)

update_ui(current_state)
root.mainloop()