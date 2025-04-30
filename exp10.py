import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Maze Solver")
        self.create_widgets()
        self.maze = [
            ['S', 0, 1, 0, 0],
            [0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 'E', 1]
        ]

    def create_widgets(self):
        self.solve_button = tk.Button(self.root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack(pady=10)

    def dfs(self, x, y, path, visited):
        """DFS function to find a path in the maze"""
        if self.maze[x][y] == 'E':  # Found exit
            path.append((x, y))
            return True

        if (x, y) in visited or self.maze[x][y] == 1:  # Wall or already visited
            return False

        visited.add((x, y))
        path.append((x, y))

        # Possible moves: Down, Up, Right, Left
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]):  # Within bounds
                if self.dfs(new_x, new_y, path, visited):
                    return True  # Stop if path found

        path.pop()  # Backtrack
        return False

    def solve_maze(self):
        """Finds a path from 'S' to 'E' using DFS and displays it"""
        start, exit = None, None

        # Find Start (S) and Exit (E)
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 'S':
                    start = (i, j)
                elif self.maze[i][j] == 'E':
                    exit = (i, j)

        if not start or not exit:
            print("Maze must contain 'S' (start) and 'E' (exit).")
            return

        path = []
        visited = set()
        if self.dfs(start[0], start[1], path, visited):
            self.display_maze(path)
        else:
            print("No Path Found.")

    def display_maze(self, path):
        """Displays the maze with the DFS path using Matplotlib"""
        maze_array = np.array([[0 if cell == 0 else 1 for cell in row] for row in self.maze])

        # Convert path to coordinates
        x_path = [p[1] for p in path]
        y_path = [p[0] for p in path]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(maze_array, cmap="gray_r")

        # Mark Start (S) and Exit (E)
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 'S':
                    ax.text(j, i, 'S', ha='center', va='center', color='red', fontsize=16, fontweight='bold')
                elif self.maze[i][j] == 'E':
                    ax.text(j, i, 'E', ha='center', va='center', color='green', fontsize=16, fontweight='bold')

        # Plot DFS path
        ax.plot(x_path, y_path, marker="o", color="blue", markersize=8, linestyle="-")

        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

# Run the GUI
root = tk.Tk()
app = MazeSolverGUI(root)
root.mainloop()
