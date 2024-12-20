"""
Creator: Ashik Mahmud
Contact: ashikmahmud1104@gmail.com
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

# Main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.state('zoomed')
root.configure(bg='orange')

board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"

# User Interface
label = tk.Label(root, text="Player X's Turn", font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50")
label.pack(pady=10)

frame = tk.Frame(root, bg="#34495e", bd=3, relief=tk.RIDGE)
frame.pack(pady=10)

def reset_game():
    global board, current_player
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    label.config(text="Player X's Turn")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=tk.NORMAL, bg="#ecf0f1", font=("Helvetica", 24, "bold"))

def on_click(row, col):
    global current_player
    if board[row][col] == " " and current_player == "X":
        make_move(row, col, "X")
        if not check_game_status("X"):
            root.after(1000, ai_preparation)

def ai_preparation():
    label.config(text="AI is making move...")
    root.update()  # Refresh the window
    root.after(1000, ai_move)

def ai_move():
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax_algorithm(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        make_move(best_move[0], best_move[1], "O")
        check_game_status("O")

def minimax_algorithm(board, depth, is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax_algorithm(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax_algorithm(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def make_move(row, col, player):
    board[row][col] = player
    buttons[row][col].config(text=player, state=tk.DISABLED, font=("Helvetica", 24, "bold"),
                             fg="white", bg="#3498db" if player == "X" else "#e74c3c")

def check_game_status(player):
    if check_winner(player):
        label.config(text=f"Player {player} Wins!")
        disable_buttons()
        messagebox.showinfo("Game Over", f"Player {player} wins!")
        return True
    elif all(board[i][j] != " " for i in range(3) for j in range(3)):
        label.config(text="It's a Draw!")
        messagebox.showinfo("Game Over", "It's a draw!")
        return True
    else:
        label.config(text=f"Player X's Turn" if player == "O" else "AI's Turn")
        return False

def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

def check_winner(player):
    return any(
        all(board[i][j] == player for j in range(3)) or
        all(board[j][i] == player for j in range(3)) or
        all(board[j][j] == player for j in range(3)) or
        all(board[j][2-j] == player for j in range(3))
        for i in range(3)
    )

# Game board and buttons
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(frame, text="", width=8, height=3, 
                                  command=lambda i=i, j=j: on_click(i, j), bg="#ecf0f1", font=("Helvetica", 24, "bold"))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

reset_btn = tk.Button(root, text="Reset Game", command=reset_game, font=("Helvetica", 12, "bold"), bg="#f39c12", fg="white")
reset_btn.pack(pady=10)

root.mainloop()
