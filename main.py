import customtkinter as ctk

from enums.pages import PageName
from pages.auth import AuthPage
from pages.menu import MenuPage
from config import STYLE_VARS


PAGES = {PageName.AUTH: AuthPage, PageName.MENU: MenuPage}
DEFAULT_PAGE_NAME = PageName.MENU


class App(ctk.CTk):
    def __init__(self):
        super().__init__(
            fg_color=STYLE_VARS.get("background"),
        )

        self.title("Minesweeper")
        self.geometry("700x500")
        self.resizable(False, False)

        self.__page = None

        self.set_page(DEFAULT_PAGE_NAME)

    def set_page(self, name: PageName):
        if self.__page:
            self.__page.forget_pack()

        self.__page = PAGES[name](self)

        self.__page.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
