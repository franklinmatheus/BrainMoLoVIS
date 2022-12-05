from tkinter import Button, Label, PhotoImage, Toplevel, Frame, font, LabelFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.pyplot import clf
from pandas import read_csv, DataFrame
from seaborn import set_theme, lineplot, heatmap, regplot
from numpy import arange

from brainmolovis.appconfig.config import get_logger_file_sep
from brainmolovis.apputils.mindwavedata import *

# matriz de correlação entre bands
class VisualizationWindow(Toplevel):

    def quit(self) -> None:
        self.canvas.get_tk_widget().destroy()
        self.destroy()

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.title('Data Visualization')
        self.iconbitmap('./icon/favicon.ico')
        self.attributes('-fullscreen',True)
        
        mainframe = Frame(self)
        mainframe.pack(expand=True, fill='both', pady=10, padx=10)

        self.optionsframe = Frame(mainframe)
        self.optionsframe.pack(padx=(0,10), side='left', anchor='n')

        Label(self.optionsframe, text='Choose a vizualization to be displayed', font=("Arial", 12, font.BOLD)).pack(side='top', anchor='w')
        
        self.SHOWICON = PhotoImage(file = r"./imgs/show.png")

        singlevisframe = LabelFrame(self.optionsframe, text='Single Data Visualizations', padx=5, pady=5)
        singlevisframe.pack(fill='x', pady=5)

        chartframe = Frame(mainframe, background='white', highlightbackground='black', highlightthickness=1, padx=5, pady=5)
        chartframe.pack(expand=True, fill='both', side='right')

        self.fig = Figure()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a visualization', horizontalalignment='center', verticalalignment='center')
        
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

        set_theme()

        botframe = Frame(self)
        Button(botframe, text='Close', command=self.quit).pack(anchor='e')
        botframe.pack(fill='x', side='bottom', padx=10, pady=(0,10))


class SingleFileVisualizationWindow(VisualizationWindow):

    def load_dataframe(self) -> DataFrame:
        sep = get_logger_file_sep()

        return read_csv(self.datafile, sep=sep)

    def esense_attention_history_line(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap([self.df['esenseat']], cmap='Spectral_r', ax=ax, 
                    yticklabels=False, xticklabels=False,
                    cbar_kws=dict(use_gridspec=False, location="bottom", shrink=0.5))
        ax.set_title('eSense Attention Heatmap')
        ax.set_xlabel('Samples')

        self.canvas.draw()
    
    def esense_attention_history_heatmap(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(self.df['esenseat'], color='red', ax=ax)
        regplot(x=arange(0,len(self.df['esenseat']),1), y=self.df['esenseat'], fit_reg=True, ax=ax, color='black', scatter_kws=dict(alpha=0)) 
        
        ax.set_title('eSense Attention History')
        ax.set_ylabel('eSense Attention')
        ax.set_xlabel('Samples')

        self.canvas.draw()

    def power_bands_correlation(self) -> None:
        pass

    def __init__(self, parent, datafile) -> None:
        super().__init__(parent)

        self.datafile = datafile

        self.df = self.load_dataframe()

        singlevisframe = LabelFrame(self.optionsframe, text='Single Data Visualizations', padx=5, pady=5)
        singlevisframe.pack(fill='x', pady=5)

        # OP1
        op1frame = Frame(singlevisframe, pady=5)
        op1frame.pack(side='top', anchor='w')
        self.buttonop1 = Button(op1frame, image=self.SHOWICON, command=self.esense_attention_history_line)
        self.buttonop1.pack(side='left')
        Label(op1frame, text='eSense Attention Heatmap').pack(side='left')

        # OP2
        op2frame = Frame(singlevisframe, pady=5)
        op2frame.pack(side='top', anchor='w')
        self.buttonop2 = Button(op2frame, image=self.SHOWICON, command=self.esense_attention_history_heatmap)
        self.buttonop2.pack(side='left')
        Label(op2frame, text='eSense Attention History').pack(side='left')

        multiplevisframe = LabelFrame(self.optionsframe, text='Multiple Data Visualizations', padx=5, pady=5)
        multiplevisframe.pack(fill='x', pady=5)

        # OP3
        op3frame = Frame(multiplevisframe, pady=5)
        op3frame.pack(side='top', anchor='w')
        self.buttonop3 = Button(op3frame, image=self.SHOWICON, command=self.power_bands_correlation)
        self.buttonop3.pack(side='left')
        Label(op3frame, text='Power bands correlation').pack(side='left')


class MultipleFilesVisualizationWindow(VisualizationWindow):

    def load_dataframe(self) -> DataFrame:
        sep = get_logger_file_sep()

        return None

    def command(self) -> None:
        print('command')

    def __init__(self, parent, foldername) -> None:
        super().__init__(parent)

        self.foldername = foldername

        self.df = self.load_dataframe()

        singlevisframe = LabelFrame(self.optionsframe, text='Example Visualization Category', padx=5, pady=5)
        singlevisframe.pack(fill='x', pady=5)

        # OP1
        op1frame = Frame(singlevisframe, pady=5)
        op1frame.pack(side='top', anchor='w')
        self.buttonop1 = Button(op1frame, image=self.SHOWICON, command=self.command)
        self.buttonop1.pack(side='left')
        Label(op1frame, text='Example Visualization').pack(side='left')
