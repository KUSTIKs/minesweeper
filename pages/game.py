import pickle
from tkinter import messagebox
import customtkinter as ctk
import random
from PIL import Image

from components.button import Button, ButtonVariant
from enums.difficulty import GameDifficulty
from helpers.user_database import UserDatabase
from enums.pages import PageName
from config import STYLE_VARS

difficulty_simple_img = Image.open("assets/difficulty-easy.png")
difficulty_medium_img = Image.open("assets/difficulty-medium.png")
difficulty_hard_img = Image.open("assets/difficulty-hard.png")

flag_img = Image.open("assets/flag.png")
bomb_img = Image.open("assets/bomb.png")
clock_img = Image.open("assets/clock.png")


GAME_DIFFICULTY_SETTINGS = {
    GameDifficulty.EASY: {
        "rows": 9,
        "cols": 9,
        "mines_count": 10,
    },
    GameDifficulty.MEDIUM: {
        "rows": 12,
        "cols": 12,
        "mines_count": 20,
    },
    GameDifficulty.HARD: {
        "rows": 16,
        "cols": 16,
        "mines_count": 30,
    },
}

TILE_COLORS = [
    STYLE_VARS.get("orange"),
    STYLE_VARS.get("yellow"),
    STYLE_VARS.get("green"),
    STYLE_VARS.get("lightblue"),
    STYLE_VARS.get("blue"),
    STYLE_VARS.get("purple"),
    STYLE_VARS.get("pink"),
]

DEFAULT_DIFFICULTY = GameDifficulty.EASY

ROWS = 9
COLS = 9
MINES = 10


class GamePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.user_db = UserDatabase()

        self.difficulty = GameDifficulty.EASY
        self.tiles = []
        self.mines = set()
        self.game_state = None

        self.settings_frame = DifficultySettings(
            master=self,
            on_difficulty_click=self.on_difficulty_click,
        )

        self.create_widgets()

        self.pack_configure(expand=True)

    def create_widgets(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")

        top_bar = ctk.CTkFrame(self.container, fg_color="transparent")

        back_button = Button(
            master=top_bar,
            variant=ButtonVariant.SECONDARY,
            text="Back",
            command=self.back_to_menu,
        )
        back_button.pack(side=ctk.LEFT, padx=(0, 8))

        settings_button = Button(
            master=top_bar,
            variant=ButtonVariant.SECONDARY,
            text="Settings",
            command=self.open_settings,
        )
        settings_button.pack(side=ctk.LEFT, padx=(0, 8))

        top_bar.pack(pady=(0, 8), anchor="w")

        tiles_wrapper = ctk.CTkFrame(self.container, fg_color="transparent")

        for row in range(ROWS):
            tile_row = []
            for col in range(COLS):
                tile = MinesweeperTile(
                    master=tiles_wrapper,
                    row=row,
                    col=col,
                    on_left_click=lambda *args, row=row, col=col: self.on_tile_left_click(
                        row, col
                    ),
                    on_right_click=lambda *args, row=row, col=col: self.on_tile_right_click(
                        row, col
                    ),
                )
                tile.grid(row=row, column=col)
                tile_row.append(tile)
            self.tiles.append(tile_row)

        tiles_wrapper.pack(expand=True, fill="both", pady=(0, 16))

        controls_wrapper = ctk.CTkFrame(self.container, fg_color="transparent")

        save_button = Button(
            master=controls_wrapper,
            text="Save Game",
            command=self.save_game_state,
        )
        save_button.pack(side=ctk.LEFT, padx=(0, 8))

        load_button = Button(
            master=controls_wrapper,
            text="Load Game",
            command=self.load_game_state,
        )
        load_button.pack(side=ctk.LEFT, padx=(0, 8))

        new_game_button = Button(
            master=controls_wrapper,
            text="New Game",
            command=self.new_game,
        )
        new_game_button.pack(side=ctk.LEFT)

        controls_wrapper.pack()

        self.container.pack(expand=True, padx=16, pady=16)

        # Start a new game
        self.new_game()

    def new_game(self):
        self.reset_tiles()
        self.reset_minefield()
        self.place_mines()

    def reset_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()

    def reset_minefield(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) in self.mines:
                    self.tiles[row][col].set_is_mine(False)

    def place_mines(self):
        self.mines = set()
        count = 0
        while count < MINES:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if not self.tiles[row][col].is_mine:
                self.tiles[row][col].set_is_mine(True)
                self.mines.add((row, col))
                count += 1

    def on_tile_left_click(self, row, col):
        tile = self.tiles[row][col]
        if tile.is_flagged:
            return
        if tile.is_mine:
            self.game_over()
        else:
            mine_count = self.count_adjacent_mines(row, col)
            tile.set_number(mine_count)
            tile.reveal()
            if mine_count == 0:
                self.reveal_empty_cells(row, col)
            self.check_win()

    def on_tile_right_click(self, row, col):
        self.game_over
        tile = self.tiles[row][col]
        if tile.is_revealed:
            return
        tile.toggle_flagged()

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(row + 2, ROWS)):
            for c in range(max(0, col - 1), min(col + 2, COLS)):
                if self.tiles[r][c].is_mine:
                    count += 1
        return count

    def reveal_empty_cells(self, row, col):
        for r in range(max(0, row - 1), min(row + 2, ROWS)):
            for c in range(max(0, col - 1), min(col + 2, COLS)):
                tile = self.tiles[r][c]
                if not tile.is_mine and not tile.is_revealed:
                    mine_count = self.count_adjacent_mines(r, c)
                    tile.set_number(mine_count)
                    tile.reveal()
                    if mine_count == 0:
                        self.reveal_empty_cells(r, c)

    def game_over(self):
        for row in self.tiles:
            for tile in row:
                tile.configure(state=ctk.DISABLED)
                if tile.is_mine:
                    tile.reveal()
        messagebox.showinfo("Game Over", "You hit a mine! Game over.")

    def check_win(self):
        remaining_tiles = sum(
            1 for row in self.tiles for tile in row if not tile.is_revealed
        )
        if remaining_tiles == MINES:
            messagebox.showinfo("Congratulations", "You won the game")

            if self.master.user:
                self.user_db.update_wins_count(self.master.username)

    def save_game_state(self):
        self.game_state = []
        for row in self.tiles:
            row_state = []
            for tile in row:
                tile_state = {
                    "number": tile.number,
                    "is_mine": tile.is_mine,
                    "is_flagged": tile.is_flagged,
                    "is_revealed": tile.is_revealed,
                }
                row_state.append(tile_state)
            self.game_state.append(row_state)
        with open("game_state.pkl", "wb") as file:
            pickle.dump(self.game_state, file)
        messagebox.showinfo("Game Saved", "Game state saved successfully.")

    def load_game_state(self):
        try:
            with open("game_state.pkl", "rb") as file:
                self.game_state = pickle.load(file)
            for row, row_state in enumerate(self.game_state):
                for col, tile_state in enumerate(row_state):
                    tile = self.tiles[row][col]
                    tile.set_number(tile_state["number"])
                    tile.is_mine = tile_state["is_mine"]
                    tile.is_flagged = tile_state["is_flagged"]
                    tile.is_revealed = tile_state["is_revealed"]
                    tile.configure_styles()
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "No saved game state found.")

    def open_settings(self):
        self.container.pack_forget()
        self.settings_frame.pack(expand=True)

    def on_difficulty_click(self, difficulty):
        self.difficulty = difficulty
        self.settings_frame.pack_forget()
        self.container.pack()
        self.new_game()

    def back_to_menu(self):
        self.master.set_page(PageName.MENU)

    def __del__(self):
        self.user_db.close_connection()


