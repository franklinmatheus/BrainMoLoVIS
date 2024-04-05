from tkinter import Button, Label, PhotoImage, Toplevel, Frame, font, LabelFrame
from tkinter.filedialog import asksaveasfile
from tkinter.simpledialog import askfloat
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from seaborn import set_theme

from brainmolovis.apputils.mindwavedata import *

class VisualizationWindow(Toplevel):

    def create_singledatavis_opt(self, title, func) -> None:
        opframe = Frame(self.singledatavisframe, pady=5)
        opframe.pack(side='top', anchor='w')
        self.buttonop = Button(opframe, image=self.SHOWICON, command=func)
        self.buttonop.pack(side='left')
        Label(opframe, text=title).pack(side='left')

    def create_multipledatavis_opt(self, title, func) -> None:
        opframe = Frame(self.multipledatavisframe, pady=5)
        opframe.pack(side='top', anchor='w')
        self.buttonop = Button(opframe, image=self.SHOWICON, command=func)
        self.buttonop.pack(side='left')
        Label(opframe, text=title).pack(side='left')

    def save_figure(self) -> None:
        height = askfloat(parent=self, title='Figure height (inches)', prompt='Input the figure height in inches')
        width = askfloat(parent=self, title='Figure width (inches)', prompt='Input the figure width in inches')

        file = asksaveasfile(parent=self, filetypes=[('PNG', '*.png')], defaultextension=[('PNG', '*.png')])
        
        temp = self.fig
        temp.set_size_inches(width, height)
        temp.savefig(file.name, bbox_inches='tight', dpi=200)

    def handle_close(self) -> None:
        self.destroy()

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.iconbitmap('./icon/favicon.ico')
        #self.attributes('-fullscreen',True)
        self.state('zoomed')

        mainframe = Frame(self)
        mainframe.pack(expand=True, fill='both', pady=10, padx=10)

        self.optionsframe = Frame(mainframe)
        self.optionsframe.pack(padx=(0,10), side='left', anchor='n')

        Label(self.optionsframe, text='Choose a vizualization to be displayed', font=('Arial', 12, font.BOLD)).pack(side='top', anchor='w')
        
        self.SHOWICON = PhotoImage(file = r'./imgs/show.png')

        self.singledatavisframe = LabelFrame(self.optionsframe, text='Single Data Visualizations', padx=5, pady=5)
        self.singledatavisframe.pack(fill='x', pady=5)

        self.multipledatavisframe = LabelFrame(self.optionsframe, text='Multiple Data Visualizations', padx=5, pady=5)
        self.multipledatavisframe.pack(fill='x', pady=5)

        self.chartframe = Frame(mainframe, background='white', highlightbackground='black', highlightthickness=1, padx=5, pady=5)
        self.chartframe.pack(expand=True, fill='both', side='right')

        self.fig = Figure(tight_layout=True)
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a visualization', horizontalalignment='center', verticalalignment='center')
        
        #def on_key_press(event):
        #    key_press_handler(event, self.canvas, self.toolbar)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chartframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', anchor='center', expand=True)

        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.chartframe)
        #self.toolbar.config(background='white')
        #self.toolbar._message_label.config(background='white')
        #self.toolbar.update()
        #self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        #self.canvas.mpl_connect('key_press_event', on_key_press)

        set_theme()

        botframe = Frame(self)

        Button(botframe, text='Close', command=self.handle_close).pack(anchor='e', side='right')
        self.savebutton = Button(botframe, text='Save PNG', command=self.save_figure)
        self.savebutton.pack(side='right', padx=5)
        botframe.pack(fill='x', side='bottom', padx=10, pady=(0,10))
