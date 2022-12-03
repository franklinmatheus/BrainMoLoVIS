import socket
from threading import Thread
from time import strftime
from datetime import datetime
from tkinter import Button, IntVar, StringVar, Label, PhotoImage, Toplevel, messagebox, Frame, font, Checkbutton, Radiobutton
from tkinter.ttk import Separator, Combobox
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from idlelib.tooltip import Hovertip
from pandas import read_csv, DataFrame

from brainmolovis.apputils.common import LIGHT_GREY, LIGHT_GREY
from brainmolovis.apputils.safelist import SafeList
from brainmolovis.appconfig.subject import InputSubjectWindow
from brainmolovis.appconfig.config import get_logger_file_sep
from brainmolovis.apputils.mindwavedata import *

# matriz de correlação entre bands
class VisualizationWindow(Toplevel):

    def load_dataframe(self) -> DataFrame:
        sep = get_logger_file_sep()

        return read_csv(self.datafile, sep=sep)

    def esense_attention_history(self) -> None:
        self.ax.cla()
        self.ax.plot(self.df['esenseat'], color='red')
        self.canvas.draw()

    def esense_meditation_history(self) -> None:
        self.ax.cla()
        self.ax.plot(self.df['esensemed'], color='blue')
        self.canvas.draw()

    def power_bands_correlation(self) -> None:
        pass

    def quit(self) -> None:
        self.destroy()

    def __init__(self, parent, datafile) -> None:
        super().__init__(parent)

        self.title('Data Visualization')
        self.iconbitmap('./icon/favicon.ico')
        self.attributes('-fullscreen',True)
        self.datafile = datafile

        self.df = self.load_dataframe()
        
        mainframe = Frame(self)
        mainframe.pack(expand=True, fill='both', pady=10, padx=10)

        optionsframe = Frame(mainframe)
        optionsframe.pack(padx=(0,10), side='left', anchor='n')

        Label(optionsframe, text='Choose a vizualization to be displayed', font=("Arial", 12, font.BOLD)).pack(side='top', anchor='w')
        
        self.SHOWICON = PhotoImage(file = r"./imgs/show.png")

        # OP1
        op1frame = Frame(optionsframe, pady=5)
        op1frame.pack(side='top', anchor='w')
        self.buttonop1 = Button(op1frame, image=self.SHOWICON, command=self.esense_attention_history)
        self.buttonop1.pack(side='left')
        Label(op1frame, text='eSense Attention History').pack(side='left')

        # OP2
        op2frame = Frame(optionsframe, pady=5)
        op2frame.pack(side='top', anchor='w')
        self.buttonop2 = Button(op2frame, image=self.SHOWICON, command=self.esense_meditation_history)
        self.buttonop2.pack(side='left')
        Label(op2frame, text='eSense Meditation History').pack(side='left')

        # OP3
        op3frame = Frame(optionsframe, pady=5)
        op3frame.pack(side='top', anchor='w')
        self.buttonop3 = Button(op3frame, image=self.SHOWICON, command=self.power_bands_correlation)
        self.buttonop3.pack(side='left')
        Label(op3frame, text='Power bands correlation').pack(side='left')

        chartframe = Frame(mainframe, background='white', highlightbackground='black', highlightthickness=1, padx=5, pady=5)
        chartframe.pack(expand=True, fill='both', side='right')

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.text(0.5, 0.5, 'Select a visualization', horizontalalignment='center', verticalalignment='center')
        
        def on_key_press(event):
            key_press_handler(event, self.canvas, self.toolbar)

        self.canvas = FigureCanvasTkAgg(self.fig, master=chartframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, chartframe)
        self.toolbar.config(background='white')
        self.toolbar._message_label.config(background='white')
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        self.canvas.mpl_connect("key_press_event", on_key_press)

        botframe = Frame(self)
        Button(botframe, text='Close', command=self.quit).pack(anchor='e')
        botframe.pack(fill='x', side='bottom', padx=10, pady=(0,10))