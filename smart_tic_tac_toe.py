# ==========================================
# TIC TAC TOE - MEDIUM AI VERSION
# ==========================================
#
# Features:
# ✔ Smart GUI Design
# ✔ Bold Typography
# ✔ Score Tracking System
# ✔ Win Timer
# ✔ Medium Difficulty AI
# ✔ Winner Highlighting
# ✔ New Game Functionality

# Technologies:
# - Python
# - Tkinter
# ==========================================
import tkinter as tk                          # messagebox -> popup messages
from tkinter import messagebox, simpledialog  # simpledialog ->Popup dialogs and user input
 
import random                                 # Random move selection
import time 
import winsound                                  # Timer functionality

# -------------------------
# WINDOW SETUP
# -------------------------
root = tk.Tk()                   # Create the main application window
root.title("Smart Tic Tac Toe")
root.geometry("800x900")
root.resizable(False, False)
root.config(bg="#9d94aa")

# -------------------------
# GET PLAYER NAME
# -------------------------

# Prompt the user to enter a name
player_name = simpledialog.askstring(
    "Player Name",
    "Enter your name:"
)

# Assign a default name if no input is provided
if not player_name:
    player_name = "Player"


# -------------------------
# GAME VARIABLES
# -------------------------
board = [""] * 9
buttons = []

player_score = 0
computer_score = 0
# Theme mode state
dark_mode = False
# Statistics variables
games_played = 0
draw_count = 0


start_time = time.time()
# Current game timer
timer_running = True
# -------------------------
# WINNING COMBINATIONS
# -------------------------
winning_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],

    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],

    [0, 4, 8],
    [2, 4, 6]
]

# -------------------------
# CHECK WINNER
# Returns winning combo
# -------------------------
def check_winner(player):

    for combo in winning_combinations:

        if all(board[pos] == player for pos in combo):
            return combo

    return None


# -------------------------
# CHECK DRAW
# -------------------------
def is_draw():        #Check whether the board is completely filled

    return "" not in board


# -------------------------
# HIGHLIGHT WINNING BOXES
# -------------------------
def highlight_winner(combo):

    for pos in combo:

        buttons[pos].config(
            bg="lightgreen",
            fg="black"
        )
def animate_winner(combo,count=0):

    if count > 6:
        return

    color = "yellow" if count % 2 == 0 else "lightgreen"

    for pos in combo:
        buttons[pos].config(bg=color)

    root.after(
        250,
        lambda: animate_winner(combo,count+1)
    )        
# -------------------------
# DISABLE BOARD
# -------------------------
def disable_board():            # Disable all buttons after game completion

    for btn in buttons:

        btn.config(state="disabled")
# -------------------------
# LIVE TIMER
# -------------------------
def update_timer():

    if timer_running:

        elapsed = int(time.time() - start_time)

        timer_label.config(
            text=f"Time : {elapsed}s"
        )

        root.after(
            1000,
            update_timer
        )

# -------------------------
# TOGGLE THEME
# -------------------------
def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        root.config(bg="#1e1e1e")

        title_label.config(bg="#1e1e1e", fg="cyan")
        score_label.config(bg="#1e1e1e", fg="white")
        stats_label.config(bg="#1e1e1e", fg="white")
        status_label.config(bg="#1e1e1e", fg="white")
        footer_label.config(bg="#1e1e1e", fg="lightgray")

        game_frame.config(bg="#1e1e1e")

    else:

        root.config(bg="#f0f8ff")

        title_label.config(bg="#f0f8ff", fg="#003366")
        score_label.config(bg="#f0f8ff", fg="black")
        stats_label.config(bg="#f0f8ff", fg="black")
        status_label.config(bg="#f0f8ff", fg="black")
        footer_label.config(bg="#f0f8ff", fg="gray")

        game_frame.config(bg="#f0f8ff")

# -------------------------
# RESET GAME
# -------------------------
def reset_game():

    global board
    global start_time

    board = [""] * 9

    start_time = time.time()

    for btn in buttons:

        btn.config(
            text="",
            state="normal",
            bg="white",
            fg="black"
        )

   # Restore player's turn after resetting the game
    status_label.config(
      text=f"{player_name}'s Turn (X)"  
     )


# -------------------------
# Computer AI move logic
# -------------------------
def computer_move():

    global computer_score
    global games_played
    global timer_running
    available_moves = [

        i for i in range(9)

        if board[i] == ""
    ]

    if not available_moves:
        return

    move = None

    # ---------------------
    # Try to find a winning move
    # ---------------------
    for i in available_moves:

        board[i] = "O"

        if check_winner("O"):

            move = i
            board[i] = ""
            break

        board[i] = ""

    # ---------------------
    # Block the player's winning move
    # ---------------------
    if move is None:

        for i in available_moves:

            board[i] = "X"

            if check_winner("X"):

                move = i
                board[i] = ""
                break

            board[i] = ""

    # ---------------------
    # Select a Random Move
    # ---------------------
    if move is None:

        move = random.choice(
            available_moves
        )

    board[move] = "O"

    buttons[move].config(

        text="O",

        fg="red",

        state="disabled"
    )

    combo = check_winner("O")

    # ---------------------
    # ---------------------
    # Computer Wins
    # ---------------------
    if combo:

        computer_score += 1
        games_played += 1

        score_label.config(
            text=f"{player_name} : {player_score}    Computer : {computer_score}"
        )

        stats_label.config(
            text=f"Games: {games_played} | Draws: {draw_count}"
        )

        highlight_winner(combo)
        animate_winner(combo)
        winsound.Beep(500, 300)
        timer_running= False

        disable_board()

        status_label.config(
            text="Computer Wins!"
        )

        messagebox.showinfo(
            "Game Over",
            "Computer Wins!"
        )

        return 
    # ---------------------
    # Draw
    # ---------------------
    if is_draw():
        timer_running=False
        disable_board()

        status_label.config(
            text="Draw!"
        )

        messagebox.showinfo(

            "Game Over",

            "It's A Draw!"
        )

        return

    status_label.config(
       text=f"{player_name}'s Turn (X)"
)

