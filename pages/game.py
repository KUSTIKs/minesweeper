import customtkinter as ctk

from config import STYLE_VARS


class GamePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")

        self.create_widgets()

        self.pack_configure(expand=True)

    def create_widgets(self):
        container = ctk.CTkFrame(
            master=self,
            width=300,
            fg_color="transparent",
        )

        title = ctk.CTkLabel(
            master=container,
            text="Game Page",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 24, "bold"),
        )
        title.pack()

        container.pack(expand=True)
