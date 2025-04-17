import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from PySide6.QtWidgets import QApplication, QSplashScreen, QProgressBar
from model import DB
import tkinter as tk
import joblib
import joblib
from webbrowser import open
import sklearn
from sklearn.pipeline import Pipeline
root=None

db = DB()
bar=None
class Adminapp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#fe4240', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="img/add.gif")
        btn_open_dialog = tk.Button(toolbar, text='Добавить ', command=self.open_dialog, bg='#fe4240', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='img/update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Внести ищменения', bg='#fe4240', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='img/delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить авто', bg='#fe4240', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='img/search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#fe4240', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='img/refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить страницу', bg='#fe4240', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)





        self.tree = ttk.Treeview(self, columns=('ID', 'username', 'password')
                                 , height=15, show='headings')
        self.tree.column("ID", width=10, anchor=tk.CENTER)
        self.tree.column("username", width=150, anchor=tk.CENTER)
        self.tree.column("password", width=55, anchor=tk.CENTER)


        self.tree.heading("ID", text='ID')
        self.tree.heading("username", text='Имя')
        self.tree.heading("password", text='Пароль')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, username, password):
        self.db.insert_data(username, password)
        self.view_records()

    def update_record(self,username, password):
        self.db.c.execute(
            '''UPDATE users SET username = ?, password = ? WHERE ID=?''',
            (username, password,
             self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM users''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM users WHERE username = ? AND password = ?''', [self.tree.set(selection_item,
                                                                                         '#1')])
        self.db.conn.commit()
        self.view_records()

    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM users WHERE name || 
        username ||
        password LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить игрока')
        self.geometry('1000x1000+400+300')
        #self.resizable(False, False)

        label_Name = tk.Label(self, text='Имя:')
        label_Name.place(x=100, y=25)
        label_Password = tk.Label(self, text='Пароль:')
        label_Password.place(x=100, y=50)


        self.entry_Name = ttk.Entry(self)
        self.entry_Name.place(x=200, y=25)

        self.entry_Password = ttk.Entry(self)
        self.entry_Password.place(x=200, y=50)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=500)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=500)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_Name.get(),
                                                                       self.entry_Password.get()))

        self.grab_set()
        self.focus_set()


    def _get_r(self, r):
        return [*r, r[0]]

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Внесение изменений')
        btn_edit = ttk.Button(self, text='Изменить')
        btn_edit.place(x=200, y=500)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_Name.get(),
                                                                          self.entry_Password.get()))


    def default_data(self):
        self.db.c.execute('''SELECT * FROM users WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_Name.insert(0, row[1])
        self.entry_Password.insert(0, row[2])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск игрока')
        self.geometry('350x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')



def update_progress(value):
    bar.step(value)

def navigate_to_app(root):
    update_progress(100)
    root.destroy()
    root.quit()

def main():

if __name__ == "__main__":
    screensaver()
    global app
    
    root = tk.Tk()
    db = DB()
    app = Adminapp(root)
    app.pack()
    root.title("FootScaut")
    root.geometry("1400x900+300+200")
    root.resizable(True, True)
    root.mainloop()
