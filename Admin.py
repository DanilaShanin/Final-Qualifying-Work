import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from PIL import Image, ImageTk
global Main_Window

import matplotlib
import login2
matplotlib.use("TkAgg")

class DB:
    def __init__(self, database_path="users.db"):
        self.database_path = database_path
        self.conn = None
        self.c = None
        self._connect_db()

    def _connect_db(self):
        #Устанавливает соединение с базой данных
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()

    def close_connection(self):
        #Закрывает соединение с базой данных
        if self.conn is not None:
            self.conn.close()

    def insert_user(self, username, password):

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

        query = "DELETE FROM users WHERE id = ?"
        try:
            self.c.execute(query, (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {str(e)}")
            return False

    def select_all_users(self):

        query = "SELECT * FROM users"
        self.c.execute(query)
        return self.c.fetchall()


class Adminapp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()  # создаем объект базы данных
        self.view_records()

    def main(self):
        global main_window
        main_window = login2.MainWindow()  # Инициализируем главное окно приложения
        main_window.mainloop()  # Запускаем основной цикл событий


    def go_back_to_code(self):
        self.master.destroy()
        #global main_window
        main_window = login2.MainWindow()  # Инициализируем главное окно приложения
        main_window.mainloop()
        # Закрываем текущее окно
        # main_window.deiconify()     # Показываем скрытое окно
        # main_window.lift()

    def init_main(self):
        toolbar = tk.Frame(bg='#fe4240', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = ImageTk.PhotoImage(Image.open("img/add.gif"))
        btn_open_dialog = tk.Button(toolbar, text='Добавить ', command=self.open_dialog, bg='#fe4240', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = ImageTk.PhotoImage(Image.open("img/update.gif"))
        btn_edit_dialog = tk.Button(toolbar, text='Внести изменения', bg='#fe4240', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = ImageTk.PhotoImage(Image.open("img/delete.gif"))
        btn_delete = tk.Button(toolbar, text='Удалить авто', bg='#fe4240', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = ImageTk.PhotoImage(Image.open("img/search.gif"))
        btn_search = tk.Button(toolbar, text='Поиск', bg='#fe4240', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = ImageTk.PhotoImage(Image.open("img/refresh.gif"))
        btn_refresh = tk.Button(toolbar, text='Обновить страницу', bg='#fe4240', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.back_img = ImageTk.PhotoImage(Image.open("img/back.gif"))  # Изображение для кнопки возврата
        btn_back = tk.Button(toolbar, text='Вернуться к входу', bg='#fe4240', bd=0, image=self.back_img,
                             compound=tk.TOP, command=self.go_back_to_code)
        btn_back.pack(side=tk.LEFT)



        self.tree = ttk.Treeview(self, columns=('ID', 'username', 'password'),
                                 height=15, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("username", width=150, anchor=tk.CENTER)
        self.tree.column("password", width=300, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("username", text='Имя')
        self.tree.heading("password", text='Пароль')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, username, password):
        # добавляем нового пользователя
        if self.db.insert_user(username, password):
            messagebox.showinfo("Успешно", "Пользователь добавлен!")
        else:
            messagebox.showwarning("Ошибка", "Произошла ошибка при добавлении пользователя.")
        self.view_records()

    def update_record(self, user_id, username, password):
        # обновляем данные пользователя
        if self.db.update_user(user_id, username, password):
            messagebox.showinfo("Успешно", "Данные пользователя обновлены!")
        else:
            messagebox.showwarning("Ошибка", "Произошла ошибка при обновлении данных.")
        self.view_records()

    def delete_records(self, user_id):
        # удаляем пользователя
        if self.db.delete_user(user_id):
            messagebox.showinfo("Успешно", "Пользователь удалён!")
        else:
            messagebox.showwarning("Ошибка", "Произошла ошибка при удалении пользователя.")
        self.view_records()

    def view_records(self):
        # отображаем всех пользователей
        rows = self.db.select_all_users()
        [self.tree.delete(i) for i in self.tree.get_children()]  # очищаем дерево
        [self.tree.insert('', 'end', values=row) for row in rows]

    def open_dialog(self):
        AddUserDialog(self)

    def open_update_dialog(self):
        UpdateUserDialog(self)

    def open_search_dialog(self):
        SearchUserDialog(self)


class AddUserDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить пользователя")
        self.geometry("400x180+400+300")
        self.resizable(False, False)

        self.label_name = tk.Label(self, text="Имя пользователя:")
        self.label_name.place(x=50, y=40)
        self.label_pass = tk.Label(self, text="Пароль:")
        self.label_pass.place(x=50, y=70)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=170, y=40)
        self.entry_pass = ttk.Entry(self, show="*")
        self.entry_pass.place(x=170, y=70)

        self.btn_save = ttk.Button(self, text="Добавить", command=self.add_user)
        self.btn_save.place(x=160, y=120)
        self.btn_cancel = ttk.Button(self, text="Отмена", command=self.destroy)
        self.btn_cancel.place(x=240, y=120)

        self.grab_set()
        self.focus_set()

    def add_user(self):
        username = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        if len(password) < 6:   # Перед сдачей поменять
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

        self.clear_button = ttk.Button(self, text="Очистить", command=lambda: self.entry_pass.delete(0, tk.END))
        self.clear_button.place(x=340, y=65)  # Размещаем кнопку справа от поля ввода пароля

        self.btn_save.config(text="Сохранить", command=self.update_user)

    def update_user(self):
        user_id = self.master.tree.item(self.master.tree.selection())['values'][0]
        username = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
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

            self.entry_search = ttk.Entry(self)
            self.entry_search.place(x=60, y=60, width=280)

            btn_search = ttk.Button(self, text="Найти", command=self.search_user)
            btn_search.place(x=155, y=90)
            btn_cancel = ttk.Button(self, text="Отмена", command=self.destroy)
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
    root = tk.Tk()
    root.title("FootScaut")
    root.geometry("700x450+300+200")
    root.resizable(True, True)
    app = Adminapp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()