# -------------------------
# PLAYER MOVE
# -------------------------
def player_move(index):

    global player_score
    global games_played
    global timer_running

    if board[index] != "":
        return

    board[index] = "X"

    buttons[index].config(

        text="X",

        fg="blue",

        state="disabled"
    )

    combo = check_winner("X")
    winsound.Beep(700,100)

    

# ---------------------
    # ---------------------
    # Player Wins
    # ---------------------
    if combo:

        player_score += 1
        games_played += 1

        score_label.config(
            text=f"{player_name} : {player_score}    Computer : {computer_score}"
        )

        stats_label.config(
            text=f"Games: {games_played} | Draws: {draw_count}"
        )

        highlight_winner(combo)
        animate_winner(combo)
        winsound.Beep(1000, 300)
        timer_running = False
        disable_board()

        total_time = int(
            time.time() - start_time
        )

        status_label.config(
            text="You Win!"
        )

        messagebox.showinfo(
            "🏆 CHAMPION 🏆",
            f"""
Congratulations {player_name}!

You defeated the Computer.

Time Taken: {total_time} seconds

Excellent Game!
"""
        )

        return

    # ---------------------
    # Draw
    # ---------------------
    if is_draw():
        timer_running= False
        disable_board()

        status_label.config(
            text="Draw!"
        )

        messagebox.showinfo(

            "Game Over",

            "It's A Draw!"
        )

        return

#Switch turn back to the player
    # Computer turn starts
    status_label.config(
        text="Computer Thinking..."
    )

    root.after(
        500,
        computer_move
    )

# -------------------------
# TITLE LABEL
# -------------------------
title_label = tk.Label(

    root,

    text="TIC TAC TOE",

    font=("Verdana", 24, "bold"),

    bg="#f0f8ff",

    fg="#003366"
)

title_label.pack(
    pady=15
)

# -------------------------
# SCORE LABEL
# -------------------------
score_label = tk.Label(
    root,
    text=f"{player_name} : 0    Computer : 0",
    font=("Arial", 14, "bold"),
    bg="#f0f8ff"
)

score_label.pack(
    pady=5
)
# -------------------------
# STATISTICS LABEL
# -------------------------

stats_label = tk.Label(

    root,

    text="Games: 0 | Draws: 0",

    font=("Arial", 12),

    bg="#f0f8ff"
)

stats_label.pack(
    pady=5
)
# -------------------------
# TIMER LABEL
# -------------------------
timer_label = tk.Label(

    root,

    text="Time : 0s",

    font=("Arial", 12, "bold"),

    bg="#f0f8ff"
)

timer_label.pack(
    pady=5
)

# -------------------------
# STATUS LABEL
# -------------------------
status_label = tk.Label(

    root,

    text=f"{player_name}'s Turn (X)",

    font=("Arial", 14, "bold"),

    bg="#f0f8ff"
)
status_label.pack(
    pady=10
)   


# -------------------------
# GAME FRAME
# -------------------------
game_frame = tk.Frame(
    root,
    bg="#f0f8ff"
)

game_frame.pack(
    pady=15
)

# -------------------------
# CREATE 9 BUTTONS
# -------------------------
for i in range(9):

    btn = tk.Button(

        game_frame,

        text="",

        width=5,

        height=2,

        font=("Arial", 24, "bold"),

        bg="white",

        activebackground="#d9edf7",

        command=lambda i=i:
        player_move(i)
    )

    btn.grid(

        row=i // 3,

        column=i % 3,

        padx=4,

        pady=4
    )

    buttons.append(btn)

# -------------------------
# NEW GAME BUTTON
# -------------------------
new_game_btn = tk.Button(

    root,

    text="New Game",

    font=("Arial", 14, "bold"),

    bg="orange",

    fg="black",

    padx=15,

    pady=5,

    command=reset_game
)

new_game_btn.pack(
    pady=20
)

# -------------------------
# THEME BUTTON
# -------------------------

theme_btn = tk.Button(

    root,

    text="🌙 Toggle Theme",

    font=("Arial", 12, "bold"),

    bg="purple",

    fg="white",

    command=toggle_theme
)

theme_btn.pack(
    pady=20
)
# -------------------------
# FOOTER
# -------------------------
developer_label = tk.Label(

    root,

    text="Developed by Manvi Balodi",

    font=("Arial", 9, "italic"),

    bg="#d4e27a",

    fg="gray"

)

developer_label.pack(
    pady=5
)

footer_label = tk.Label(

    root,

    text="Medium Difficulty AI",

    font=("Arial", 10, "italic"),

    bg="#f0f8ff",

    fg="gray"
)

footer_label.pack()

# -------------------------
# START GUI
# -------------------------
update_timer()
root.mainloop()
