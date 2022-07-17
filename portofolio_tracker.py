'''
Finance Dashboard : Multiple Crypto Charts w/ Indicators
'''

'''IMPORTS MATPLOTLIB BINANCA_API TKTINTER PANDAS'''

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import mplfinance as mplf

from binance import Client

import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np

from functions_database import *

'''VARIABLES'''
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")

fig = Figure(figsize=(5,5), dpi=150)
a = fig.add_subplot(111)

def animate(i):
    headers = ["Asset", "Volume"]

    df = pd.read_csv("portfolio.csv", names=headers)
    df = df.set_index('Asset')
    index = ["BTC", "ETH"]

    plt.clf()
    plt.bar(index, df.iloc[:,0], color='b')
    plt.ylim(bottom=0, top=5000000)
    plt.show()


class PortfolioTracker(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Live Portfolio Tracker")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Live Tracking of Exchange Holdings", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Quit", command=quit)
        button.pack()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = PortfolioTracker()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
