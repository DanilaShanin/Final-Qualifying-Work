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
        btn_open_helper_dialog = tk.Button(toolbar, text='помочник', command=self.open_helper_dialog, bg='#fe4240', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_helper_dialog.pack(side=tk.LEFT)

        self.info = tk.PhotoImage(file="img/add.gif")
        btn_info = tk.Button(toolbar, text='Инструкция', command=self.open_info_dialog, bg='#fe4240', bd=0,
                                    compound=tk.TOP, image=self.add_img)

        btn_info.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Make', 'Name', 'Transmission', 'EngineType', 'EngineCapacity', 'Mileage',
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

    def open_helper_dialog(self):
        Helper()



class Info(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_info()
        self.view = app

    def init_info(self):
        self.title('Инструкция')
        self.geometry('300x150+40+30')
        #self.resizable(False, False)

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
        # print(self.model.predict([[self.entry_EngineCapacity.get(),self.entry_Mileage.get(),self.entry_Year.get(),self.EngineType.get(),self.transmission.get()]]))

        # self.entry_Make.get(),
        # self.entry_Name.get(),
        # self.transmission.get(),
        # self.EngineType.get(),
        # self.entry_EngineCapacity.get(),
        # self.entry_Mileage.get(),
        # self.entry_City.get(),
        # self.entry_Year.get(),
        # self.entry_Price.get()))

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        self.title('Добавить')
        self.geometry('1000x1000+400+300')
        #self.resizable(False, False)

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
        # label_pace = tk.Label(self, text='Скорость:')
        # label_pace.place(x=100, y=225)
        # label_shooting = tk.Label(self, text='Удар:')
        # label_shooting.place(x=100, y=250)
        # label_passing = tk.Label(self, text='Передачи:')
        # label_passing.place(x=100, y=275)
        # label_dribbling = tk.Label(self, text='Дриблинг:')
        # label_dribbling.place(x=100, y=300)
        # label_defending = tk.Label(self, text='Оборона:')
        # label_defending.place(x=100, y=325)
        # label_physicality = tk.Label(self, text='Физика:')
        # label_physicality.place(x=100, y=350)
        #
        # self.var = tk.StringVar()
        # self.var.trace_add("write", self.graf)
        #
        # self.var1 = tk.StringVar()
        # self.var1.trace_add("write", self.graf)
        #
        # self.var2 = tk.StringVar()
        # self.var2.trace_add("write", self.graf)
        #
        # self.var3 = tk.StringVar()
        # self.var3.trace_add("write", self.graf)
        #
        # self.var4 = tk.StringVar()
        # self.var4.trace_add("write", self.graf)
        #
        # self.var5 = tk.StringVar()
        # self.var5.trace_add("write", self.graf)

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


        self.entry_EngineCapacity = ttk.Entry(self)
        self.entry_EngineCapacity.place(x=250, y=155)

        self.entry_Mileage = ttk.Entry(self)
        self.entry_Mileage.place(x=250, y=180)

        self.entry_City = ttk.Entry(self)
        self.entry_City.place(x=250, y=205)

        self.entry_Year = ttk.Entry(self)
        self.entry_Year.place(x=250, y=230)

        self.entry_Price = ttk.Entry(self)
        self.entry_Price.place(x=250, y=255)

        # self.entry_pace = ttk.Entry(self, textvariable=self.var)
        # self.entry_pace.place(x=200, y=225)
        #
        # self.entry_shooting = ttk.Entry(self, textvariable=self.var1)
        # self.entry_shooting.place(x=200, y=250)
        #
        # self.entry_passing = ttk.Entry(self, textvariable=self.var2)
        # self.entry_passing.place(x=200, y=275)
        #
        # self.entry_dribbling = ttk.Entry(self, textvariable=self.var3)
        # self.entry_dribbling.place(x=200, y=300)
        #
        # self.entry_defending = ttk.Entry(self, textvariable=self.var4)
        # self.entry_defending.place(x=200, y=325)
        #
        # self.entry_physicality = ttk.Entry(self, textvariable=self.var5)
        # self.entry_physicality.place(x=200, y=350)
        #
        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111, projection='polar')
        #
        # labels = ["Скорость", "Удар", "Передачи", "Дриблинг", "Оборона", "Физика"]
        #
        # r = [100, 7, 9, 6, 1, 8]
        # theta = np.deg2rad(np.linspace(0, 360, 7))
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

        # btn_pred = ttk.Button(self, text='Predict', command=lambda: Helper(self.entry_EngineCapacity.get(),self.entry_Mileage.get(),self.entry_Year.get(),self.EngineType.get(),self.transmission.get()))
        # btn_pred = ttk.Button(self, text='Predict', command=Helper)
        btn_pred = ttk.Button(self, text='Анализ цены', command=self.pred_m)
        btn_pred.place(x=100, y=500)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=400, y=500)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=250, y=500)
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

    def pred_m(self):
        # Загрузка модели из файла
        self.model = joblib.load('forest_pipe.joblib')
        value = self.model.predict([[self.entry_EngineCapacity.get(),
                                    self.entry_Mileage.get(),
                                   self.entry_Year.get(), eng_type, transmission]])
        self.entry_Price.delete(0, tk.END)
        self.entry_Price.insert(0,round(value[0],2))

    # def graf(self, name, index,mode, *args):
    #     try:
    #
    #         # f = Figure(figsize=(5, 5), dpi=100)
    #         # a = f.add_subplot(111, projection='polar')
    #         #
    #         labels = ["Скорость", "Удар", "Передачи", "Дриблинг", "Оборона", "Физика"]
    #
    #         r = [int(self.var.get()),
    #              int(self.var1.get()),
    #              int(self.var2.get()),
    #              int(self.var3.get()),
    #              int(self.var4.get()),
    #              int(self.var5.get())]
    #         theta = np.deg2rad(np.linspace(0, 360, 7))
    #         self.ax.clear()
    #         self.ax.set_xticklabels(labels)
    #         #
    #         self.ax.set_xticks(theta)
    #         self.ax.plot(theta, self._get_r(r), color='black')
    #         # self.canvas.delete('all')
    #         # self.canvas = FigureCanvasTkAgg(f, self)
    #         self.canvas.draw()
    #         # self.canvas.get_tk_widget().pack(side=tk.RIGHT)
    #     except:
    #         pass

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
                                                                          # self.entry_pace.get(),
                                                                          # self.entry_shooting.get(),
                                                                          # self.entry_passing.get(),
                                                                          # self.entry_dribbling.get(),
                                                                          # self.entry_defending.get(),
                                                                          # self.entry_physicality.get()))
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
        # self.entry_pace.insert(0, row[9])
        # self.entry_shooting.insert(0, row[10])
        # self.entry_passing.insert(0, row[11])
        # self.entry_dribbling.insert(0, row[12])
        # self.entry_defending.insert(0, row[13])
        # self.entry_physicality.insert(0, row[14])



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


# def screensaver():
#     from tk_loader import Screensaver
#     from random import randint
#
#     global bar
#
#     saver = tk.Tk()
#     load_screen = Screensaver(saver, progress_func=update_progress, go_next=lambda: navigate_to_app(saver))
#
#     # image_id = randint(1, 4)
#     # load_screen.play_gif(f'loading_gifs/{image_id}.gif', 0.03)
#
#     bar = ttk.Progressbar(orient='horizontal')
#     bar.pack(fill='both')
#     saver.title("FootScaut")
#     saver.mainloop()
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
