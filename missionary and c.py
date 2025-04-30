from collections import deque
from typing import List, Set, Tuple, Optional
import datetime

class State:
    def __init__(self, m_left: int, c_left: int, boat: bool, m_right: int, c_right: int, parent=None):
        self.m_left = m_left      
        self.c_left = c_left      
        self.boat = boat          
        self.m_right = m_right    
        self.c_right = c_right    
        self.parent = parent      
        
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.m_left == other.m_left and 
                self.c_left == other.c_left and 
                self.boat == other.boat and 
                self.m_right == other.m_right and 
                self.c_right == other.c_right)
    
    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat, self.m_right, self.c_right))
    
    def __str__(self):
        left_bank = f"M:{self.m_left} C:{self.c_left}"
        right_bank = f"M:{self.m_right} C:{self.c_right}"
        boat = "B" if self.boat else " "
        return f"[{left_bank}] {boat}~~~ [{right_bank}]"

def is_valid_state(state: State, total_missionaries: int, total_cannibals: int) -> bool:
    if (state.m_left < 0 or state.c_left < 0 or 
        state.m_right < 0 or state.c_right < 0 or
        state.m_left + state.m_right > total_missionaries or 
        state.c_left + state.c_right > total_cannibals):
        return False
    
    if (state.m_left > 0 and state.m_left < state.c_left) or \
       (state.m_right > 0 and state.m_right < state.c_right):
        return False
        
    return True


def get_next_states(current: State, total_missionaries: int, total_cannibals: int, boat_capacity: int) -> List[State]:
    next_states = []
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # Possible moves: (missionaries, cannibals)
    
    for m, c in moves:
        # Ensure the boat doesn't carry more than its capacity
        if m + c > boat_capacity:
            continue
        
        new_state = None
        if current.boat:
            new_state = State(
                current.m_left - m,
                current.c_left - c,
                False,
                current.m_right + m,
                current.c_right + c,
                current
            )
        else:
            new_state = State(
                current.m_left + m,
                current.c_left + c,
                True,
                current.m_right - m,
                current.c_right - c,
                current
            )
            
        if is_valid_state(new_state, total_missionaries, total_cannibals):
            next_states.append(new_state)
            
    return next_states

def print_and_save_tree(initial_state: State, goal_state: State, file, total_missionaries: int, total_cannibals: int, boat_capacity: int):
    visited = set()
    queue = deque([initial_state])
    level = 0
    level_nodes = 1
    next_level_nodes = 0
    
    header = "\nState Space Search Tree:"
    separator = "=" * 50
    
    print(header)
    print(separator)
    file.write(header + "\n")
    file.write(separator + "\n")
    
    while queue:
        current = queue.popleft()
        level_nodes -= 1
        
        prefix = "  " * level
        state_str = f"{prefix}├─ {current}"
        print(state_str)
        file.write(state_str + "\n")
        
        if current == goal_state:
            result = f"\nGoal state reached at level {level}!"
            print(result)
            file.write(result + "\n")
            return
            
        if current not in visited:
            visited.add(current)
            next_states = get_next_states(current, total_missionaries, total_cannibals, boat_capacity)
            queue.extend(next_states)
            next_level_nodes += len(next_states)
        
        if level_nodes == 0:
            level += 1
            level_nodes = next_level_nodes
            next_level_nodes = 0

def get_valid_input(prompt: str, max_value: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if 0 <= value <= max_value:
                return value
            print(f"Please enter a number between 0 and {max_value}")
        except ValueError:
            print("Please enter a valid number")

def main():
    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"missionary_cannibals_output_{timestamp}.txt"
    
    print("\nMissionaries and Cannibals Problem - Input Parameters")
    print("=" * 50)
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Missionaries and Cannibals Problem - User Input\n")
        file.write("=" * 50 + "\n\n")
        
        # Get total number of missionaries and cannibals
        total_missionaries = get_valid_input("Enter total number of missionaries: ", 100)
        total_cannibals = get_valid_input("Enter total number of cannibals: ", 100)
        file.write(f"Total missionaries: {total_missionaries}\n")
        file.write(f"Total cannibals: {total_cannibals}\n\n")
        
        # Get boat capacity input
        boat_capacity = get_valid_input("Enter boat capacity (1 to 2): ", 2)
        file.write(f"Boat capacity: {boat_capacity}\n\n")
        
        # Get initial state input
        print("\nEnter initial state parameters:")
        file.write("Initial State Parameters:\n")
        m_left = get_valid_input(f"Number of missionaries on left bank (0-{total_missionaries}): ", total_missionaries)
        c_left = get_valid_input(f"Number of cannibals on left bank (0-{total_cannibals}): ", total_cannibals)
        boat_side = input("Is boat on left bank? (y/n): ").lower() == 'y'
        
        file.write(f"  Missionaries on left bank: {m_left}\n")
        file.write(f"  Cannibals on left bank: {c_left}\n")
        file.write(f"  Boat on left bank: {'Yes' if boat_side else 'No'}\n\n")
        
        # Calculate right bank numbers
        m_right = total_missionaries - m_left
        c_right = total_cannibals - c_left
        
        # Create initial state
        initial_state = State(m_left, c_left, boat_side, m_right, c_right)
        
        # Get goal state input
        print("\nEnter goal state parameters:")
        file.write("Goal State Parameters:\n")
        m_left_goal = get_valid_input(f"Number of missionaries on left bank (0-{total_missionaries}): ", total_missionaries)
        c_left_goal = get_valid_input(f"Number of cannibals on left bank (0-{total_cannibals}): ", total_cannibals)
        boat_side_goal = input("Is boat on left bank? (y/n): ").lower() == 'y'
        
        file.write(f"  Missionaries on left bank: {m_left_goal}\n")
        file.write(f"  Cannibals on left bank: {c_left_goal}\n")
        file.write(f"  Boat on left bank: {'Yes' if boat_side_goal else 'No'}\n\n")
        
        # Calculate right bank numbers for goal
        m_right_goal = total_missionaries - m_left_goal
        c_right_goal = total_cannibals - c_left_goal
        
        # Create goal state
        goal_state = State(m_left_goal, c_left_goal, boat_side_goal, m_right_goal, c_right_goal)
        
        print("\nInitial state:", initial_state)
        print("Goal state:", goal_state)
        
        file.write("Derived States:\n")
        file.write(f"  Initial state: {initial_state}\n")
        file.write(f"  Goal state: {goal_state}\n\n")
        
        # Validate initial and goal states
        if not is_valid_state(initial_state, total_missionaries, total_cannibals) or \
           not is_valid_state(goal_state, total_missionaries, total_cannibals):
            error_message = "\nError: Invalid initial or goal state configuration!"
            print(error_message)
            file.write(error_message + "\n")
            return
        
        # Generate and save the state space tree
        print_and_save_tree(initial_state, goal_state, file, total_missionaries, total_cannibals, boat_capacity)
    
    print(f"\nOutput has been saved to: {filename}")

if __name__ == "__main__":
    main()
