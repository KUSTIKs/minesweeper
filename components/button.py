import customtkinter as ctk
from enum import Enum

from config import STYLE_VARS


class ButtonVariant(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Button(ctk.CTkButton):
    def __init__(self, variant=ButtonVariant.PRIMARY, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            corner_radius=STYLE_VARS.get("radius"),
            font=("Helvetica", 14, "bold"),
        )

        self.__variant = variant
        self.configure_styles()

        self.pack_configure(ipadx=16, ipady=8)

    @property
    def variant(self):
        return self.__vartinat

    @variant.setter
    def variant(self, variant):
        self.__vartinat = variant
        self.configure_styles()

    def configure_styles(self):
        match (self.__variant):
            case ButtonVariant.SECONDARY:
                self.configure(
                    text_color=STYLE_VARS.get("foreground"),
                    fg_color=STYLE_VARS.get("background"),
                    hover_color=STYLE_VARS.get("accent"),
                    border_color=STYLE_VARS.get("border"),
                    border_width=1,
                )
            case _:
                self.configure(
                    text_color=STYLE_VARS.get("primary-foreground"),
                    fg_color=STYLE_VARS.get("primary"),
                    hover_color=STYLE_VARS.get("primary-hover"),
                )
