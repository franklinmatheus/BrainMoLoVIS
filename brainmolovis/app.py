from datetime import datetime
import os
import socket
from tkinter import Button, Frame, IntVar, Label, LabelFrame, Menu, Tk, font, messagebox, Text
from tkinter.ttk import Notebook, Style
from tkinter.filedialog import askopenfilename

from brainmolovis.apputils.common import CONNECTED, DISCONNECTED, GREEN, RED, LIGHT_GREY, GREY
from brainmolovis.appmonitor.monitor import MonitoringWindow
from brainmolovis.appconfig.export import ConfigExportPathWindow, ConfigLoggerFilenameWindow, ConfigLoggerFileContentWindow
from brainmolovis.appviewer.datavis import VisualizationWindow
from brainmolovis.appconfig.config import load_config

class App(Tk):
        
    def monitoring_window(self) -> None:
        self.monitoringwindow = MonitoringWindow(self)
        self.monitoringwindow.grab_set()

    def visualization_window(self) -> None:
        if self.datafilename != '':
            self.visualizationwindow = VisualizationWindow(self, self.datafilename)
            self.visualizationwindow.grab_set()
        else:
            messagebox.showinfo('Error', 'Please, inform a valid file!')

    def logger_export_window(self) -> None:
        self.configexportpathwindow = ConfigExportPathWindow(self)
        self.configexportpathwindow.grab_set()

    def logger_filename_format(self) -> None:
        self.loggerfilenamewindow = ConfigLoggerFilenameWindow(self)
        self.loggerfilenamewindow.grab_set()

    def logger_data_file_format(self) -> None:
        self.loggerfilecontentwindow = ConfigLoggerFileContentWindow(self)
        self.loggerfilecontentwindow.grab_set()
    
    def select_data_file(self) -> None:
        self.datafilename = askopenfilename()
        self.datafilevis.configure(state='normal')
        self.datafilevis.delete(1.0, 'end')
        self.datafilevis.insert('end', self.datafilename)
        self.datafilevis.configure(state='disabled')

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
        self.label_last_check['text'] = 'Last check: ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if status == CONNECTED: self.label_headset_status.config(fg=GREEN)
        else: self.label_headset_status.config(fg=RED)
        
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

        self.title('[NeuroSky MindWave] Brain Monitor and Logger')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('720x480')
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

        self.config(menu=menu)

        # side frame
        self.sideframe = Frame(self, padx=10, pady=10, bg=LIGHT_GREY)
        self.sideframe.pack(expand=False, fill='both', side='left', anchor='w')

        Label(self.sideframe, text='Brain Monitor and Logger', bg=LIGHT_GREY, font=("Arial", 12, font.BOLD), border=0).pack(side='top', anchor='w')
        Label(self.sideframe, text='for NeuroSky MindWave', bg=LIGHT_GREY, fg=GREY, font=("Arial", 8), border=0).pack(side='top', anchor='w')

        framestatus = LabelFrame(self.sideframe, text='Headset connection status', bg=LIGHT_GREY, padx=5, pady=5)
        framestatus.pack(fill='x', side='bottom')

        Button(framestatus, text='Check connection', command=self.checkconnection).pack(side='bottom', anchor='w', pady=5)

        self.label_last_check = Label(framestatus, text='Last status check: n.a.', bg=LIGHT_GREY, fg=GREY, border=0, font=("Arial", 8))
        self.label_last_check.pack(side='bottom', anchor='w')

        self.label_headset_status = Label(framestatus, text=DISCONNECTED, bg=LIGHT_GREY, fg=RED, font=("Arial", 10, font.BOLD), border=0)
        self.label_headset_status.pack(side='bottom', anchor='w')

        # main frame
        self.mainframe = Frame(self)
        self.mainframe.pack(expand=True, fill='both', side='right')

        tabcontrol = Notebook(self.mainframe)
        tab1 = Frame(tabcontrol, padx=10, pady=10)
        tab2 = Frame(tabcontrol, padx=10, pady=10)
        tabcontrol.add(tab1, text='Monitoring')
        tabcontrol.add(tab2, text='Data visualization')
        tabcontrol.pack(expand=True, fill='both')
        
        ### tab1: monitor only
        monitorframe = LabelFrame(tab1, text='Monitoring information', padx=10, pady=10)
        monitorframe.pack(fill='x', side='top')
        Label(monitorframe, text='RawEeg').pack(side='top', anchor='w')
        Label(monitorframe, text='Eyes blink detection').pack(side='top', anchor='w')
        Label(monitorframe, text='eSense Meditation').pack(side='top', anchor='w')
        Label(monitorframe, text='eSense Attetion').pack(side='top', anchor='w')
        Label(monitorframe, text='EegPower').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- delta').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- theta').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- lowAlpha').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- highAlpha').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- lowBeta').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- highBeta').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- lowGamma').pack(side='top', anchor='w')
        Label(monitorframe, text='\t- highGamma').pack(side='top', anchor='w')
        
        Button(tab1, text='Start monitoring', command=self.monitoring_window).pack(side='top', anchor='w', pady=10)

        ### tab2: visualization
        visframe = LabelFrame(tab2, text='Data file', padx=10, pady=10)
        visframe.pack(fill='x', side='top')

        Label(visframe, text='Selected data file:').pack(anchor='w', side='top')
        self.datafilevis = Text(visframe, height=5)
        self.datafilevis.pack(side='top', anchor='center', expand=True, fill='x', pady=10)
        self.datafilevis.configure(state='disabled')
        Button(visframe, text='Choose file', command=self.select_data_file).pack(side='top', anchor='w')

        Button(tab2, text='Open visualization module', command=self.visualization_window).pack(side='top', anchor='w', pady=10)

        load_config()

if __name__ == '__main__':
    app = App()
    app.mainloop()