import customtkinter as ctk

from components.button import Button, ButtonVariant
from helpers.user_database import UserDatabase
from enums.pages import PageName
from config import STYLE_VARS


class LeaderboardPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.user_db = UserDatabase()

        self.create_widegets()

        self.pack_configure(expand=True, fill="y")

    def create_widegets(self):
        container = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
        )

        top_bar = ctk.CTkFrame(master=container, fg_color="transparent")

        back_button = Button(
            master=top_bar,
            variant=ButtonVariant.SECONDARY,
            text="Back",
            command=self.back_to_menu,
            width=60,
        )
        back_button.pack(side="left", padx=(0, 10))

        title = ctk.CTkLabel(
            master=top_bar,
            text="Leaderboard",
            font=("Helvetica", 24, "bold"),
            text_color=STYLE_VARS.get("foreground"),
        )
        title.pack(side="left")

        top_bar.pack(pady=(0, 16), anchor="w")

        table = ctk.CTkScrollableFrame(
            master=container,
            fg_color="transparent",
            width=500,
        )

        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=1)

        headers = ["Username", "Wins"]

        data = self.user_db.get_leaderboard()

        for col, header in enumerate(headers):
            header = ctk.CTkLabel(
                master=table,
                text=header,
                font=("Helvetica", 16, "bold"),
                text_color=STYLE_VARS.get("foreground"),
            )
            header.grid(
                row=0,
                column=col,
                padx=10,
                pady=5,
                sticky="w",
            )

        for row, row_data in enumerate(data):
            for col, cell_value in enumerate(row_data):
                value = ctk.CTkLabel(
                    master=table,
                    text=str(cell_value),
                    font=("Helvetica", 14),
                    text_color=STYLE_VARS.get("muted-foreground"),
                )
                value.grid(
                    row=row + 1,
                    column=col,
                    padx=10,
                    pady=5,
                    sticky="w",
                )

        table.pack(expand=True, fill="both")

        container.pack(expand=True, fill="y", padx=20, pady=20)

    def back_to_menu(self):
        self.master.set_page(PageName.MENU)

    def __del__(self):
        self.user_db.close_connection()
