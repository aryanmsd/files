class NQueensStateSpaceTree:
    def __init__(self, n):
        self.n = n  # Size of the chessboard
        self.tree = []  # To store the search tree in a structured way
        self.node_count = 0  # Track the total number of nodes
        self.solutions = []  # To store all valid solutions

    def is_safe(self, board, row, col):
        """Check if it's safe to place a queen at board[row][col]."""
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def generate_tree(self, row=0, board=None, depth=0, parent="Root"):
        """Generate the search tree recursively."""
        if board is None:
            board = [-1] * self.n  # Initialize an empty board

        # Create a copy of the board for storing in the tree
        state = (depth, board[:], parent)
        self.tree.append(state)
        self.node_count += 1

        # If all queens are placed, save the solution
        if row == self.n:
            self.solutions.append(board[:])
            return

        # Try placing a queen in each column of the current row
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.generate_tree(row + 1, board[:], depth + 1, f"Depth {depth}")
                board[row] = -1  # Backtrack

    def print_tree(self):
        """Print the search tree in the requested format."""
        print("Generating State Space Tree...")
        print("=" * 40)
        print("\nRoot State (Depth 0):")
        self.print_board([-1] * self.n)

        # Iterate through the tree and print each node
        for depth, board, parent in self.tree:
            if depth == 0:
                continue  # Skip the root node here
            indent = "|   " * (depth - 1) + "+-- "
            print(f"{indent}State at depth {depth}")
            self.print_board(board)

        # Summary
        print("\nTree Generation Summary")
        print("=" * 40)
        print(f"Total nodes generated: {self.node_count}")
        print(f"Nodes at depth 0: 1")
        for d in range(1, self.n + 1):
            count = sum(1 for node in self.tree if node[0] == d)
            print(f"Nodes at depth {d}: {count}")

        # Display solutions
        print("\nSolutions Found")
        print("=" * 40)
        for i, solution in enumerate(self.solutions, 1):
            print(f"Solution {i}:")
            self.print_board(solution)

    def print_board(self, board):
        """Print a board representation based on the current state."""
        for row in range(self.n):
            line = ["Q" if board[row] == col else "." for col in range(self.n)]
            print("    " + " ".join(line))
        print()  # Add spacing between boards


# Input from the user
try:
    n = int(input("Enter the size of the chessboard (N): "))
    if n < 1:
        print("N must be greater than 0.")
    else:
        # Create an instance of the NQueensStateSpaceTree class
        n_queens_tree = NQueensStateSpaceTree(n)
        n_queens_tree.generate_tree()
        n_queens_tree.print_tree()
except ValueError:
    print("Please enter a valid integer.")
