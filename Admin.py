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


class Adminapp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()





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
