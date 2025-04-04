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

    def get_hashed_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_credentials(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, self.get_hashed_password(password)))
        result = c.fetchone()
        conn.close()
        return bool(result)

    def add_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, self.get_hashed_password(password)))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def register_user(self):
        register_window = RegisterWindow(self)
        self.wait_window(register_window)

    def create_login_form(self):
        # Создание виджетов для формы входа
        username_label = tk.Label(self, text="Имя пользователя:")
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Пароль:")
        password_entry = tk.Entry(self, show="*")  # Скрывает вводимый пароль

        login_button = tk.Button(self, text="Войти", command=lambda: self.loginpas(username_entry.get(), password_entry.get()))
        register_button = tk.Button(self, text="Зарегистрироваться", command=self.register_user)

        # Размещение виджетов на экране
        username_label.pack(pady=5)
        username_entry.pack(pady=5)
        password_label.pack(pady=5)
        password_entry.pack(pady=5)
        login_button.pack(pady=10)
        register_button.pack(pady=5)

    def loginpas(self, username, password):
        if self.check_credentials(username, password):
            messagebox.showinfo("Успех", "Вы успешно вошли!")
            self.destroy()  # Закрытие окна входа
            self.open_main_app()  # Открытие главного приложения
            login()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль.")

    def open_main_app(self):
        pass  


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