class MinesweeperTile(ctk.CTkButton):
    def __init__(
        self,
        row,
        col,
        on_left_click,
        on_right_click,
        number=0,
        is_mine=False,
        is_flagged=False,
        is_revealed=False,
        *args,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs,
            corner_radius=STYLE_VARS.get("radius"),
            font=("Helvetica", 20, "bold"),
            height=50,
            width=50,
            text="",
            command=on_left_click,
        )

        self.bind("<Button-3>", on_right_click)

        self.number = number
        self.is_mine = is_mine
        self.is_flagged = is_flagged
        self.is_revealed = is_revealed
        self.row = row
        self.col = col

        self.configure_styles()

    def toggle_flagged(self):
        self.is_flagged = not self.is_flagged
        self.configure_styles()

    def reveal(self, *args):
        self.is_revealed = True
        self.is_flagged = False
        self.configure_styles()

    def set_is_mine(self, *args):
        self.is_mine = True
        self.configure_styles()

    def set_number(self, number, *args):
        self.number = number
        self.configure_styles()

    def reset(self, *args):
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.number = 0
        self.configure_styles()

    def configure_styles(self):
        if self.is_flagged:
            self.configure(
                fg_color=STYLE_VARS.get("background"),
                text_color=STYLE_VARS.get("foreground"),
                border_color=STYLE_VARS.get("border"),
                hover_color=STYLE_VARS.get("accent"),
                image=ctk.CTkImage(flag_img.resize((48, 48))),
                border_width=1,
                state=ctk.NORMAL,
                text="",
            )
        elif not self.is_revealed:
            self.configure(
                fg_color=STYLE_VARS.get("background"),
                text_color=STYLE_VARS.get("foreground"),
                border_color=STYLE_VARS.get("border"),
                hover_color=STYLE_VARS.get("accent"),
                text="",
                image=None,
                state=ctk.NORMAL,
                border_width=1,
            )
        elif self.is_mine:
            self.configure(
                fg_color=STYLE_VARS.get("muted"),
                image=ctk.CTkImage(bomb_img.resize((24, 24))),
                text="",
                state=ctk.DISABLED,
            )
        elif self.number:
            self.configure(
                fg_color=TILE_COLORS[self.number - 1],
                text_color_disabled="white",
                text=str(self.number),
                image=None,
                state=ctk.DISABLED,
            )
        else:
            self.configure(
                fg_color=STYLE_VARS.get("muted"),
                text="",
                image=None,
                state=ctk.DISABLED,
            )


class DifficultySettings(ctk.CTkFrame):
    def __init__(self, on_difficulty_click, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.on_difficulty_click = on_difficulty_click

        self.create_widgets()

    def create_widgets(self):
        container = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
        )

        title = ctk.CTkLabel(
            master=container,
            text="Choose difficulty",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 24, "bold"),
        )
        title.pack(pady=(0, 4), anchor="w")

        subtitle = ctk.CTkLabel(
            master=container,
            text="Difficulty affects field size",
            text_color=STYLE_VARS.get("muted-foreground"),
            font=("Helvetica", 16),
        )
        subtitle.pack(pady=(0, 20), anchor="w")

        buttons_wrapper = ctk.CTkFrame(
            master=container,
            fg_color="transparent",
        )

        easy_difficulty_button = Button(
            master=buttons_wrapper,
            text="Easy",
            variant=ButtonVariant.SECONDARY,
            image=ctk.CTkImage(difficulty_simple_img.resize((24, 24))),
            compound="top",
            command=lambda: self.on_difficulty_click(GameDifficulty.EASY),
        )
        easy_difficulty_button.pack(padx=(0, 8), ipady=20, ipadx=20, side="left")

        medium_difficulty_button = Button(
            master=buttons_wrapper,
            text="Medium",
            variant=ButtonVariant.SECONDARY,
            image=ctk.CTkImage(difficulty_medium_img.resize((24, 24))),
            compound="top",
            command=lambda: self.on_difficulty_click(GameDifficulty.MEDIUM),
        )
        medium_difficulty_button.pack(padx=(0, 8), ipady=20, ipadx=20, side="left")

        hard_difficulty_button = Button(
            master=buttons_wrapper,
            text="Hard",
            variant=ButtonVariant.SECONDARY,
            image=ctk.CTkImage(difficulty_hard_img.resize((24, 24))),
            compound="top",
            command=lambda: self.on_difficulty_click(GameDifficulty.HARD),
        )
        hard_difficulty_button.pack(padx=(0, 8), ipady=20, ipadx=20, side="left")

        buttons_wrapper.pack(fill="x")

        container.pack(expand=True, fill="both")
