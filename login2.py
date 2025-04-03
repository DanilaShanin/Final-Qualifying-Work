import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from loading import login

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приложение")
        self.geometry("400x250") 
        self.resizable(False, False)  
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
       
        username_label = tk.Label(self, text="Имя пользователя:")
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Пароль:")
        password_entry = tk.Entry(self, show="*")  

        login_button = tk.Button(self, text="Войти", command=lambda: self.loginpas(username_entry.get(), password_entry.get()))
        register_button = tk.Button(self, text="Зарегистрироваться", command=self.register_user)

        username_label.pack(pady=5)
        username_entry.pack(pady=5)
        password_label.pack(pady=5)
        password_entry.pack(pady=5)
        login_button.pack(pady=10)
        register_button.pack(pady=5)

    def loginpas(self, username, password):
        if self.check_credentials(username, password):
            messagebox.showinfo("Успех", "Вы успешно вошли!")
            self.destroy() 
            self.open_main_app() 
            login()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль.")

 


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Регистрация")
        self.geometry("300x300")
        self.parent = parent
        self.create_register_form()

    def create_register_form(self):
       
        username_label = tk.Label(self, text="Имя пользователя:")
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Пароль:")
        password_entry = tk.Entry(self, show="*")  
        confirm_password_label = tk.Label(self, text="Подтверждение пароля:")
        confirm_password_entry = tk.Entry(self, show="*")          register_button = tk.Button(self, text="Зарегистрироваться", command=lambda: self.register(
            username_entry.get(),
            password_entry.get(),
            confirm_password_entry.get())
        )

        username_label.pack(pady=5)
        username_entry.pack(pady=5)
        password_label.pack(pady=5)
        password_entry.pack(pady=5)
        confirm_password_label.pack(pady=5)
        confirm_password_entry.pack(pady=5)
        register_button.pack(pady=10)

    def register(self, username, password, confirm_password):
        if not username or not password or not confirm_password:
            messagebox.showwarning("Предупреждение", "Все поля обязательны для заполнения.")
            return
        if password != confirm_password:
            messagebox.showwarning("Предупреждение", "Пароли не совпадают.")
            return
        if self.parent.add_user(username, password):
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.destroy()
        else:
            messagebox.showwarning("Предупреждение", f"Пользователь {username} уже существует.")


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
