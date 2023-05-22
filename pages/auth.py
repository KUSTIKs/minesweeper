import customtkinter as ctk
from tkinter import messagebox

from components.button import Button, ButtonVariant
from components.input import TextInput
from enums.pages import PageName
from config import STYLE_VARS
from helpers.user_database import UserDatabase


class AuthPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color="transparent")
        self.user_db = UserDatabase()
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
            text="Welcome to Minesweeper!",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 24, "bold"),
        )
        title.pack(pady=(0, 4), anchor="w")

        subtitle = ctk.CTkLabel(
            master=container,
            text="Please log in or register to continue",
            text_color=STYLE_VARS.get("muted-foreground"),
            font=("Helvetica", 16),
        )
        subtitle.pack(pady=(0, 20), anchor="w")

        username_input_wrapper = ctk.CTkFrame(
            master=container,
            fg_color="transparent",
        )

        ctk.CTkLabel(
            master=username_input_wrapper,
            text="Username:",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 14, "bold"),
        ).pack(pady=(0, 4), anchor="w")

        username_input = TextInput(master=username_input_wrapper)
        username_input.pack(anchor="w", expand=True, fill="x", pady=(0, 4))

        username_input_wrapper.pack(expand=True, fill="x")

        password_input_wrapper = ctk.CTkFrame(
            master=container,
            fg_color="transparent",
        )

        ctk.CTkLabel(
            master=password_input_wrapper,
            text="Password:",
            text_color=STYLE_VARS.get("foreground"),
            font=("Helvetica", 14, "bold"),
        ).pack(pady=(0, 4), anchor="w")

        password_input = TextInput(master=password_input_wrapper, show="*")
        password_input.pack(anchor="w", expand=True, fill="x")

        password_input_wrapper.pack(expand=True, fill="x", pady=(0, 20))

        buttons_wrapper = ctk.CTkFrame(
            master=container,
            fg_color="transparent",
        )

        register_button = Button(
            master=buttons_wrapper,
            text="Register",
            variant=ButtonVariant.SECONDARY,
            command=lambda: self.register_user(
                username_input.get(), password_input.get()
            ),
        )
        register_button.pack(fill="both", expand=True, side="left", padx=(0, 8))

        login_button = Button(
            master=buttons_wrapper,
            text="Log In",
            variant=ButtonVariant.PRIMARY,
            command=lambda: self.login_user(username_input.get(), password_input.get()),
        )
        login_button.pack(fill="both", expand=True, side="right")

        buttons_wrapper.pack()

        container.pack(expand=True)

    def register_user(self, username, password):
        self.user_db.register_user(username, password)

    def login_user(self, username, password):
        if self.user_db.login_user(username, password):
            self.master.set_username(username)
            self.master.set_page(PageName.MENU)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def __del__(self):
        self.user_db.close_connection()
