from datetime import datetime
import os
import socket
from tkinter import Button, Frame, IntVar, Label, LabelFrame, Menu, Tk, font, messagebox
from tkinter.ttk import Notebook, Style

from brainmolovis.apputils.common import CONNECTED, DISCONNECTED, GREEN, RED, LIGHT_GREY, GREY
from brainmolovis.appmonitor.monitor import MonitoringWindow
from brainmolovis.appconfig.export import ConfigExportPathWindow, ConfigLoggerFilenameWindow, ConfigLoggerFileContentWindow
from brainmolovis.appconfig.config import load_config

class App(Tk):
        
    def monitoring_window(self) -> None:
        self.monitoringwindow = MonitoringWindow(self)
        self.monitoringwindow.grab_set()

    def logger_export_window(self) -> None:
        self.configexportpathwindow = ConfigExportPathWindow(self)
        self.configexportpathwindow.grab_set()

    def logger_filename_format(self) -> None:
        self.loggerfilenamewindow = ConfigLoggerFilenameWindow(self)
        self.loggerfilenamewindow.grab_set()

    def logger_data_file_format(self) -> None:
        self.loggerfilecontentwindow = ConfigLoggerFileContentWindow(self)
        self.loggerfilecontentwindow.grab_set()
    
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

        # menu
        menu = Menu(self)
        filemenu = Menu(menu, tearoff=0)
        #filemenu.add_command(label='Record history', command=self.command)
        #filemenu.add_separator()
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

        #tabcontrol.tab(1, state='disabled')
        
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

        ### tab2: frame form
        ###### this approach/tab (tab2) is temporarily unavailable
        #frameform = LabelFrame(tab2, text='Session metadata', padx=10, pady=10)
        #frameform.pack(fill='x', side='top', anchor='n')
        #frameform.columnconfigure(index=1, weight=1)

        #Label(frameform, text='User ID').grid(row=0, column=0, padx=10, sticky='e')
        #Label(frameform, text='User age').grid(row=1, column=0, padx=10, sticky='e')
        #Label(frameform, text='User genre').grid(row=2, column=0, padx=10, sticky='e')
        #Label(frameform, text='BCI Experience?').grid(row=3, column=0, padx=10, sticky='e')
        #Label(frameform, text='Session date').grid(row=4, column=0, padx=10, sticky='e')
        #Label(frameform, text='Export directory').grid(row=5, column=0, padx=10, sticky='e')
        
        #self.userid = Entry(frameform).grid(row=0, column=1, columnspan=3, sticky='news', pady=5)
        #self.userage = Entry(frameform).grid(row=1, column=1, columnspan=3, sticky='news', pady=5)
        #Radiobutton(frameform, text="Male", padx=5, variable=self.usergenre, value=1).grid(row=2, column=1, pady=5, sticky='w')
        #Radiobutton(frameform, text="Famale", padx=5, variable=self.usergenre, value=2).grid(row=2, column=2, pady=5, sticky='w')
        
        #Radiobutton(frameform, text="No", padx=5, variable=self.experience, value=1).grid(row=3, column=1, pady=5, sticky='w')
        #Radiobutton(frameform, text="Yes", padx=5, variable=self.experience, value=2).grid(row=3, column=2, pady=5, sticky='w')
        #self.sessiondate = DateEntry(frameform, bg=GREEN, fg='white', state='readonly').grid(row=4, column=1, columnspan=3, sticky='news', pady=5)
        #Label(frameform, wraplength=320, text=self.exportpath).grid(row=5, column=1, columnspan=3, sticky='w', pady=5)

        #Button(frameform, text='Start new session', command=self.registersession).grid(row=6, column=2)

        #self.mainloop()

        load_config()

if __name__ == '__main__':
    app = App()
    app.mainloop()