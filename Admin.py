import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from Admin12312321 import Adminapp  # Импортируем класс Adminapp из файла admin.py
global app
import hashlib
from loading import login

# Глобальная переменная для главного окна
global main_window


# Классы для работы с базой данных и GUI
class DB:
    def __init__(self, database_path="users.db"):
        self.database_path = database_path
        self.conn = None
        self.c = None
        self._connect_db()

    def _connect_db(self):
        """Устанавливает соединение с базой данных."""
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()

    def close_connection(self):
        """Закрывает соединение с базой данных."""
        if self.conn is not None:
            self.conn.close()

    def insert_user(self, username, password):
        """
        Вставляет нового пользователя в таблицу users.

        :param username: Имя пользователя
        :param password: Пароль пользователя (в хешированном виде)
        :return: True при успешном добавлении, иначе False
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        try:
            self.c.execute(query, (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Пользователь '{username}' уже существует.")
            return False
        except Exception as e:
            print(f"Ошибка при вставке данных: {str(e)}")
            return False

    def update_user(self, user_id, new_username=None, new_password=None):
        """
        Обновляет данные пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя
        :param new_username: Новое имя пользователя (если None, не изменяется)
        :param new_password: Новый пароль (если None, не изменяется)
        :return: True при успешном обновлении, иначе False
        """
        query = ""
        params = []
        if new_username is not None and new_password is not None:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            query = "UPDATE users SET username = ?, password = ? WHERE id = ?"
            params = (new_username, hashed_password, user_id)
        elif new_username is not None:
            query = "UPDATE users SET username = ? WHERE id = ?"
            params = (new_username, user_id)
        elif new_password is not None:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            query = "UPDATE users SET password = ? WHERE id = ?"
            params = (hashed_password, user_id)
        else:
            print("Не указано ни одного параметра для обновления.")
            return False

        try:
            self.c.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {str(e)}")
            return False

    def delete_user(self, user_id):
        """
        Удаляет пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя
        :return: True при успешном удалении, иначе False
        """
        query = "DELETE FROM users WHERE id = ?"
        try:
            self.c.execute(query, (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {str(e)}")
            return False

    def select_all_users(self):
        """
        Возвращает всех пользователей из базы данных.

        :return: Список кортежей с пользователями
        """
        query = "SELECT * FROM users"
        self.c.execute(query)
        return self.c.fetchall()

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
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                  (username, self.get_hashed_password(password)))
        result = c.fetchone()
        conn.close()
        return bool(result)

    def add_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, self.get_hashed_password(password)))
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

        login_button = tk.Button(self, text="Войти",
                                 command=lambda: self.loginpas(username_entry.get(), password_entry.get()))
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

            # Проверка на логин 'admin' и соответствующий пароль
            if username == 'admin' and password == '11':
                self.withdraw()  # Скрываем текущее окно
                root = tk.Tk()  # Создаем новое корневое окно Tkinter
                app = Adminapp(root)  # Инициализируем приложение администратора
                app.pack()  # Упаковываем виджет в окно
                root.title("Администраторское приложение")  # Устанавливаем заголовок окна
                root.geometry("800x600")  # Задаем размер окна
                root.mainloop()  # Запускаем цикл обработки событий Tkinter
            else:
                self.destroy()  # Закрытие окна входа
                self.open_main_app()  # Открытие главного приложения
                login()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль.")

    def open_main_app(self):
        pass  # Здесь будет реализована логика вашего приложения


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Регистрация")
        self.geometry("300x300")
        self.parent = parent
        self.create_register_form()

    def create_register_form(self):
        # Создание виджетов для формы регистрации
        username_label = tk.Label(self, text="Имя пользователя:")
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Пароль:")
        password_entry = tk.Entry(self, show="*")  # Скрывает вводимый пароль
        confirm_password_label = tk.Label(self, text="Подтверждение пароля:")
        confirm_password_entry = tk.Entry(self, show="*")  # Скрывает вводимый пароль

        register_button = tk.Button(self, text="Зарегистрироваться", command=lambda: self.register(
            username_entry.get(),
            password_entry.get(),
            confirm_password_entry.get())
                                    )

        # Размещение виджетов на экране
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


class Adminapp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()  # создаем объект базы данных
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#fe4240', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="img/add.gif")
        btn_open_dialog = tk.Button(toolbar, text='Добавить ', command=self.open_dialog, bg='#fe4240', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file="img/add.gif")
        btn_edit_dialog = tk.Button(toolbar, text='Внести изменения', bg='#fe4240', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="img/add.gif")
        btn_delete = tk.Button(toolbar, text='Удалить авто', bg='#fe4240', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="img/add.gif")
        btn_search = tk.Button(toolbar, text='Поиск', bg='#fe4240', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="img/add.gif")
        btn_refresh = tk.Button(toolbar, text='Обновить страницу', bg='#fe4240', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавляем кнопку для возврата
        self.back_img = tk.PhotoImage(file="img/add.gif")  # Изображение для кнопки возврата
        btn_back = tk.Button(toolbar, text='Вернуться к коду', bg='#fe4240', bd=0, image=self.back_img,
                             compound=tk.TOP, command=self.go_back_to_code)
        btn_back.pack(side=tk.LEFT)

    def go_back_to_code(self):
        self.master.destroy()  # Закрываем текущее окно администратора
        main_window.deiconify()  # Показываем скрытое главное окно
        main_window.lift()       # Перемещаем главное окно наверх

    def open_dialog(self):
        AddUserDialog(self)

    def open_update_dialog(self):
        UpdateUserDialog(self)

    def open_search_dialog(self):
        SearchUserDialog(self)

    def view_records(self):
        # Отображаем всех пользователей
        rows = self.db.select_all_users()
        [self.tree.delete(i) for i in self.tree.get_children()]  # Очищаем дерево
        [self.tree.insert('', 'end', values=row) for row in rows]

    def delete_records(self):
        selected_item = self.tree.selection()[0]
        user_id = self.tree.item(selected_item)['values'][0]
        answer = messagebox.askyesno(title="Подтверждение удаления",
                                     message=f"Точно удалить запись с ID {user_id}?")
        if answer:
            self.db.delete_user(user_id)
            self.view_records()

class AddUserDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить пользователя")
        self.geometry("400x180+400+300")
        self.resizable(False, False)

        label_name = tk.Label(self, text="Имя пользователя:")
        label_name.place(x=50, y=40)
        label_pass = tk.Label(self, text="Пароль:")
        label_pass.place(x=50, y=70)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=170, y=40)
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.place(x=170, y=70)

        btn_add = tk.Button(self, text="Добавить", command=self.add_user)
        btn_add.place(x=160, y=120)
        btn_cancel = tk.Button(self, text="Отмена", command=self.destroy)
        btn_cancel.place(x=240, y=120)

        self.grab_set()
        self.focus_set()

    def add_user(self):
        username = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        if len(password) < 8:
            messagebox.showwarning("Предупреждение", "Пароль должен содержать минимум 8 символов!")
            return
        if self.master.db.insert_user(username, password):
            messagebox.showinfo("Успешно", "Пользователь добавлен!")
            self.destroy()
        else:
            messagebox.showwarning("Ошибка", "Пользователь с таким именем уже существует.")

class UpdateUserDialog(AddUserDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Редактировать пользователя")
        self.label_name.config(text="Новое имя пользователя:")
        self.label_pass.config(text="Новый пароль:")
        self.entry_name.insert(0, self.master.tree.item(self.master.tree.selection())['values'][1])
        self.entry_pass.insert(0, self.master.tree.item(self.master.tree.selection())['values'][2])
        self.btn_add.config(text="Сохранить изменения", command=self.update_user)

    def update_user(self):
        user_id = self.master.tree.item(self.master.tree.selection())['values'][0]
        username = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        if len(password) < 8:
            messagebox.showwarning("Предупреждение", "Пароль должен содержать минимум 8 символов!")
            return
        if self.master.db.update_user(user_id, username, password):
            messagebox.showinfo("Успешно", "Пользователь обновлён!")
            self.destroy()
        else:
            messagebox.showwarning("Ошибка", "Ошибка при обновлении пользователя.")

class SearchUserDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Поиск пользователя")
        self.geometry("400x130+400+300")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Введите имя пользователя для поиска:")
        label_search.place(x=50, y=30)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=60, y=60, width=280)

        btn_search = tk.Button(self, text="Найти", command=self.search_user)
        btn_search.place(x=155, y=90)
        btn_cancel = tk.Button(self, text="Отмена", command=self.destroy)
        btn_cancel.place(x=220, y=90)

        self.grab_set()
        self.focus_set()

    def search_user(self):
        username = self.entry_search.get().strip()
        if not username:
            messagebox.showwarning("Предупреждение", "Введите имя пользователя для поиска!")
            return
        results = self.master.db.select_all_users()
        found = False
        for row in results:
            if username.lower() in row[1].lower():  # Поиск по имени пользователя
                found = True
                break
        if found:
            messagebox.showinfo("Результат поиска", f"Пользователь '{username}' найден!")
        else:
            messagebox.showwarning("Результат поиска", f"Пользователь '{username}' не найден.")
        self.destroy()

def main():
    global main_window
    main_window = MainWindow()  # Инициализируем главное окно приложения
    main_window.mainloop()      # Запускаем основной цикл событий

if __name__ == "__main__":
    main()