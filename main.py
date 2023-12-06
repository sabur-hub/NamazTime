import tkinter as tk
import random

root = tk.Tk()
root.title("2048")

WIDTH = 4
HEIGHT = 4
BG_COLOR_EMPTY_CELL = "#9e948a"
CELL_COLORS = {
    0: "#9e948a",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

game_board = [[0] * WIDTH for _ in range(HEIGHT)]


def move_left():
    global game_board
    for row in game_board:
        non_zero_elements = [x for x in row if x != 0]
        new_row = non_zero_elements + [0] * (WIDTH - len(non_zero_elements))

        for i in range(WIDTH - 1):
            if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                new_row[i] *= 2
                new_row[i + 1] = 0

        non_zero_elements = [x for x in new_row if x != 0]
        new_row = non_zero_elements + [0] * (WIDTH - len(non_zero_elements))
        row[:] = new_row

    add_new_tile()
    update_GUI()
def move_down():
    global game_board
    mirrored_board = [row[::-1] for row in game_board]
    transposed_board = [list(row) for row in zip(*mirrored_board)]

    for i in range(WIDTH):
        transposed_board[i] = move_row_left(transposed_board[i])

    mirrored_board = [list(row) for row in zip(*transposed_board)]
    game_board = [row[::-1] for row in mirrored_board]
    update_GUI()

def move_right():
    global game_board
    mirrored_board = [row[::-1] for row in game_board]

    for i in range(HEIGHT):
        mirrored_board[i] = move_row_left(mirrored_board[i])

    game_board = [row[::-1] for row in mirrored_board]
    update_GUI()



def move_up():
    global game_board
    transposed_board = [list(row) for row in zip(*game_board)]

    for i in range(WIDTH):
        transposed_board[i] = move_row_left(transposed_board[i])

    game_board = [list(row) for row in zip(*transposed_board)]
    update_GUI()


def move_row_left(row):
    non_zero_elements = [x for x in row if x != 0]
    new_row = non_zero_elements + [0] * (WIDTH - len(non_zero_elements))

    for i in range(WIDTH - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0

    non_zero_elements = [x for x in new_row if x != 0]
    new_row = non_zero_elements + [0] * (WIDTH - len(non_zero_elements))
    return new_row


def on_key(event):
    if event.keysym == 'Left':
        move_left()
    elif event.keysym == 'Right':
        move_right()
    elif event.keysym == 'Up':
        move_up()
    elif event.keysym == 'Down':
        move_down()

root.bind("<Key>", on_key)




def update_GUI():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            cell_value = game_board[i][j]
            cell_text = str(cell_value) if cell_value > 0 else ""
            cell_color = CELL_COLORS.get(cell_value, BG_COLOR_EMPTY_CELL)
            cells[i][j].configure(text=cell_text, bg=cell_color)

def add_new_tile():
    empty_cells = [(i, j) for i in range(HEIGHT) for j in range(WIDTH) if game_board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        game_board[i][j] = 2

cells = []
for i in range(HEIGHT):
    row = []
    for j in range(WIDTH):
        cell = tk.Label(root, text="", font=("Helvetica", 32), width=4, height=2, relief="ridge")
        cell.grid(row=i, column=j, padx=5, pady=5)
        row.append(cell)
    cells.append(row)

add_new_tile()
update_GUI()

root.mainloop()
