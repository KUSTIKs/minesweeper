import customtkinter as ctk
from PIL import Image

from components.button import Button, ButtonVariant
from enums.difficulty import GameDifficulty
from config import STYLE_VARS

difficulty_simple_img = Image.open("assets/difficulty-easy.png")
difficulty_medium_img = Image.open("assets/difficulty-medium.png")
difficulty_hard_img = Image.open("assets/difficulty-hard.png")


class GamePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.difficulty_state = ctk.StringVar()

        self.difficulty_frame = DifficultyFrame(
            master=self,
            on_difficulty_click=self.on_difficulty_click,
        )
        self.difficulty_frame.pack()

        self.pack_configure(expand=True)

    def on_difficulty_click(self, difficulty):
        self.difficulty_state.set(difficulty)
        self.difficulty_frame.destroy()
        self.create_widgets()

    def create_widgets(self):
        container = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
        )

        title = ctk.CTkLabel(
            master=container,
            text=self.difficulty_state.get(),
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 24, "bold"),
        )
        title.pack(anchor="w")

        container.pack_configure(expand=True)


class DifficultyFrame(ctk.CTkFrame):
    def __init__(self, on_difficulty_click, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.on_difficulty_click = on_difficulty_click

        self.create_widgets()

        self.pack_configure(expand=True)

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
