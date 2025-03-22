import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")

from model import DB
import tkinter as tk


root = None

db = DB()
bar = None
global app


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#fe4240', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="img/add.gif")
        btn_open_dialog = tk.Button(toolbar, text='Добавить авто', command=self.open_dialog, bg='#fe4240', bd=0,
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

        self.helper_img = tk.PhotoImage(file="img/add.gif")
        btn_open_helper_dialog = tk.Button(toolbar, text='помочник', command=self.open_helper_dialog, bg='#fe4240',
                                           bd=0,
                                           compound=tk.TOP, image=self.add_img)
        btn_open_helper_dialog.pack(side=tk.LEFT)

        self.info = tk.PhotoImage(file="img/add.gif")
        btn_info = tk.Button(toolbar, text='Инструкция', command=self.open_info_dialog, bg='#fe4240', bd=0,
                             compound=tk.TOP, image=self.add_img)

        btn_info.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=(
        'ID', 'Make', 'Name', 'Transmission', 'EngineType', 'EngineCapacity', 'Mileage',
        'City', 'Year', 'Price')
                                 , height=15, show='headings')
        self.tree.column("ID", width=10, anchor=tk.CENTER)
        self.tree.column("Make", width=150, anchor=tk.CENTER)
        self.tree.column("Name", width=55, anchor=tk.CENTER)
        self.tree.column("Transmission", width=55, anchor=tk.CENTER)
        self.tree.column("EngineType", width=150, anchor=tk.CENTER)
        self.tree.column("EngineCapacity", width=400, anchor=tk.CENTER)
        self.tree.column("Mileage", width=100, anchor=tk.CENTER)
        self.tree.column("City", width=150, anchor=tk.CENTER)
        self.tree.column("Year", width=100, anchor=tk.CENTER)
        self.tree.column("Price", width=100, anchor=tk.CENTER)
        # self.tree.column("pace", width=100, anchor=tk.CENTER)
        # self.tree.column("shooting", width=100, anchor=tk.CENTER)
        # self.tree.column("passing", width=100, anchor=tk.CENTER)
        # self.tree.column("dribbling", width=100, anchor=tk.CENTER)
        # self.tree.column("defending", width=100, anchor=tk.CENTER)
        # self.tree.column("physicality", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("Make", text='Марка')
        self.tree.heading("Name", text='Наименование')
        self.tree.heading("Transmission", text='Коробка передач')
        self.tree.heading("EngineType", text='Тип двигателя')
        self.tree.heading("EngineCapacity", text='Мощьность двигателя')
        self.tree.heading("Mileage", text='Пробег')
        self.tree.heading("Year", text='Год выпуска')
        self.tree.heading("Price", text='Цена')
        # self.tree.heading("pace", text='Скорость')
        # self.tree.heading("shooting", text='Удар')
        # self.tree.heading("passing", text='Предачи')
        # self.tree.heading("dribbling", text='Дриблинг')
        # self.tree.heading("defending", text='Дриблинг')
        # self.tree.heading("physicality", text='Физика')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price):
        self.db.insert_data(Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price)
        self.view_records()

    def update_record(self, Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price):
        self.db.c.execute(
            '''UPDATE carhelper SET Make=?, Name=?, Transmission=?, EngineType=?, EngineCapacity=?, Mileage=?, City=?, Year=?, Price=? WHERE ID=?''',
            (Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price,
             self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM carhelper''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM carhelper WHERE id=?''', [self.tree.set(selection_item,
                                                                                     '#1')])
        self.db.conn.commit()
        self.view_records()

    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM carhelper WHERE name || 
        Make ||
        Name || 
        Transmission || 
        EngineType || 
        EngineCapacity|| 
        Mileage|| 
        City || 
        Year || 
        Price LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def open_info_dialog(self):
        Info()


class Info(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_info()
        self.view = app

    def init_info(self):
        self.title('Инструкция')
        self.geometry('300x150+40+30')

        # self.resizable(False, False)

        def open_link(event):
            # Ссылка на сайт
            url = 'https://rutube.ru/video/f8cdfddf0fa59963d92fde841bfde0fb/?r=wd'
            open(url)

        def open_link1(event):
            url1 = 'https://example.com'
            open(url1)

        def open_link2(event):
            url2 = 'https://example.com'
            open(url2)

        def open_link3(event):
            url3 = 'https://example.com'
            open(url3)

        def open_link4(event):
            url4 = 'https://example.com'
            open(url4)

        self.title('Пример приложения')

        # Создаем метку с текстом и ссылкой
        name_label = tk.Label(self, text='Введение:', anchor="w")
        name_label.grid(row=0, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=0, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link)

        name_label = tk.Label(self, text='Добавлнение', anchor="w")
        name_label.grid(row=2, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=2, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link1)

        name_label = tk.Label(self, text='Изменение и обнавление', anchor="w")
        name_label.grid(row=3, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=3, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link2)

        name_label = tk.Label(self, text='Удаление', anchor="w")
        name_label.grid(row=4, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=4, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link3)

        name_label = tk.Label(self, text='помощник', anchor="w")
        name_label.grid(row=5, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=5, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link4)

        self.mainloop()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('1000x1000+400+300')
        # self.resizable(False, False)

        label_Make = tk.Label(self, text='Имя:')
        label_Make.place(x=100, y=25)
        label_Name = tk.Label(self, text='Возраст:')
        label_Name.place(x=100, y=50)

        label_EngineType = tk.Label(self, text='Позиция')
        label_EngineType.place(x=100, y=100)
        label_EngineCapacity = tk.Label(self, text='Информация:')
        label_EngineCapacity.place(x=100, y=125)
        label_Mileage = tk.Label(self, text='Гражданство:')
        label_Mileage.place(x=100, y=150)
        label_City = tk.Label(self, text='Клуб:')
        label_City.place(x=100, y=175)
        label_Year = tk.Label(self, text='Цена:')
        label_Year.place(x=100, y=200)
        label_Price = tk.Label(self, text='Цена:')
        label_Price.place(x=100, y=200)

        self.entry_Make = ttk.Entry(self)
        self.entry_Make.place(x=200, y=25)

        self.entry_Name = ttk.Entry(self)
        self.entry_Name.place(x=200, y=50)

        transmission_types = ["Механическая", "Автоматическая", "Вариатор"]
        self.transmission = tk.StringVar(self)
        self.transmission.set(transmission_types[0])
        tk.Label(self, text="Тип трансмиссии:").place(x=200, y=75)
        tk.OptionMenu(self, self.transmission, *transmission_types).place(x=200, y=85)

        Engine_types = ["Бнензин", "Газ", "Вариатор"]
        self.EngineType = tk.StringVar(self)
        self.EngineType.set(Engine_types[0])
        tk.Label(self, text="Тип трансмиссии:").place(x=200, y=100)
        tk.OptionMenu(self, self.EngineType, *Engine_types).place(x=200, y=100)

        self.entry_EngineCapacity = ttk.Entry(self)
        self.entry_EngineCapacity.place(x=200, y=125)

        self.entry_Mileage = ttk.Entry(self)
        self.entry_Mileage.place(x=200, y=150)

        self.entry_City = ttk.Entry(self)
        self.entry_City.place(x=200, y=175)

        self.entry_Year = ttk.Entry(self)
        self.entry_Year.place(x=200, y=200)

        self.entry_Price = ttk.Entry(self)
        self.entry_Price.place(x=200, y=200)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=500)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=500)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_Make.get(),
                                                                       self.entry_Name.get(),
                                                                       self.transmission.get(),
                                                                       self.EngineType.get(),
                                                                       self.entry_EngineCapacity.get(),
                                                                       self.entry_Mileage.get(),
                                                                       self.entry_City.get(),
                                                                       self.entry_Year.get(),
                                                                       self.entry_Price.get()))

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
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_Make.get(),
                                                                          self.entry_Name.get(),
                                                                          self.transmission.get(),
                                                                          self.EngineType.get(),
                                                                          self.entry_EngineCapacity.get(),
                                                                          self.entry_Mileage.get(),
                                                                          self.entry_City.get(),
                                                                          self.entry_Year.get(),
                                                                          self.entry_Price.get()))
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM carhelper WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_Make.insert(0, row[1])
        self.entry_Name.insert(0, row[2])
        self.transmission.insert(0, row[3])
        self.EngineType.insert(0, row[4])
        self.entry_EngineCapacity.insert(0, row[5])
        self.entry_Mileage.insert(0, row[6])
        self.entry_City.insert(0, row[7])
        self.entry_Year.insert(0, row[8])
        self.entry_Price.insert(0, row[9])


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



    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Car Helper")
    root.geometry("1400x900+300+200")
    root.resizable(True, True)
    root.mainloop()
