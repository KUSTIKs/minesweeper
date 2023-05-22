import sqlite3
from tkinter import messagebox


class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("auth.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, wins_count INTEGER)"
        )
        self.conn.commit()

    def register_user(self, username, password):
        if (
            len(username) >= 4
            and len(password) >= 6
            and " " not in username
            and " " not in password
        ):
            self.create_table()
            self.cursor.execute(
                "INSERT INTO users (username, password, wins_count) VALUES (?, ?, ?)",
                (username, password, 0),  # Initialize wins_count to 0
            )
            self.conn.commit()
            messagebox.showinfo("Registration Successful", "Registration successful!")
        else:
            messagebox.showerror(
                "Invalid Input",
                "Invalid username or password. "
                "Make sure the username has at least 4 characters, "
                "the password has at least 6 characters, "
                "and neither contain spaces.",
            )

    def login_user(self, username, password):
        self.create_table()
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def update_wins_count(self, username):
        self.create_table()
        self.cursor.execute(
            "UPDATE users SET wins_count = wins_count + 1 WHERE username=?", (username,)
        )
        self.conn.commit()

    def get_leaderboard(self):
        self.create_table()
        self.cursor.execute(
            "SELECT username, wins_count FROM users ORDER BY wins_count DESC"
        )
        leaderboard_data = self.cursor.fetchall()
        return leaderboard_data

    def close_connection(self):
        self.conn.close()
