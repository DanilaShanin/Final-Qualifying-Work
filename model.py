
import sqlite3
import matplotlib
matplotlib.use("TkAgg")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('carhelper.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS carhelper (id integer primary key, Make text, Name text, Transmission text,
            EngineType text, EngineCapacity text ,Mileage text, City text, Year text,  Price text,Trunk text,Fuel text,Passengers text,Doors text)''')
        self.conn.commit()

    def insert_data(self, Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year,  Price ,Trunk ,Fuel ,Passengers,Doors):
        self.c.execute('''INSERT INTO carhelper (Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price,Trunk ,Fuel ,Passengers,Doors) VALUES (?, ?, ?, ?, ?, ?, ?,?, ?,?,?,?,?)''',
                       (Make, Name, Transmission, EngineType, EngineCapacity, Mileage, City, Year, Price,Trunk ,Fuel ,Passengers,Doors))
        self.conn.commit()