import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from loading import login

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приложение")
        self.geometry("400x250")  # Размер окна
        self.resizable(False, False)  # Запрет изменения размера окна
        self.db_path = "users.db"
        self.init_database()
        self.create_login_form()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()