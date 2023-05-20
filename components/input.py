import customtkinter as ctk

from config import STYLE_VARS


class TextInput(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            corner_radius=STYLE_VARS.get("radius"),
            font=("Helvetica", 14, "normal"),
            text_color=STYLE_VARS.get("foreground"),
            fg_color=STYLE_VARS.get("background"),
            border_color=STYLE_VARS.get("border"),
            border_width=1,
        )

        self.pack_configure(ipadx=16, ipady=8)
