import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.resizable(False, False)

# Game variables
current_player = "X"
board = [""] * 9

# Function to check for a winner
def check_winner():
    win_conditions = [(0,1,2), (3,4,5), (6,7,8),  # Rows
                      (0,3,6), (1,4,7), (2,5,8),  # Columns
                      (0,4,8), (2,4,6)]           # Diagonals

    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]  # Return the winning player (X or O)
    
    if "" not in board:
        return "Tie"  # If no spaces left, it's a tie

    return None  # No winner yet

# Function to handle button click
def on_click(index):
    global current_player

    if board[index] == "" and not check_winner():  # Ensure the cell is empty
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled")

        winner = check_winner()
        if winner:
            if winner == "Tie":
                messagebox.showinfo("Game Over", "It's a Tie!")
            else:
                messagebox.showinfo("Game Over", f"Player {winner} Wins!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"  # Switch turns

# Function to reset the game
def reset_game():
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for button in buttons:
        button.config(text="", state="normal")

# Create buttons
buttons = []
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 20), width=6, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

# Run the Tkinter event loop
root.mainloop()
