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




class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить пользователя')
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
