from collections import deque
import copy
import random
import sys
from datetime import datetime

def tee_print(*args, **kwargs):
    """Print to both console and file."""
    print(*args, **kwargs)
    if 'file' in kwargs:
        print(*args)  # Also print to console if writing to file

class StateSpaceTree:
    # [Previous StateSpaceTree class implementation remains the same]
    def __init__(self, initial_state, goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.visited_states = set()
        self.size = len(initial_state)
        
    def get_state_id(self, state):
        if isinstance(state, list):
            return tuple(tuple(row) if isinstance(row, list) else row for row in state)
        return tuple(state)
    
    def format_state(self, state):
        if isinstance(state[0], list):
            return '\n'.join(' '.join(f"{x:2d}" for x in row) for row in state)
        return ' '.join(map(str, state))
    
    def generate_moves(self, state):
        raise NotImplementedError("Must implement generate_moves for specific problem")
    
    def print_tree(self, max_depth=3, output_file=None):
        queue = deque([(self.initial_state, None, 0, "")])
        self.visited_states = set()
        nodes_at_depth = {i: 0 for i in range(max_depth + 1)}
        total_nodes = 0
        
        tee_print("\nGenerating State Space Tree...", file=output_file)
        tee_print("=" * 40, file=output_file)
        
        while queue:
            current_state, parent, depth, prefix = queue.popleft()
            if depth > max_depth:
                continue
                
            state_id = self.get_state_id(current_state)
            if state_id in self.visited_states:
                continue
                
            self.visited_states.add(state_id)
            nodes_at_depth[depth] += 1
            total_nodes += 1
            
            tee_print(file=output_file)
            if depth == 0:
                tee_print("Root State (Depth 0):", file=output_file)
            else:
                tee_print(f"{prefix}+-- State at depth {depth}", file=output_file)
            tee_print(prefix + "    " + self.format_state(current_state).replace('\n', '\n' + prefix + "    "), file=output_file)
            
            children = self.generate_moves(current_state)
            for i, child in enumerate(children):
                child_id = self.get_state_id(child)
                if child_id not in self.visited_states:
                    new_prefix = prefix + ("    " if i == len(children) - 1 else "|   ")
                    queue.append((child, current_state, depth + 1, new_prefix))
        
        tee_print("\nTree Generation Summary", file=output_file)
        tee_print("=" * 40, file=output_file)
        tee_print(f"Total nodes generated: {total_nodes}", file=output_file)
        for depth, count in nodes_at_depth.items():
            if count > 0:
                tee_print(f"Nodes at depth {depth}: {count}", file=output_file)

class NPuzzle(StateSpaceTree):
    def find_blank(self, state):
        for i, row in enumerate(state):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j
        return None
    
    def generate_moves(self, state):
        moves = []
        i, j = self.find_blank(state)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for di, dj in directions:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                new_state = [row[:] for row in state]
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                moves.append(new_state)
        
        return moves

def is_solvable(state, goal_state, size):
    """
    Check if the puzzle is solvable using the correct logic for both odd and even sized puzzles.
    """
    def get_inversions(state):
        # Convert 2D state to 1D and remove blank (0)
        flat = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return inversions

    def get_blank_row(state):
        # Get the row number (0-based) of the blank tile from the top
        for i in range(size):
            for j in range(size):
                if state[i][j] == 0:
                    return i
        return -1

    # Get inversions count
    inversions = get_inversions(state)
    
    # Get blank position from top
    blank_row = get_blank_row(state)

    # For odd-sized puzzles (e.g., 3x3)
    if size % 2 == 1:
        return inversions % 2 == 0
    # For even-sized puzzles (e.g., 4x4)
    else:
        blank_row_from_bottom = size - blank_row - 1
        if blank_row_from_bottom % 2 == 0:
            return inversions % 2 == 1
        else:
            return inversions % 2 == 0

def generate_random_state(size):
    """
    Generate a random solvable puzzle state.
    """
    goal_state = [[i + j * size for i in range(1, size + 1)] for j in range(size)]
    goal_state[-1][-1] = 0  # Set last position to blank (0)
    
    while True:
        # Create a random state
        numbers = list(range(size * size))
        random.shuffle(numbers)
        state = [numbers[i:i + size] for i in range(0, size * size, size)]
        
        # Check if it's solvable
        if is_solvable(state, goal_state, size):
            return state

def demo_n_puzzle():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"puzzle_tree_{timestamp}.txt"
    
    with open(output_filename, 'w') as output_file:
        tee_print("N-Puzzle State Space Tree Demonstration", file=output_file)
        tee_print("=" * 40, file=output_file)
        
        while True:
            try:
                size = int(input("\nEnter grid size (2-7 supported): "))
                if size < 2:
                    print("Grid size must be at least 2")
                    continue
                if size > 7:
                    print("Warning: Sizes above 7 may be very slow and consume lots of memory")
                    if input("Do you want to continue anyway? (y/n): ").lower() != 'y':
                        continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Calculate maximum value for input validation
        max_value = size * size - 1
        
        initial_state = generate_random_state(size)
        
        tee_print("\nRandomly generated initial state:", file=output_file)
        tee_print('\n'.join(' '.join(f"{x:{len(str(max_value))}d}" for x in row) for row in initial_state), file=output_file)
        
        tee_print(f"\nEnter the goal state row by row (use space-separated numbers, use 0 for empty tile)", file=output_file)
        tee_print(f"Numbers should be between 0 and {max_value}", file=output_file)
        
        goal_state = []
        tee_print("\nEnter goal state:", file=output_file)
        used_numbers = set()
        
        for i in range(size):
            while True:
                try:
                    row = list(map(int, input(f"Enter row {i + 1}: ").split()))
                    if len(row) != size:
                        print(f"Please enter exactly {size} numbers")
                        continue
                    if not all(0 <= x <= max_value for x in row):
                        print(f"Numbers must be between 0 and {max_value}")
                        continue
                        
                    # Check for duplicate numbers
                    row_set = set(row)
                    if len(row_set & used_numbers) > 0:
                        print("Duplicate numbers are not allowed")
                        continue
                    used_numbers.update(row_set)
                    
                    goal_state.append(row)
                    break
                except ValueError:
                    print("Please enter valid numbers")
        
        # Verify all numbers are used
        if len(used_numbers) != size * size:
            missing = set(range(size * size)) - used_numbers
            print(f"Error: Missing numbers {missing}")
            return
        
        tee_print("\nEntered goal state:", file=output_file)
        tee_print('\n'.join(' '.join(f"{x:{len(str(max_value))}d}" for x in row) for row in goal_state), file=output_file)
        
        if not is_solvable(initial_state, goal_state, size):
            tee_print("\nWarning: The puzzle is not solvable between the initial and goal states.", file=output_file)
            return
        
        puzzle = NPuzzle(initial_state, goal_state)
        
        while True:
            try:
                max_depth = int(input("\nEnter maximum depth to explore (recommended 1-2 for large puzzles): "))
                if max_depth < 0:
                    print("Depth must be non-negative")
                    continue
                if max_depth > 3 and size > 4:
                    print("Warning: Large depth values with big puzzles may be very slow")
                    if input("Do you want to continue anyway? (y/n): ").lower() != 'y':
                        continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        puzzle.print_tree(max_depth, output_file)
        tee_print(f"\nOutput has been saved to: {output_filename}", file=output_file)

if __name__ == "__main__":
    demo_n_puzzle()