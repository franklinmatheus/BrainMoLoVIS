from datetime import datetime
from os.path import basename
import socket
from tkinter import Button, Frame, IntVar, Label, LabelFrame, Menu, Tk, font, messagebox, PhotoImage
from tkinter.ttk import Style
from tkinter.filedialog import askopenfilename, askdirectory

from brainmolovis.apputils.common import CONNECTED, DISCONNECTED, GREEN, RED, LIGHT_GREY, GREY, DARK_GREY, BLUE1
from brainmolovis.appmonitor.monitor import MonitoringWindow
from brainmolovis.appconfig.export import ConfigExportPathWindow, ConfigLoggerFilenameWindow, ConfigLoggerFileContentWindow
from brainmolovis.appviewer.datavis import SingleFileVisualizationWindow, MultipleFilesVisualizationWindow
from brainmolovis.appconfig.config import load_config

class App(Tk):
        
    def monitoring_window(self) -> None:
        self.monitoringwindow = MonitoringWindow(self)
        self.monitoringwindow.grab_set()

    def visualization_single_window(self) -> None:
        if self.datafilename != '':
            self.visualizationwindow = SingleFileVisualizationWindow(self, self.datafilename)
            self.visualizationwindow.grab_set()
        else:
            messagebox.showinfo('Error', 'Please, inform a valid file!')

    def visualization_multiple_window(self) -> None:
        if self.foldername != '':
            self.visualizationwindow = MultipleFilesVisualizationWindow(self, self.foldername)
            self.visualizationwindow.grab_set()
        else:
            messagebox.showinfo('Error', 'Please, inform a valid directory!')

    def logger_export_window(self) -> None:
        self.configexportpathwindow = ConfigExportPathWindow(self)
        self.configexportpathwindow.grab_set()

    def logger_filename_format(self) -> None:
        self.loggerfilenamewindow = ConfigLoggerFilenameWindow(self)
        self.loggerfilenamewindow.grab_set()

    def logger_data_file_format(self) -> None:
        self.loggerfilecontentwindow = ConfigLoggerFileContentWindow(self)
        self.loggerfilecontentwindow.grab_set()
    
    def select_datafile_vis(self) -> None:
        self.datafilename = askopenfilename()
        self.datafilevis.config(text=basename(self.datafilename))

    def select_folder_vis(self) -> None:
        self.foldername = askdirectory()
        self.foldervis.config(text='.../' + basename(self.foldername))

    def registersession(self) -> None:
        if self.label_headset_status['text'] == DISCONNECTED:
            messagebox.showinfo('Headset disconnected', 'Please, check your headset connection!')
        else:
            print('connected')
            pass

    def quit(self) -> None:
        self.destroy()

    def command(self) -> None:
        print('command')

    def changestatusconnection(self, status) -> None:
        self.label_headset_status['text'] = status
        self.label_last_check['text'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if status == CONNECTED: self.label_headset_status.config(bg=GREEN)
        else: self.label_headset_status.config(bg=RED)
        
    def checkconnection(self) -> None:
        host = '127.0.0.1'
        port = 13854
        param = '{"enableRawOutput": false, "format": "Json"}'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            try:
                skt.connect((host, port))
                skt.sendall(str.encode(param))
                data = skt.recv(2048)
                print(data)
                if data: self.changestatusconnection(CONNECTED)
                else: self.changestatusconnection(DISCONNECTED)
            except socket.error:
                print('connection error')
                self.changestatusconnection(DISCONNECTED)

    def __init__(self) -> None:
        # build GUI
        super().__init__()

        #self.title('[NeuroSky MindWave] Brain Monitor and Logger')
        self.title('BMLVIS')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('780x520')
        self.resizable(False, False)

        self.defaultFont = font.nametofont('TkDefaultFont')
        self.defaultFont.configure(family="Arial", size=10)
        
        s= Style()
        s.theme_use('default')

        self.userid = None
        self.userage = None
        self.usergenre = IntVar()
        self.experience = IntVar()
        self.sessiondate = None
        self.datafilename = ''
        self.foldername = ''

        self.CSV = PhotoImage(file = r"./imgs/csv.png")
        self.FOLDER = PhotoImage(file = r"./imgs/folder.png")

        # menu
        menu = Menu(self)
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label='Exit', command=self.quit)
        menu.add_cascade(label='File', menu=filemenu)

        options = Menu(menu, tearoff=0)
        options.add_command(label='Logger export directory', command=self.logger_export_window)
        options.add_command(label='Logger filename format', command=self.logger_filename_format)
        options.add_command(label='Logger data file format', command=self.logger_data_file_format)

        menu.add_cascade(label='Options', menu=options)

        help = Menu(menu, tearoff=0)
        help.add_command(label='About', command=self.command)
        help.add_command(label='Help', command=self.command)
        menu.add_cascade(label='Help', menu=help)

        self.config(menu=menu, bg=BLUE1)

        # side frame
        self.sideframe = Frame(self, padx=10, pady=10, bg=BLUE1)
        self.sideframe.pack(expand=False, fill='both', side='left', anchor='w', padx=(0, 50))

        Label(self.sideframe, text='BrainMoLoVIS', bg=BLUE1, fg='white', font=("Arial", 12, font.BOLD), border=0).pack(side='top', anchor='w')
        Label(self.sideframe, text='for NeuroSky MindWave', bg=BLUE1, fg=GREY, font=("Arial", 8), border=0).pack(side='top', anchor='w')

        framestatus = Frame(self.sideframe, bg=BLUE1)
        framestatus.pack(fill='x', side='bottom')

        Label(framestatus, text='Headset status', bg=BLUE1, fg=LIGHT_GREY, padx=0, font=("Arial", 10, font.BOLD)).pack(side='top', anchor='w', pady=(0,5))
        
        self.label_headset_status = Label(framestatus, text=DISCONNECTED, bg=RED, fg='white', font=("Arial", 10, font.BOLD), border=0, padx=4, pady=2)
        self.label_headset_status.pack(side='top', anchor='w')
        Label(framestatus, text='Last status check:', bg=BLUE1, fg=GREY, border=0, font=("Arial", 8)).pack(side='top', anchor='w')
        self.label_last_check = Label(framestatus, text='n.a.', bg=BLUE1, fg=LIGHT_GREY, border=0, font=("Arial", 8))
        self.label_last_check.pack(side='top', anchor='w')
        Button(framestatus, text='Check connection', command=self.checkconnection).pack(side='top', anchor='w', pady=(5,0))

        # main frame
        mainframe = Frame(self, bg=LIGHT_GREY)
        mainframe.pack(expand=True, fill='both', side='right')

        ## monitor/logger module
        monitorframe = Frame(mainframe, padx=10, pady=10)
        monitorframe.pack(fill='x', side='top', padx=10, pady=10)

        Label(monitorframe, text='Monitor and Logger Module', font=("Arial", 12, font.BOLD)).pack(anchor='w', side='top', pady=(0,10))
        monitorframegrid = Frame(monitorframe)
        monitorframegrid.pack(fill='x', side='top')
        monitorframegrid.columnconfigure(0, weight=1)
        Label(monitorframegrid, text='Mindwave Monitoring Dashboard', font=("Arial", 10, font.BOLD), fg=DARK_GREY).grid(row=0, column=0, sticky='w')
        Button(monitorframegrid, text='Open', command=self.monitoring_window).grid(row=0, column=1)

        ## vizualition module options
        visframe = Frame(mainframe, padx=10, pady=10)
        visframe.pack(fill='x', side='top', padx=10, pady=10)

        Label(visframe, text='Visualization Module', font=("Arial", 12, font.BOLD)).pack(anchor='w', side='top', pady=(0,10))

        visframegrid = Frame(visframe)
        visframegrid.pack(fill='x', side='top')
        visframegrid.columnconfigure(1, weight=1)
        
        ### single file
        Label(visframegrid, text='Single Datafile', fg=DARK_GREY, font=("Arial", 10, font.BOLD)).grid(row=0, column=0, padx=(0,10), sticky='w')
        self.datafilevis = Label(visframegrid, font=("Arial", 8), text='Select a file...', background=LIGHT_GREY)
        self.datafilevis.grid(row=0, column=1, sticky='ew', padx=(0,10), pady=(0,5))
        Button(visframegrid, text='Choose file', image=self.CSV, command=self.select_datafile_vis).grid(row=0, column=2, padx=(0,10), pady=(0,5))
        Button(visframegrid, text='Open', command=self.visualization_single_window).grid(row=0, column=3, pady=(0,5))

        ### multiple files, i.e. folder
        Label(visframegrid, text='Multiple Datafiles', fg=DARK_GREY, font=("Arial", 10, font.BOLD)).grid(row=1, column=0, padx=(0,10), sticky='w')
        self.foldervis = Label(visframegrid, font=("Arial", 8), text='Select a folder...', background=LIGHT_GREY)
        self.foldervis.grid(row=1, column=1, sticky='ew', padx=(0,10))
        Button(visframegrid, text='Choose file', image=self.FOLDER, command=self.select_folder_vis).grid(row=1, column=2, padx=(0,10))
        Button(visframegrid, text='Open', command=self.visualization_multiple_window).grid(row=1, column=3)

        load_config()

if __name__ == '__main__':
    app = App()
    app.mainloop()