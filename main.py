import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model import DB
import tkinter as tk

import joblib
from webbrowser import open
import tensorflow as tf
from tensorflow import keras

import numpy as np

from tkinter import filedialog


root = None

db = DB()
bar = None


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

        self.compare_img = tk.PhotoImage(file='img/comparison.gif')
        btn_compare = tk.Button(toolbar, text='Сравнить авто', bg='#fe4240', bd=0, image=self.compare_img,
                                compound=tk.TOP, command=self.open_compare_dialog)
        btn_compare.pack(side=tk.LEFT)

        self.info = tk.PhotoImage(file='img/instructions.gif')
        btn_info = tk.Button(toolbar, text='Поддержка', command=self.open_info_dialog, bg='#fe4240', bd=0,
                             compound=tk.TOP, image=self.info)

        btn_info.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=(
        'ID', 'Make', 'Name', 'Transmission', 'EngineType', 'EngineCapacity', 'Mileage',
        'City', 'Year', 'Price', 'Trunk', 'Fuel', 'Passengers', 'Doors')
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
        self.tree.column("Trunk", width=100, anchor=tk.CENTER)
        self.tree.column("Fuel", width=100, anchor=tk.CENTER)
        self.tree.column("Passengers", width=100, anchor=tk.CENTER)
        self.tree.column("Doors", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("Make", text='Марка')
        self.tree.heading("Name", text='Наименование')
        self.tree.heading("Transmission", text='Коробка передач')
        self.tree.heading("EngineType", text='Тип двигателя')
        self.tree.heading("EngineCapacity", text='Мощьность двигателя')
        self.tree.heading("Mileage", text='Пробег')
        self.tree.heading("Year", text='Год выпуска')
        self.tree.heading("Price", text='Цена')
        self.tree.heading("Trunk", text='Объем багажника')
        self.tree.heading("Fuel", text='Расход топлива')
        self.tree.heading("Passengers", text='Количество пассажиров')
        self.tree.heading("Doors", text='Количество дверей')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price, Trunk, Fuel,
                Passengers, Doors):
        self.db.insert_data(Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price, Trunk, Fuel, Passengers, Doors)
        self.view_records()

    def update_record(self, Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price, Trunk,
                      Fuel, Passengers, Doors):
        print(self.tree.set)
        self.db.c.execute(
            '''UPDATE carhelper SET Make=?, Name=?, Transmission=?, EngineType=?, EngineCapacity=?, Mileage=?, City=?, Year=?, Price=?,Trunk=?,Fuel=?,Passengers=?,Doors=? WHERE ID=?''',
            (Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price, Trunk, Fuel, Passengers,
             Doors,
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
        Price ||
        Trunk ||
        Fuel ||
        Passengers ||
        Doors LIKE ?''', name)
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

    def open_compare_dialog(self):
        CompareDialog()

    def open_compare_dialog(self):
        CompareDialog(db=self.db)

    # def open_helper_dialog(self):
    #     Helper()

class CompareDialog(tk.Toplevel):
    def __init__(self, db):
        super().__init__(root)
        self.db = db  # Сохраняем ссылку на базу данных
        self.record1 = None  # хранения первой записи
        self.record2 = None  # хранения второй записи
        self.init_compare()
        self.view = app

    def init_compare(self):
        self.title('Сравнение автомобилей')
        self.geometry('800x600+400+300')
        self.resizable(False, False)

        # Дерево для выбора записей
        self.compare_tree = ttk.Treeview(self, columns=('ID', 'Make', 'Name'),
                                         height=15, show='headings')
        self.compare_tree.column("ID", width=10, anchor=tk.CENTER)
        self.compare_tree.column("Make", width=150, anchor=tk.CENTER)
        self.compare_tree.column("Name", width=150, anchor=tk.CENTER)
        self.compare_tree.heading("ID", text='ID')
        self.compare_tree.heading("Make", text='Марка')
        self.compare_tree.heading("Name", text='Модель')
        self.compare_tree.pack(side=tk.LEFT)

        # Область для вывода сравнений
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Кнопки для выбора записей
        btn_select1 = ttk.Button(self, text='Выбрать первую запись', command=self.select_first_record)
        btn_select1.pack(padx=10, pady=10)

        btn_select2 = ttk.Button(self, text='Выбрать вторую запись', command=self.select_second_record)
        btn_select2.pack(padx=10, pady=10)

        # Кнопка для отображения сравнения
        btn_compare = ttk.Button(self, text='Сравнить записи', command=self.display_comparison)
        btn_compare.pack(padx=10, pady=10)


        self.fill_compare_tree()

    def select_first_record(self):
        selected_item = self.compare_tree.selection()
        if not selected_item:
            tk.messagebox.showinfo('Ошибка', 'Не выбрана первая запись.')
            return
        record_id = self.compare_tree.item(selected_item[0])['values'][0]
        self.db.c.execute('''SELECT * FROM carhelper WHERE id=?''', (record_id,))
        self.record1 = self.db.c.fetchone()
        tk.messagebox.showinfo('Информация', 'Первая запись выбрана.')

    def select_second_record(self):
        selected_item = self.compare_tree.selection()
        if not selected_item:
            tk.messagebox.showinfo('Ошибка', 'Не выбрана вторая запись.')
            return
        record_id = self.compare_tree.item(selected_item[0])['values'][0]
        self.db.c.execute('''SELECT * FROM carhelper WHERE id=?''', (record_id,))
        self.record2 = self.db.c.fetchone()
        tk.messagebox.showinfo('Информация', 'Вторая запись выбрана.')

    def display_comparison(self):
        if self.record1 is None or self.record2 is None:
            tk.messagebox.showerror('Ошибка', 'Для сравнения выберите обе записи!')
            return

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        headers = ['Параметр', 'Запись 1', 'Запись 2']
        header_row = tk.Frame(self.result_frame)
        for col, header in enumerate(headers):
            tk.Label(header_row, text=header, font=('Arial', 14)).grid(row=0, column=col, pady=10)
        header_row.pack(fill=tk.X)

        parameters = ['Марка', 'Модель', 'Коробка передач', 'Тип двигателя', 'Мощность двигателя',
                      'Пробег', 'Город', 'Год выпуска', 'Цена', 'Объем багажника',
                      'Расход топлива', 'Количество пассажиров', 'Количество дверей']

        for idx, param in enumerate(parameters):
            param_row = tk.Frame(self.result_frame)
            tk.Label(param_row, text=param, font=(12)).grid(row=idx + 1, column=0, sticky=tk.W)

            # Значения для записей
            value1 = self.record1[idx + 1]
            value2 = self.record2[idx + 1]

            # Определяем цвета для определенных параметров
            bg_color1 = 'white'
            bg_color2 = 'white'

            if param == 'Пробег':
                try:
                    val1 = float(value1)
                    val2 = float(value2)
                    if val1 < val2:
                        bg_color1 = 'lightgreen'
                        bg_color2 = 'lightcoral'
                    elif val1 > val2:
                        bg_color1 = 'lightcoral'
                        bg_color2 = 'lightgreen'
                    else:
                        bg_color1 = bg_color2 = 'lightyellow'
                except (ValueError, TypeError):
                    pass

            elif param == 'Год выпуска':
                try:
                    val1 = int(value1)
                    val2 = int(value2)
                    if val1 > val2:
                        bg_color1 = 'lightgreen'
                        bg_color2 = 'lightcoral'
                    elif val1 < val2:
                        bg_color1 = 'lightcoral'
                        bg_color2 = 'lightgreen'
                    else:
                        bg_color1 = bg_color2 = 'lightyellow'
                except (ValueError, TypeError):
                    pass

            elif param == 'Цена':
                try:
                    val1 = float(value1)
                    val2 = float(value2)
                    if val1 < val2:
                        bg_color1 = 'lightgreen'
                        bg_color2 = 'lightcoral'
                    elif val1 > val2:
                        bg_color1 = 'lightcoral'
                        bg_color2 = 'lightgreen'
                    else:
                        bg_color1 = bg_color2 = 'lightyellow'
                except (ValueError, TypeError):
                    pass

            elif param == 'Расход топлива':
                try:
                    val1 = float(value1)
                    val2 = float(value2)
                    if val1 < val2:
                        bg_color1 = 'lightgreen'
                        bg_color2 = 'lightcoral'
                    elif val1 > val2:
                        bg_color1 = 'lightcoral'
                        bg_color2 = 'lightgreen'
                    else:
                        bg_color1 = bg_color2 = 'lightyellow'
                except (ValueError, TypeError):
                    pass

            tk.Label(param_row, text=value1, font=('Arial', 12), bg=bg_color1).grid(row=idx + 1, column=1)
            tk.Label(param_row, text=value2, font=('Arial', 12), bg=bg_color2).grid(row=idx + 1, column=2)
            param_row.pack(fill=tk.X)
    def fill_compare_tree(self):
        self.db.c.execute('''SELECT id, Make, Name FROM carhelper''')
        rows = self.db.c.fetchall()
        for row in rows:
            self.compare_tree.insert('', 'end', values=row)


class Info(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_info()
        self.view = app

    def init_info(self):
        self.title('Поддержка')
        self.geometry('300x150+40+30')

        # self.resizable(False, False)

        def open_link(event):
            # Ссылка на сайт
            url = 'https://t.me/CarHelpermsk'
            open(url)


        self.title('Поддержка')

        # Создаем метку с текстом и ссылкой
        name_label = tk.Label(self, text='Поддержка:', anchor="w")
        name_label.grid(row=0, column=0, sticky="w")

        # Создание метки-ссылки
        link_label = tk.Label(self, text='Нажмите здесь', fg='blue', cursor='hand2')
        link_label.grid(row=0, column=1, padx=(20, 0))
        link_label.bind('<Button-1>', open_link)

        self.mainloop()


class Helper(tk.Toplevel):
    def __init__(self, eng_cap, mill, year, eng_type, transmission):
        super().__init__()
        self.view = app
        if eng_type == 'Бензин':
            eng_type = 3
        elif eng_type == 'Газ':
            eng_type = 1
        elif eng_type == 'Электрический':
            eng_type = 5

        if transmission == 'Механическая':
            transmission = 1
        elif transmission == 'Автоматическая':
            transmission = 2

        print(eng_cap, mill, year, eng_type, transmission)

        # Загрузка модели из файла
        self.model = joblib.load('forest_pipe.joblib')
        print(self.model.predict([[eng_cap, mill, year, eng_type, transmission]]))



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('1000x1000+400+300')
        # self.resizable(False, False)

        label_Make = tk.Label(self, text='Марка:')
        label_Make.place(x=115, y=25)
        label_Name = tk.Label(self, text='Наименование:')
        label_Name.place(x=115, y=50)

        label_EngineCapacity = tk.Label(self, text='Мощность ДВС:')
        label_EngineCapacity.place(x=115, y=155)
        label_Mileage = tk.Label(self, text='Пробег:')
        label_Mileage.place(x=115, y=180)
        label_City = tk.Label(self, text='Город:')
        label_City.place(x=115, y=205)
        label_Year = tk.Label(self, text='Год выпуска:')
        label_Year.place(x=115, y=230)
        label_Price = tk.Label(self, text='Цена:')
        label_Price.place(x=115, y=255)
        label_Trunk = tk.Label(self, text='Объем багажника:')
        label_Trunk.place(x=100, y=280)
        label_Fuel = tk.Label(self, text='Расход топлива:')
        label_Fuel.place(x=100, y=305)
        label_Passengers = tk.Label(self, text='Количество пассажирв:')
        label_Passengers.place(x=100, y=330)
        label_Doors = tk.Label(self, text='Количество дверей:')
        label_Doors.place(x=100, y=355)

        self.var = tk.StringVar()
        self.var.trace_add("write", self.graf)

        self.var1 = tk.StringVar()
        self.var1.trace_add("write", self.graf)

        self.var2 = tk.StringVar()
        self.var2.trace_add("write", self.graf)

        self.var3 = tk.StringVar()
        self.var3.trace_add("write", self.graf)

        self.var4 = tk.StringVar()
        self.var4.trace_add("write", self.graf)

        self.var5 = tk.StringVar()
        self.var5.trace_add("write", self.graf)
        self.var6 = tk.StringVar()
        self.var6.trace_add("write", self.graf)

        self.var7 = tk.StringVar()
        self.var7.trace_add("write", self.graf)

        self.entry_Make = ttk.Entry(self)
        self.entry_Make.place(x=250, y=25)

        self.entry_Name = ttk.Entry(self)
        self.entry_Name.place(x=250, y=50)

        transmission_types = ["Механическая", "Автоматическая"]
        self.transmission = tk.StringVar(self)
        self.transmission.set(transmission_types[0])
        tk.Label(self, text="Тип трансмиссии:").place(x=100, y=90)
        tk.OptionMenu(self, self.transmission, *transmission_types).place(x=250, y=90)

        Engine_types = ["Бензин", "Газ", "Электрический"]
        self.EngineType = tk.StringVar(self)
        self.EngineType.set(Engine_types[0])
        tk.Label(self, text="Тип двигателя:").place(x=100, y=130)
        tk.OptionMenu(self, self.EngineType, *Engine_types).place(x=250, y=130)

        self.entry_EngineCapacity = ttk.Entry(self, textvariable=self.var)
        self.entry_EngineCapacity.place(x=250, y=155)

        self.entry_Mileage = ttk.Entry(self, textvariable=self.var1)
        self.entry_Mileage.place(x=250, y=180)

        self.entry_City = ttk.Entry(self)
        self.entry_City.place(x=250, y=205)

        self.entry_Year = ttk.Entry(self, textvariable=self.var2)
        self.entry_Year.place(x=250, y=230)

        self.entry_Price = ttk.Entry(self, textvariable=self.var3)
        self.entry_Price.place(x=250, y=255)

        self.entry_Trunk = ttk.Entry(self, textvariable=self.var4)
        self.entry_Trunk.place(x=250, y=280)

        self.entry_Fuel = ttk.Entry(self, textvariable=self.var5)
        self.entry_Fuel.place(x=250, y=305)

        self.entry_Passengers = ttk.Entry(self, textvariable=self.var6)
        self.entry_Passengers.place(x=250, y=330)

        self.entry_Doors = ttk.Entry(self, textvariable=self.var7)
        self.entry_Doors.place(x=250, y=355)

        f = Figure(figsize=(8, 8), dpi=50)
        a = f.add_subplot(111, projection='polar')

        labels = ["Мощность двигателя", "Пробег", "год", "Цена", "Объем багажника", "Расход топлива",
                  "Количество пассажирв", "Количество дверей"]


        btn_pred = ttk.Button(self, text='Анализ цены', command=self.pred_m)
        btn_pred.place(x=100, y=600)

        btn_pred = ttk.Button(self, text='Оценка авто', command=self.evaluate_car)
        btn_pred.place(x=200, y=700)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=400, y=600)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=250, y=600)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_Make.get(),
                                                                       self.entry_Name.get(),
                                                                       self.transmission.get(),
                                                                       self.EngineType.get(),
                                                                       self.entry_EngineCapacity.get(),
                                                                       self.entry_Mileage.get(),
                                                                       self.entry_City.get(),
                                                                       self.entry_Year.get(),
                                                                       self.entry_Price.get(),
                                                                       self.entry_Trunk.get(),
                                                                       self.entry_Fuel.get(),
                                                                       self.entry_Passengers.get(),
                                                                       self.entry_Doors.get()))

        self.grab_set()
        self.focus_set()

        f = Figure(figsize=(8, 8), dpi=100)
        f.set_size_inches(5, 5)
        a = f.add_subplot(111, projection='polar')
        self.ax = a.axes

        self.canvas = FigureCanvasTkAgg(f, self)

        self.canvas.get_tk_widget().pack(side=tk.RIGHT)

    def evaluate_car(self):

        # Размеры изображения
        img_width, img_height = 150, 150

        # Загрузка модели для распознавания повреждений
        model = keras.models.load_model('/Users/danilashanin/Desktop/Диплом/CarHelper/best_modelll.h5')

        # Параметры директории и классов
        files = filedialog.askopenfiles()
        path = ''
        if len(files) != 0:
            path = files[0].name
        val_dir = path  # '/Users/danilashanin/Desktop/Диплом/CarHelper/7905.jpg'
        class_names = ["00-good", "01-minor", "02-moderate", "03-severe"]


        if True:
            # Загружаем изображение
            img = tf.keras.preprocessing.image.load_img(val_dir, target_size=(img_width, img_height))
            img = tf.keras.preprocessing.image.img_to_array(img)
            img = img / 255.0
            img = tf.expand_dims(img, axis=0)

            # Делаем предсказание
            pred = model.predict(img)
            pred_label = class_names[np.argmax(pred)]
            print(pred_label)
            car_rate = {
                '00-good': 1,
                '01-minor': 0.93,
                '02-moderate': 0.7,
                '03-severe': 0.3
            }
            self.var3.set(float(self.entry_Price.get()) * car_rate[pred_label])
            print(self.entry_Price)

    def pred_m(self):
        eng_type = self.EngineType.get()
        if eng_type == 'Бензин':
            eng_type = 3
        elif eng_type == 'Газ':
            eng_type = 1
        elif eng_type == 'Электрический':
            eng_type = 5

        transmission = self.transmission.get()
        if transmission == 'Механическая':
            transmission = 1
        elif transmission == 'Автоматическая':
            transmission = 2

        # print(eng_cap, mill, year, eng_type, transmission)

        # Загрузка модели из файла
        self.model = joblib.load('forest_pipe.joblib')
        value = self.model.predict([[self.entry_EngineCapacity.get(),
                                     self.entry_Mileage.get(),
                                     self.entry_Year.get(), eng_type, transmission]])
        self.entry_Price.delete(0, tk.END)
        self.entry_Price.insert(0, round(value[0], 2))
        # self.entry_Price=[]

        # f = Figure(figsize=(8, 8), dpi=100)
        # a = f.add_subplot(111, projection='polar')
        #
        # labels = ["Мощность двигателя", "Пробег", "год", "Цена", "Объем багажника", "Расход топлива", "Количество пассажирв", "Количество дверей"]

        # r = [100, 7, 9, 6, 1, 8,8,8]
        # theta = np.deg2rad(np.linspace(0, 360, 9))
        #
        # a.axes.set_xticklabels(labels)
        # a.axes.set_ylim(100)
        # a.axes.set_xticks(theta)
        # a.axes.plot(theta, self._get_r(r), color='black')
        #
        # self.ax = a.axes
        #
        # self.canvas = FigureCanvasTkAgg(f, self)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(side=tk.RIGHT)

    def graf(self, name, index, mode, *args):
        # try:
        if 1:
            # f = Figure(figsize=(8, 8), dpi=100)
            # a = f.add_subplot(111, projection='polar')
            # self.ax = a.axes

            labels = ["Мощность двигателя", "Пробег", "год", "Цена", "Объем багажника", "Расход топлива",
                      "Количество пассажирв", "Количество дверей"]

            theta = np.deg2rad(np.linspace(0, 360, 9))
            r = [float(self.var.get()),
                 float(self.var1.get()),
                 float(self.var2.get()),
                 float(self.var3.get()),
                 float(self.var4.get()),
                 float(self.var5.get()),
                 float(self.var6.get()),
                 float(self.var7.get())]
            self.ax.clear()
            self.ax.set_xticklabels(labels)
            self.ax.set_yscale('log')
            self.ax.set_xticks(theta)
            self.ax.plot(theta, self._get_r(r), color='black')
            # self.canvas.delete('all')
            # self.canvas = FigureCanvasTkAgg(f, self)
            self.canvas.draw()
            # self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # except:
        #     pass

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
                                                                          self.entry_Price.get(),
                                                                          self.entry_Trunk.get(),
                                                                          self.entry_Fuel.get(),
                                                                          self.entry_Passengers.get(),
                                                                          self.entry_Doors.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM carhelper WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_Make.insert(0, row[1])
        self.entry_Name.insert(0, row[2])
        self.transmission.set(row[3])
        self.EngineType.set(row[4])
        self.entry_EngineCapacity.insert(0, row[5])
        self.entry_Mileage.insert(0, row[6])
        self.entry_City.insert(0, row[7])
        self.entry_Year.insert(0, row[8])
        self.entry_Price.insert(0, row[9])
        self.entry_Trunk.insert(0, row[10])
        self.entry_Fuel.insert(0, row[11])
        self.entry_Passengers.insert(0, row[12])
        self.entry_Doors.insert(0, row[13])
        self.entry_Price.insert(0, row[14])


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
        btn_cancel.place(x=250, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=150, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


def update_progress(value):
    bar.step(value)


def navigate_to_app(root):
    update_progress(100)
    root.destroy()
    root.quit()


def main():
    # if __name__ == "__main__":
    # screensaver()
    global app

    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Car Helper")
    root.geometry("1400x900+300+200")
    root.resizable(True, True)
    root.mainloop()
