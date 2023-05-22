import customtkinter as ctk

from enums.pages import PageName
from pages.auth import AuthPage
from pages.game import GamePage
from pages.menu import MenuPage
from pages.leaderboard import LeaderboardPage
from config import STYLE_VARS


PAGES = {
    PageName.AUTH: AuthPage,
    PageName.MENU: MenuPage,
    PageName.GAME: GamePage,
    PageName.LEADERBOARD: LeaderboardPage,
}
DEFAULT_PAGE_NAME = PageName.AUTH


class App(ctk.CTk):
    def __init__(self):
        super().__init__(
            fg_color=STYLE_VARS.get("background"),
        )

        self.title("Minesweeper")
        self.minsize(800, 600)

        self.__page = None
        self.username = None

        self.set_page(DEFAULT_PAGE_NAME)

    def set_username(self, username):
        self.username = username

    def set_page(self, name: PageName):
        if self.__page:
            self.__page.destroy()

        self.__page = PAGES[name](self)

        self.__page.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
