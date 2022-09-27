from datetime import datetime
import os
import socket
from threading import Thread
import time
from tkinter import Button, Entry, Frame, IntVar, Label, LabelFrame, Menu, Radiobutton, Scrollbar, Text, Tk, Toplevel, font, messagebox
from tkinter.filedialog import askdirectory
from tkcalendar import DateEntry
from tkinter.ttk import Notebook, Style
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from common import CONNECTED, DISCONNECTED, GREEN, LIGHT_GREY, RED,  LIGHT_GREY, GREY

class App():

    def reading_data(self) -> None:
        host = '127.0.0.1'
        port = 13854
        param = '{"enableRawOutput": true, "format": "Json"}'
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            try: skt.connect((host, port))
            except socket.error: 
                print('connection error')
                return
                
            skt.sendall(str.encode(param))
            try:
                print(skt.recv(2048).decode('utf-8'))
            except UnicodeDecodeError:
                messagebox.showinfo('Something went wrong!', 'Please, restart the monitoring process!')

            while self.__keep_reading:
                data = skt.recv(2048)
                if not data: 
                    print('no data')
                    break

                else:
                    with open('output_mindwave.txt', 'a') as file:
                        temp = data.decode('utf-8')
                        file.write(temp)
                        if 'rawEeg' in temp:
                            try: 
                                self.__raw_eeg_data.append(int(temp.split('rawEeg":')[1].split('}')[0]))
                                self.__xmax_raw += 1
                            except ValueError: self.__raw_eeg_data.append(0)
                            
                            if len(self.__raw_eeg_data) > 100: 
                                self.__raw_eeg_data.pop(0)
                                if self.__xmax_raw - self.__xmin_raw > 100: self.__xmin_raw += 1
                        
                        if 'attention' in temp:
                            try: 
                                self.__attention.append(int(temp.split('attention":')[1].split(',')[0]))
                                self.__xmax_at += 1
                            except ValueError: self.__attention.append(0)
                            
                            if len(self.__attention) > 25:
                                self.__attention.pop(0)
                                if self.__xmax_at - self.__xmin_at > 25: self.__xmin_at += 1
                                
                        if 'meditation' in temp:    
                            try: 
                                self.__meditation.append(int(temp.split('meditation":')[1].split('}')[0]))
                                self.__xmax_med += 1
                            except ValueError: self.__meditation.append(0)

                            if len(self.__meditation) > 25:
                                self.__meditation.pop(0)
                                if self.__xmax_med - self.__xmin_med > 25: self.__xmin_med += 1

                        if 'blinkStrength' in temp:
                            try: 
                                self.__blink = int(temp.split('blinkStrength":')[1].split('}')[0])
                            except ValueError: self.__blink = 0

                        if 'eegPower' in temp:
                            try: self.__eeg_power['delta'] = int(temp.split('delta":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['delta'] = 0

                            try: self.__eeg_power['theta'] = int(temp.split('theta":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['theta'] = 0
                            
                            try: self.__eeg_power['lowAlpha'] = int(temp.split('lowAlpha":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['lowAlpha'] = 0

                            try: self.__eeg_power['highAlpha'] = int(temp.split('highAlpha":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['highAlpha'] = 0

                            try: self.__eeg_power['lowBeta'] = int(temp.split('lowBeta":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['lowBeta'] = 0

                            try: self.__eeg_power['highBeta'] = int(temp.split('highBeta":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['highBeta'] = 0

                            try: self.__eeg_power['lowGamma'] = int(temp.split('lowGamma":')[1].split(',')[0])
                            except ValueError: self.__eeg_power['lowGamma'] = 0

                            try: self.__eeg_power['highGamma'] = int(temp.split('highGamma":')[1].split('}')[0])
                            except ValueError: self.__eeg_power['highGamma'] = 0

    
    def monitoring_window(self) -> None:
        window = Toplevel(padx=10)
        window.title('Brain Monitor')
        window.iconbitmap('./icon/favicon.ico')
        window.attributes('-fullscreen',True)
        window.grab_set()

        self.__raw_eeg_data = []
        self.__attention = []
        self.__meditation = []
        self.__eeg_power = {'delta': 0, 'theta': 0, 'lowAlpha': 0, 'highAlpha': 0, 'lowBeta': 0, 'highBeta': 0, 'lowGamma': 0, 'highGamma': 0}
        power_sequence = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
        self.__blink = 0
        self.__xmin_raw = 0
        self.__xmax_raw = 0
        self.__xmin_med = 0
        self.__xmax_med = 0
        self.__xmin_at = 0
        self.__xmax_at = 0
        self.__keep_reading = True

        fig = Figure()
        ax1 = fig.add_subplot(221) # raw
        ax2 = fig.add_subplot(347) # attention esense line
        ax3 = fig.add_subplot(343) # blink
        ax4 = fig.add_subplot(348) # meditation esense line
        ax5 = fig.add_subplot(3, 4, 11) # attention esense bar
        ax6 = fig.add_subplot(3, 4, 12) # meditation esense bar
        ax7 = fig.add_subplot(344) # numeric values
        ax8 = fig.add_subplot(223) # eeg power

        ax1.set_ylim(0,100)
        ax1.set_xlim(0,100)
        line_raweeg, = ax1.plot(0, 0, lw=1)

        ax2.set_ylim(0,100)
        ax2.set_xlim(0,20)
        line_atesense, = ax2.plot(0, 0, lw=2, color='red', label='Attention')

        ax4.set_ylim(0,100)
        ax4.set_xlim(0,20)
        line_medesense, = ax4.plot(0, 0, lw=2, color='blue', label='Meditation')
        
        def animate(i):
            if len(self.__raw_eeg_data) > 0:
                ax1.set_ylim(min(self.__raw_eeg_data), max(self.__raw_eeg_data))
            if self.__xmin_raw != self.__xmax_raw:
                ax1.set_xlim(self.__xmin_raw, self.__xmax_raw)

            ax1.set_title('Raw EEG')
            line_raweeg.set_ydata(self.__raw_eeg_data)
            line_raweeg.set_xdata(np.arange(self.__xmax_raw-len(self.__raw_eeg_data), self.__xmax_raw, 1))

            # esense at
            if self.__xmin_at != self.__xmax_at:
                ax2.set_xlim(self.__xmin_at, self.__xmax_at)
            ax2.set_title('eSense Attention')
            #line_atesense.set_ydata(self.__attention)
            #line_atesense.set_xdata(np.arange(self.__xmax_at-len(self.__attention), self.__xmax_at, 1))

            # esense med
            if self.__xmin_med != self.__xmax_med:
                ax4.set_xlim(self.  __xmin_med, self.__xmax_med)
            ax4.set_title('eSense Meditation')
            #line_medesense.set_ydata(self.__meditation)
            #line_medesense.set_xdata(np.arange(self.__xmax_med-len(self.__meditation), self.__xmax_med, 1))
            
            # blink
            ax3.cla()
            ax3.set_ylim(0,3)
            ax3.set_xlim(0,3)
            ax3.axes.xaxis.set_visible(False)
            ax3.axes.yaxis.set_visible(False)
            ax3.set_title('Blink Detection')
            if self.__blink != 0:
                circle = Circle((1.5,1.5), self.__blink/100, color='red')
                ax3.add_patch(circle)
                self.__blink = 0

            # eeg power
            ax8.cla()
            ax8.bar(*zip(*self.__eeg_power.items()))
            ax8.tick_params(rotation=45)

            # esense attention bar
            ax5.cla()
            if len(self.__attention) > 0:
                ax5.bar(*zip(*{'Attention': self.__attention[-1]}.items()))
                ax5.set_ylim(0,100)

            # esense meditation bar
            ax6.cla()
            if len(self.__meditation) > 0:
                ax6.bar(*zip(*{'Meditation': self.__meditation[-1]}.items()))
                ax6.set_ylim(0,100)

            # numeric values
            ax7.cla()
            ax7.axes.xaxis.set_visible(False)
            ax7.axes.yaxis.set_visible(False)
            ax7.spines['top'].set_visible(False)
            ax7.spines['right'].set_visible(False)
            ax7.spines['bottom'].set_visible(False)
            ax7.spines['left'].set_visible(False)
            ax7.text(0, 0, 'Meditation', color='blue')
            
            try: curr_med = self.__meditation[-1]
            except Exception: curr_med = 0
            ax7.text(0, 8, curr_med, color='blue', size=44)
            ax7.text(0, 30, 'Attention', color='red')
            
            try: curr_at = self.__attention[-1]
            except Exception: curr_at = 0
            ax7.text(0, 38, curr_at, color='red', size=44)
            ax7.text(10, 4, 'delta: ' + str(self.__eeg_power['delta']), size=11)
            ax7.text(10, 10, 'theta: ' + str(self.__eeg_power['theta']), size=11)
            ax7.text(10, 16, 'lowAlpha: ' + str(self.__eeg_power['lowAlpha']), size=11)
            ax7.text(10, 22, 'highAlpha: ' + str(self.__eeg_power['highAlpha']), size=11)
            ax7.text(10, 28, 'lowBeta: ' + str(self.__eeg_power['lowBeta']), size=11)
            ax7.text(10, 34, 'highBeta: ' + str(self.__eeg_power['highBeta']), size=11)
            ax7.text(10, 40, 'lowGamma: ' + str(self.__eeg_power['lowGamma']), size=11)
            ax7.text(10, 46, 'highGamma: ' + str(self.__eeg_power['highGamma']), size=11)

            ax7.set_ylim(0,50)
            ax7.set_xlim(0,20)
        
        thread = Thread(target=self.reading_data)
        thread.daemon = True
        thread.start()

        def handle_close():
            self.__keep_reading = False
            window.destroy()

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        animation = FuncAnimation(fig, func=animate, interval=100)
        #plt.tight_layout()
        #window.protocol('WN_DELETE_WINDOW', handle_close)
        Button(window, text='Close', command=handle_close).pack(side='bottom', anchor='center', pady=10)
        
        window.mainloop()

    def select_path(self) -> None:
        new_path = askdirectory()
        if new_path == '': return

        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to change the export directory?\nNew export directory: ' + new_path)
        if answer:
            self.exportpath = new_path
            self.pathfield.configure(state='normal')
            self.pathfield.delete(1.0, 'end')
            self.pathfield.insert('end', new_path)

            print(self.pathfield)

    def export_data_window(self) -> None:
        window = Toplevel(padx=10)
        window.title('Export data options')
        window.iconbitmap('./icon/favicon.ico')
        window.geometry('420x280')
        window.grab_set()
        window.resizable(False, False)

        Button(window, text='Change export directory', command=self.select_path).pack(anchor='e', side='bottom', pady=10)
        Label(window, text='Current export directory:').pack(anchor='w', side='top', pady=10)
        self.pathfield = Text(window)
        self.pathfield.pack(side='top', anchor='center', expand=True, fill='x')
        self.pathfield.insert('end', self.exportpath)
        self.pathfield.configure(state='disabled')
    
    def registersession(self) -> None:
        if self.label_headset_status['text'] == DISCONNECTED:
            messagebox.showinfo('Headset disconnected', 'Please, check your headset connection!')
        else:
            print('connected')
            pass

    def quit(self) -> None:
        self.root.destroy()

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
                if data:
                    self.changestatusconnection(CONNECTED)
                else:
                    self.changestatusconnection(DISCONNECTED)
            except socket.error:
                print('connection error')
                self.changestatusconnection(DISCONNECTED)

    def __init__(self) -> None:
        # build GUI
        self.root = Tk()
        self.root.title('[NeuroSky MindWave] Brain Monitor and Logger')
        self.root.iconbitmap('./icon/favicon.ico')
        self.root.geometry('720x480')
        self.root.resizable(False, False)

        self.defaultFont = font.nametofont('TkDefaultFont')
        self.defaultFont.configure(family="Arial", size=10)
        
        s= Style()
        s.theme_use('default')

        self.userid = None
        self.userage = None
        self.usergenre = IntVar()
        self.experience = IntVar()
        self.sessiondate = None
        self.exportpath = os.getcwd()

        # menu
        menu = Menu(self.root)
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label='Record history', command=self.command)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)
        menu.add_cascade(label='File', menu=filemenu)

        options = Menu(menu, tearoff=0)
        options.add_command(label='Export data options', command=self.export_data_window)
        menu.add_cascade(label='Options', menu=options)

        help = Menu(menu, tearoff=0)
        help.add_command(label='About', command=self.command)
        help.add_command(label='Help', command=self.command)
        menu.add_cascade(label='Help', menu=help)

        self.root.config(menu=menu)

        # side frame
        self.sideframe = Frame(self.root, padx=10, pady=10, bg=LIGHT_GREY)
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
        self.mainframe = Frame(self.root)
        self.mainframe.pack(expand=True, fill='both', side='right')

        tabcontrol = Notebook(self.mainframe)
        tab1 = Frame(tabcontrol, padx=10, pady=10)
        tab2 = Frame(tabcontrol, padx=10, pady=10)
        tabcontrol.add(tab1, text='Register new session')
        tabcontrol.add(tab2, text='Monitor only')
        tabcontrol.pack(expand=True, fill='both')
        
        ### tab1: frame form
        frameform = LabelFrame(tab1, text='Session metadata', padx=10, pady=10)
        frameform.pack(fill='x', side='top', anchor='n')
        frameform.columnconfigure(index=1, weight=1)

        Label(frameform, text='User ID').grid(row=0, column=0, padx=10, sticky='e')
        Label(frameform, text='User age').grid(row=1, column=0, padx=10, sticky='e')
        Label(frameform, text='User genre').grid(row=2, column=0, padx=10, sticky='e')
        Label(frameform, text='BCI Experience?').grid(row=3, column=0, padx=10, sticky='e')
        Label(frameform, text='Session date').grid(row=4, column=0, padx=10, sticky='e')
        Label(frameform, text='Export directory').grid(row=5, column=0, padx=10, sticky='e')
        
        self.userid = Entry(frameform).grid(row=0, column=1, columnspan=3, sticky='news', pady=5)
        self.userage = Entry(frameform).grid(row=1, column=1, columnspan=3, sticky='news', pady=5)
        Radiobutton(frameform, text="Male", padx=5, variable=self.usergenre, value=1).grid(row=2, column=1, pady=5, sticky='w')
        Radiobutton(frameform, text="Famale", padx=5, variable=self.usergenre, value=2).grid(row=2, column=2, pady=5, sticky='w')
        
        Radiobutton(frameform, text="No", padx=5, variable=self.experience, value=1).grid(row=3, column=1, pady=5, sticky='w')
        Radiobutton(frameform, text="Yes", padx=5, variable=self.experience, value=2).grid(row=3, column=2, pady=5, sticky='w')
        self.sessiondate = DateEntry(frameform, bg=GREEN, fg='white', state='readonly').grid(row=4, column=1, columnspan=3, sticky='news', pady=5)
        Label(frameform, wraplength=320, text=self.exportpath).grid(row=5, column=1, columnspan=3, sticky='w', pady=5)

        Button(frameform, text='Start new session', command=self.registersession).grid(row=6, column=2)

        ### tab2: monitor only
        monitorframe = LabelFrame(tab2, text='Monitoring information', padx=10, pady=10)
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
        
        Button(tab2, text='Start monitoring', command=self.monitoring_window).pack(side='top', anchor='w', pady=10)

        self.root.mainloop()

if __name__ == '__main__':
    app = App()