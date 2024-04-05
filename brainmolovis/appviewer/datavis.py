from tkinter import Button, Label, PhotoImage, Toplevel, Frame, font, LabelFrame, messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.simpledialog import askfloat, askstring
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
        file = asksaveasfile(parent=self, filetypes=[('PNG', '*.png')], defaultextension=[('PNG', '*.png')])
        
        self.fig.savefig(file.name, bbox_inches='tight', dpi=200)

    def set_size(self) -> None:
        height = askfloat(parent=self, title='Figure height (inches)', prompt='Input the figure height in inches')
        width = askfloat(parent=self, title='Figure width (inches)', prompt='Input the figure width in inches')

        if height == None or height <= 0 or width == None or width <= 0:
            messagebox.showinfo('Error', 'Please, inform a valid input!')
            return 

        ax = self.fig.get_axes()[0]

        self.fig.clear()
        self.canvas.draw()
        self.fig.add_subplot(ax)
        ax.text(0.5, 0.5, 'Select a visualization', horizontalalignment='center', verticalalignment='center')
        self.fig.set_size_inches(width, height)
        
        self.canvas.draw()

    def set_title(self) -> None:
        title = askstring(parent=self, title='Figure title', prompt='Input the figure title')

        ax = self.fig.get_axes()[0]
        self.fig.add_subplot(ax)
        ax.set_title(title)
        self.canvas.draw()

    def set_xaxis_title(self) -> None:
        xaxis = askstring(parent=self, title='X-axis title', prompt='Input the X-axis title')

        ax = self.fig.get_axes()[0]
        self.fig.add_subplot(ax)
        ax.set_xlabel(xaxis)
        self.canvas.draw()

    def set_yaxis_title(self) -> None:
        yaxis = askstring(parent=self, title='Y-axis title', prompt='Input the Y-axis title')

        ax = self.fig.get_axes()[0]
        self.fig.add_subplot(ax)
        ax.set_ylabel(yaxis)
        self.canvas.draw()

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
        self.savebutton.pack(side='right', padx=(0,10))

        self.setsize = Button(botframe, text='Set chart size', command=self.set_size)
        self.setsize.pack(side='right', padx=(0,10))

        self.settitle = Button(botframe, text='Set chart title', command=self.set_title)
        self.settitle.pack(side='right', padx=(0,10))

        self.setxaxis = Button(botframe, text='Set X-axis title', command=self.set_xaxis_title)
        self.setxaxis.pack(side='right', padx=(0,10))

        self.setyaxis = Button(botframe, text='Set Y-axis title', command=self.set_yaxis_title)
        self.setyaxis.pack(side='right', padx=(0,10))
        
        botframe.pack(fill='x', side='bottom', padx=10, pady=(0,10))
