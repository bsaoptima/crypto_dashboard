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

resampleSize = "15min"  # timeframe of the candlestick
DataPace = "tick"  # how much overall data will be considered
candleWidth = 0.008
DataCounter = 9000
paneCount = 1

topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
EMAs = []
SMAs = []

chartLoad = True

style.use("ggplot")

api_key = 'vNSi2ulNVJi6ZpG8Fh23VWv6oDDwpiLJpHeUbMFL17xKfu0cDvKK0Ek6H9xG0WCZ'
sec_key = 'teOpkDsKwG7zHUKyTarsqxRFOhzyBVpehvXBryOj86M6DZ6JrF3w80PQxENUYYcW'

# initiating the API Client
client = Client(api_key, sec_key)
asset = 'BTCUSDT'

options = ("BTCUSDT", "ETHUSDT")

# Creating Figure and adding sub_subplot

fig = mplf.figure(figsize=(8.5,4.8))

ax, av = fig.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [4, 1]})


portfolio = pd.DataFrame({
            "Asset" : ["BTC", "ETH"],
            "Volume" : [1000000, 2000000],
        })
portfolio = portfolio.set_index('Asset')

''''''''''''''''''''''''''''''''''''''''''''''''''''''
# -----------------FUNCTIONS---------------------------
''''''''''''''''''''''''''''''''''''''''''''''''''''''


