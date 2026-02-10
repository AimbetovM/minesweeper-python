import random
import tkinter as tk
from tkinter import messagebox


class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=15):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines_count = mines

        self.root.title("Сапёр")

        self.game_over = False
        self.buttons = []
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]

        self._create_ui()
        self._place_mines()
        self._calculate_numbers()

    def _create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(
                    frame,
                    width=3,
                    height=1,
                    font=("Arial", 12),
                    command=lambda r=row, c=col: self.reveal_cell(r, c),
                )
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def _place_mines(self):
        positions = random.sample(range(self.rows * self.cols), self.mines_count)
        for pos in positions:
            row = pos // self.cols
            col = pos % self.cols
            self.board[row][col] = -1

    def _calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue
                self.board[row][col] = self._count_adjacent_mines(row, col)

    def _count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.board[r][c] == -1:
                    count += 1
        return count

    def reveal_cell(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return

        self.revealed[row][col] = True
        value = self.board[row][col]
        button = self.buttons[row][col]

        if value == -1:
            button.config(text="💣", bg="tomato", disabledforeground="black")
            self._finish_game(False)
            return

        button.config(
            text=str(value) if value > 0 else "",
            relief=tk.SUNKEN,
            state=tk.DISABLED,
            disabledforeground="blue",
            bg="#dddddd",
        )

        if value == 0:
            for r in range(max(0, row - 1), min(self.rows, row + 2)):
                for c in range(max(0, col - 1), min(self.cols, col + 2)):
                    if not self.revealed[r][c]:
                        self.reveal_cell(r, c)

        if self._check_win():
            self._finish_game(True)

    def _check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return False
        return True

    def _finish_game(self, won):
        self.game_over = True

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.buttons[row][col].config(text="💣", bg="#ff9999")
                self.buttons[row][col].config(state=tk.DISABLED)

        if won:
            messagebox.showinfo("Сапёр", "Победа! Вы открыли все безопасные клетки.")
        else:
            messagebox.showerror("Сапёр", "Игра окончена: вы нажали на мину.")


def main():
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()
