import customtkinter as ctk
from PIL import Image

from components.button import Button, ButtonVariant
from config import STYLE_VARS
from enums.pages import PageName

trophy_img = Image.open("assets/trophy.png")
restore_img = Image.open("assets/restore.png")
play_img = Image.open("assets/play.png")


class MenuPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.create_widgets()

        self.pack_configure(expand=True)

    def create_widgets(self):
        container = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
        )

        title = ctk.CTkLabel(
            master=container,
            text="Minesweeper",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 24, "bold"),
        )
        title.pack(pady=(0, 4), anchor="w")

        subtitle = ctk.CTkLabel(
            master=container,
            text="Choose an action bellow",
            text_color=STYLE_VARS.get("muted-foreground"),
            font=("Helvetica", 16),
        )
        subtitle.pack(pady=(0, 20), anchor="w")

        buttons_wrapper = ctk.CTkFrame(
            master=container,
            fg_color="transparent",
        )

        leaderboard_button = Button(
            master=buttons_wrapper,
            text="Leaders",
            variant=ButtonVariant.SECONDARY,
            image=ctk.CTkImage(trophy_img.resize((24, 24))),
            compound="top",
        )
        leaderboard_button.pack(padx=(0, 8), ipady=20, ipadx=20, side="left")

        # restore_button = Button(
        #     master=buttons_wrapper,
        #     text="Restore",
        #     variant=ButtonVariant.SECONDARY,
        #     image=ctk.CTkImage(restore_img.resize((24, 24))),
        #     compound="top",
        # )
        # restore_button.pack(padx=(0, 8), ipady=20, ipadx=20, side="left")

        play_button = Button(
            master=buttons_wrapper,
            text="Play",
            variant=ButtonVariant.SECONDARY,
            image=ctk.CTkImage(play_img.resize((24, 24))),
            compound="top",
            command=lambda: self.master.set_page(PageName.GAME),
        )
        play_button.pack(ipady=20, ipadx=20, side="right")

        buttons_wrapper.pack(fill="x")

        container.pack(expand=True, fill="both")
