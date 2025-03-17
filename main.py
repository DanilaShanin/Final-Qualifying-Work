import tkinter as tk
from tkinter import ttk
import sqlite3
from model import DB
db = DB()
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

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


        self.tree = ttk.Treeview(self, columns=(
        'ID', 'Make', 'Name', 'Transmission', 'EngineType', 'EngineCapacity', 'Mileage', 'City', 'Year', 'Price')
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

        self.tree.heading("ID", text='ID')
        self.tree.heading("Make", text='Марка')
        self.tree.heading("Name", text='Наименование')
        self.tree.heading("Transmission", text='Коробка передач')
        self.tree.heading("EngineType", text='Тип двигателя')
        self.tree.heading("EngineCapacity", text='Мощьность двигателя')
        self.tree.heading("Mileage", text='Пробег')
        self.tree.heading("Year", text='Год выпуска')
        self.tree.heading("Price", text='Цена')


        self.tree.pack(side=tk.LEFT)

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

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title('Добавить')
        self.geometry('1000x1000+400+300')

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

        self.entry_Name = ttk.Entry(self)
        self.entry_Name.place(x=200, y=50)

        self.entry_Name = ttk.Entry(self)
        self.entry_Name.place(x=200, y=50)

        self.transmission = ttk.Entry(self)
        self.transmission.place(x=200, y=75)

        self.EngineType = ttk.Entry(self)
        self.EngineType.place(x=200, y=100)


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


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Car Helper")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()