# F1 : Retrieves minute data and dumps it into Pandas DF when called
def getminutedata(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC'))  # retrieving data
    frame = frame.iloc[:, :6]  # All Rows but only 6 columns
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')  # changing time from unix to ms
    frame = frame.astype(float)  # Changing data type from txt
    return frame

# F2 : Creates / Updates Dataframe each iteration
def animate(i):
    global refreshRate
    global DataCounter

    data = getminutedata(asset, '1m', '30')

    ax.clear()
    av.clear()

    mplf.plot(data, type='candle', ax=ax, volume=av, axtitle='test', style='yahoo')

# F3 : Pop up message
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")

    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()

    popup.mainloop()

def changeTimeFrame(tf):
    global DataPace
    global DataCounter

    if tf == "7d" and resampleSize == "1min":  # too many candlesticks to display
        popupmsg("Too much data chosen, please smaller time frame")
    else:
        DataPace = tf
        DataCounter = 9000

def changeSampleSize(size, width):
    global resampleSize
    global candleWidth
    global DataCounter

    if DataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval.")
    elif DataPace == "tick":
        popupmsg("Currently viewing tick data, not OHLC.")
    else:
        resampleSize = size
        DataCounter = 9000
        candleWidth = width

def addTopIndicator(what):
    global topIndicator
    global DataCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")
    elif what == "none":
        topIndicator = what
        DataCounter = 9000
    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Period ?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want considered")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DataCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            DataCounter = 9000
            print("Set top indicator to", group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        topIndicator = "macd"
        DataCounter = 9000

def addBottomIndicator(what):
    global bottomIndicator
    global DataCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")
    elif what == "none":
        bottomIndicator = what
        DataCounter = 9000
    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Period ?")
        label = ttk.Label(rsiQ, text="Choose how many periods you want considered")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global DataCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            DataCounter = 9000
            print("Set bottom indicator to", group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        bottomIndicator = "macd"
        DataCounter = 9000

def addMiddleIndicator(what):
    global middleIndicator
    global DataCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")
    if what != "none":
        if middleIndicator == "none":
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your SMA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DataCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DataCounter = 9000
                    print("middle indicator set to :", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                label = ttk.Label(midIQ, text="Choose how many periods you want your MA to be.")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DataCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DataCounter = 9000
                    print("middle indicator set to : ", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width="10", command=callback)
                b.pack()
                tk.mainloop()

    else:
        middleIndicator = "none"

def loadChart(run):
    global chartLoad

    if run == "start":
        chartLoad = True
    elif run == "stop":
        chartLoad = False

def changeAsset(what):
    global asset
    global DataCounter

    asset = what
    DataCounter = 9000

def placeOrder(action, what, volume):
    global portfolio

    print(volume)

    if action == "buy":
        if volume < portfolio["Volume"][what]:
            portfolio["Volume"][what] -= volume
            print(portfolio)
            portfolio.to_csv("portfolio.csv", mode='w', header=False)

    if action == "sell":
        portfolio["Volume"][what] += volume
        print(portfolio)
        portfolio.to_csv("portfolio.csv", mode='w', header=False)

''''''''''''''''''''''''''''''''''''''''''''''''''''''
# ---------------------MAIN---------------------------
''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Main Class, describes actual GUI
class SeaofBTCapp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Finance Dashboard")

        # creates the the main container
        container = tk.Frame(self)
        container.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        #container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_rowconfigure(3, weight=1)
        container.grid_rowconfigure(4, weight=5)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Dict containing all the frames
        self.frames = {}

        #Creating the Exchange Portfolio
        self.portfolio = pd.DataFrame({
            "Asset" : ["BTC", "ETH"],
            "Volume" : [1000000, 2000000],
        })
        self.portfolio = self.portfolio.set_index('Asset')

        # menubar creation
        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label='Tick', command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label='1 Day', command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label='3 Day', command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label='1 Week', command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label='Data Time Frame', menu=dataTF)

        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label='Tick', command=lambda: changeSampleSize('tick'))
        OHLCI.add_command(label='1 minute', command=lambda: changeSampleSize('1Min', 0.0005))
        OHLCI.add_command(label='5 minute', command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label='15 minute', command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label='30 minute', command=lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label='1 hour', command=lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label='3 hour', command=lambda: changeSampleSize('3H', 0.096))
        menubar.add_cascade(label='OHLC Interval', menu=OHLCI)

        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label="None", command=lambda: addTopIndicator('none'))
        topIndi.add_separator()
        topIndi.add_command(label="RSI", command=lambda: addTopIndicator('rsi'))
        topIndi.add_command(label="MACD", command=lambda: addTopIndicator('macd'))
        menubar.add_cascade(label="Top Indicator", menu=topIndi)

        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label="None", command=lambda: addMiddleIndicator('none'))
        mainI.add_separator()
        mainI.add_command(label="sma", command=lambda: addMiddleIndicator('sma'))
        mainI.add_command(label="ema", command=lambda: addMiddleIndicator('ema'))
        menubar.add_cascade(label="Main Indicator", menu=mainI)

        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label="None", command=lambda: addBottomIndicator('none'))
        bottomI.add_separator()
        bottomI.add_command(label="sma", command=lambda: addBottomIndicator('sma'))
        bottomI.add_command(label="ema", command=lambda: addBottomIndicator('ema'))
        menubar.add_cascade(label="Main Indicator", menu=bottomI)

        tradeB = tk.Menu(menubar, tearoff=1)
        tradeB.add_command(label="Quick Buy", command=lambda: popupmsg("Not live yet"))
        tradeB.add_command(label="Quick Sell", command=lambda: popupmsg("Not live yet"))
        menubar.add_cascade(label="Trading", menu=tradeB)

        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label="resume", command=lambda: loadChart('start'))
        startStop.add_command(label="pause", command=lambda: loadChart('stop'))
        menubar.add_cascade(label="Resume / Pause Client", menu=startStop)

        # adds GUI configuration, in this case menubar
        tk.Tk.config(self, menu=menubar)

        # adding the available frames to the Dict
        for F in (StartPage, Chart_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #show first page initially
        self.show_frame(StartPage)

    '''-------------------METHODS----------------------'''
    # internal function of the GUI that displays Frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def placeOrder(self, action, what, volume):
        if action == "buy":
            if volume < self.portfolio["Volume"][what]:
                self.portfolio["Volume"][what] -= volume
                print(self.portfolio)

        if action == "sell":
            self.portfolio["Volume"][what] += volume
            print(self.portfolio)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text=("Finance Dashboard multiple indicators."), font=LARGE_FONT)
        label.pack(ipady=10, ipadx=10)

        button2 = tk.Button(self, text="Enter Exchange",
                             command=lambda: [controller.show_frame(Chart_Page), changeAsset('BTCUSDT')])
        button2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        button3 = tk.Button(self, text="Quit", bg='#db5151', command=quit)
        button3.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)


# trying another page might fail
class Chart_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Back to Home Page
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, columnspan=2)

        #Changing Assets
        label = tk.Label(self, text="Assert Pair :", font=LARGE_FONT)
        label.grid(row=1, column=0, pady=10)


        default_text = tk.StringVar(self)

        dropdown = ttk.OptionMenu(self, default_text, options[0], *options, command=changeAsset)
        dropdown.grid(row=1, column=1, pady=10)

        default_text.set("BTCUSDT")

        #Placing Orders
        vol_label = tk.Label(self, text="Enter Volume: ")
        vol_label.grid(row=2, column=0, pady=10)

        vol_entry = tk.Entry(self)
        vol_entry.grid(row=2, column=1, pady=10)


        buyButton = tk.Button(self, text="Buy", bg='#74e391',
                              command=lambda: placeOrder("buy", asset[:3], int(vol_entry.get())))
        buyButton.grid(row=3, column=0, pady=10)

        sellButton = tk.Button(self, text="Sell", bg='#db5151',
                              command=lambda: placeOrder("sell", asset[:3], int(vol_entry.get())))
        sellButton.grid(row=3, column=1, pady=10)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)
        '''
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        '''

app = SeaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
