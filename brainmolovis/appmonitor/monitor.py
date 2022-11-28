import socket
from threading import Thread
from time import strftime
from tkinter import Button, IntVar, StringVar, Label, PhotoImage, Toplevel, messagebox, Frame, font, Checkbutton, Radiobutton
from tkinter.ttk import Separator, Combobox
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from idlelib.tooltip import Hovertip

from brainmolovis.apputils.common import LIGHT_GREY, LIGHT_GREY
from brainmolovis.apputils.safelist import SafeList
from brainmolovis.appconfig.subject import InputSubjectWindow

class MonitoringWindow(Toplevel):

    def receive_socket_mindwave_data(self) -> None:
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
                self.quit()
                messagebox.showinfo('Something went wrong!', 'Please, restart the monitoring process!')

            output_row = ''
            while self.__read_mindwave_data:
                data = skt.recv(2048)
                if not data:
                    self.quit()
                    messagebox.showinfo('Something went wrong!', 'Please, restart the monitoring process!')

                else:
                    temp = data.decode('utf-8')
                    #file.write(temp)
                    if 'rawEeg' in temp:                    
                        try:
                            value = int(temp.split('rawEeg":')[1].split('}')[0])
                            self.__raw_eeg_data.append(value)

                            if self.__record_mindwave_data == True:
                                output_row += str(value) + ','
                        except Exception: self.__raw_eeg_data.append(0)
                            
                    if 'attention' in temp:
                        try: 
                            value = int(temp.split('attention":')[1].split(',')[0])
                            self.__attention_esense.append(value)

                            if self.__record_mindwave_data == True:
                                output_row += '\t' + str(value)
                        except Exception: self.__attention_esense.append(0)
                        
                    if 'meditation' in temp:    
                        try: 
                            value = int(temp.split('meditation":')[1].split('}')[0])
                            self.__meditation_esense.append(value)

                            if self.__record_mindwave_data == True:
                                output_row += '\t' + str(value)
                        except Exception: self.__meditation_esense.append(0)
                        
                    if 'blinkStrength' in temp:
                        try: self.__blink = int(temp.split('blinkStrength":')[1].split('}')[0])
                        except Exception: self.__blink = 0

                    if 'eegPower' in temp:
                        try: self.__eeg_power['delta'] = int(temp.split('delta":')[1].split(',')[0])
                        except Exception: self.__eeg_power['delta'] = 0

                        try: self.__eeg_power['theta'] = int(temp.split('theta":')[1].split(',')[0])
                        except Exception: self.__eeg_power['theta'] = 0
                        
                        try: self.__eeg_power['lowAlpha'] = int(temp.split('lowAlpha":')[1].split(',')[0])
                        except Exception: self.__eeg_power['lowAlpha'] = 0

                        try: self.__eeg_power['highAlpha'] = int(temp.split('highAlpha":')[1].split(',')[0])
                        except Exception: self.__eeg_power['highAlpha'] = 0

                        try: self.__eeg_power['lowBeta'] = int(temp.split('lowBeta":')[1].split(',')[0])
                        except Exception: self.__eeg_power['lowBeta'] = 0

                        try: self.__eeg_power['highBeta'] = int(temp.split('highBeta":')[1].split(',')[0])
                        except Exception: self.__eeg_power['highBeta'] = 0

                        try: self.__eeg_power['lowGamma'] = int(temp.split('lowGamma":')[1].split(',')[0])
                        except Exception: self.__eeg_power['lowGamma'] = 0

                        try: self.__eeg_power['highGamma'] = int(temp.split('highGamma":')[1].split('}')[0])
                        except Exception: self.__eeg_power['highGamma'] = 0

                        try:
                            if self.__gen_at_opt.get() == self.__gen_at_opts[0]: # ['Theta/highBeta','Theta/lowBeta']
                                value = round(int(temp.split('theta":')[1].split(',')[0])/int(temp.split('highBeta":')[1].split(',')[0]),2)
                                self.__attention_gen.append(value)
                            elif self.__gen_at_opt.get() == self.__gen_at_opts[1]:
                                value = round(int(temp.split('theta":')[1].split(',')[0])/int(temp.split('lowBeta":')[1].split(',')[0]),2)
                                self.__attention_gen.append(value)
                            
                            if self.__gen_med_opt.get() == self.__gen_med_opts[0]: # ['highAlpha','lowAlpha']
                                self.__meditation_gen.append(int(temp.split('highAlpha":')[1].split(',')[0]))
                            elif self.__gen_med_opt.get() == self.__gen_med_opts[1]:
                                self.__meditation_gen.append(int(temp.split('lowAlpha":')[1].split(',')[0]))

                        except Exception: self.__raw_eeg_data.append(0)

                        if self.__record_mindwave_data == True:
                            output_row += '\t' + str(self.__eeg_power['delta'])
                            output_row += '\t' + str(self.__eeg_power['theta'])
                            output_row += '\t' + str(self.__eeg_power['lowAlpha'])
                            output_row += '\t' + str(self.__eeg_power['highAlpha'])
                            output_row += '\t' + str(self.__eeg_power['lowBeta'])
                            output_row += '\t' + str(self.__eeg_power['highBeta'])
                            output_row += '\t' + str(self.__eeg_power['lowGamma'])
                            output_row += '\t' + str(self.__eeg_power['highGamma'])
                            output_row += '\n'

                            with open(self.__export_file, 'a') as file:
                                file.write(output_row)
                                output_row = ''

                    if 'poorSignalLevel' in temp:
                        try: self.__signal = int(temp.split('poorSignalLevel":')[1].split('}')[0].split(',')[0])
                        except Exception: self.__signal = 0
                        self.headset_quality_signal()

    def start_pause_monitoring(self) -> None:
        if self.__read_mindwave_data == True:
            self.__read_mindwave_data = False
            self.__start_pause_button.config(text='Start', image=self.START)
            self.__recordbutton.config(state='disabled')
            self.__resetbutton.config(state='active')
            self.__config_button.config(state='active')
            self.__check_show_average.config(state='active')
            self.__radio_esense_10.config(state='active')
            self.__radio_esense_30.config(state='active')
            self.__radio_esense_60.config(state='active')
            self.__radio_gen_50.config(state='active')
            self.__radio_gen_100.config(state='active')
            self.__radio_gen_200.config(state='active')
            self.__combo_gen_at.config(state='active')
            self.__combo_gen_med.config(state='active')
        else:
            self.__read_mindwave_data = True
            self.__start_pause_button.config(text='Pause', image=self.PAUSE)
            self.__recordbutton.config(state='active')
            self.__resetbutton.config(state='disabled')
            self.__config_button.config(state='disabled')
            self.__check_show_average.config(state='disabled')
            self.__radio_esense_10.config(state='disabled')
            self.__radio_esense_30.config(state='disabled')
            self.__radio_esense_60.config(state='disabled')
            self.__radio_gen_50.config(state='disabled')
            self.__radio_gen_100.config(state='disabled')
            self.__radio_gen_200.config(state='disabled')
            self.__combo_gen_at.config(state='disabled')
            self.__combo_gen_med.config(state='disabled')

            self.set_charts_states(True)
            
            self.__thread = Thread(target=self.receive_socket_mindwave_data)
            self.__thread.daemon = True
            self.__thread.start()

    def start_pause_recording(self):
        if self.__record_mindwave_data == True:
            self.__record_mindwave_data = False
            self.__recordbutton.config(image=self.RECORD)
            self.__start_pause_button.config(state='active')
        else:
            self.__export_file = self.__export_path + '\\' + self.__subjectid + '_' + strftime('%m-%d-%Y_%Hh%Mmin%Sseg') + '.tab'
            with open(self.__export_file, 'w') as file:
                header = 'rawEeg' + '\t'
                header += 'eSenseAT' + '\t'
                header += 'eSenseMED' + '\t'
                header += 'delta' + '\t'
                header += 'theta' + '\t'
                header += 'lowAlpha' + '\t'
                header += 'highAlpha' + '\t'
                header += 'lowBeta' + '\t'
                header += 'highBeta' + '\t'
                header += 'lowGamma' + '\t'
                header += 'highGamma' + '\n'
                file.write(header)

            self.__record_mindwave_data = True
            self.__recordbutton.config(image=self.STOP)
            self.__start_pause_button.config(state='disabled')

    def init_values(self) -> None:
        self.__raw_eeg_data = SafeList(100)
        self.__attention_esense = SafeList(self.__win_esense_range.get())
        self.__meditation_esense = SafeList(self.__win_esense_range.get())
        self.__attention_gen = SafeList(self.__win_gen_range.get())
        self.__meditation_gen = SafeList(self.__win_gen_range.get())
        self.__blink = 0
        self.__eeg_power = {'delta': 0, 'theta': 0, 'lowAlpha': 0, 'highAlpha': 0, 'lowBeta': 0, 'highBeta': 0, 'lowGamma': 0, 'highGamma': 0}

    def subjectid_config(self):
        inputsubject = InputSubjectWindow(self, self.__subjectid)
        self.wait_variable(inputsubject.get_inputed())
        
        if self.__subjectid != '':
            self.__subjectid = inputsubject.get_subjectid()
            self.__subjectid_label.config(text=self.__subjectid)
        else:
            self.__subjectid = inputsubject.get_subjectid()

    def reset_monitoring_data(self) -> None:
        if self.__read_mindwave_data == False:
            self.set_charts_states(False)
            self.init_values()

    def chart_axis_visible(self, ax, visible):
        ax.axes.xaxis.set_visible(visible)
        ax.axes.yaxis.set_visible(visible)

    def set_charts_states(self, visible):
        #self.ax_raw.axis('off')
        self.chart_axis_visible(self.ax_raw, visible)
        self.ax_raw.cla()
        self.chart_axis_visible(self.ax_eeg_power, visible)
        self.ax_eeg_power.cla()
        self.chart_axis_visible(self.ax_esense_at_line, visible)
        self.ax_esense_at_line.cla()
        self.chart_axis_visible(self.ax_esense_at_bar, visible)
        self.ax_esense_at_bar.cla()
        self.chart_axis_visible(self.ax_esense_med_line, visible)
        self.ax_esense_med_line.cla()
        self.chart_axis_visible(self.ax_esense_med_bar, visible)
        self.ax_esense_med_bar.cla()
        self.chart_axis_visible(self.ax_blink, visible)
        self.ax_blink.cla()
        self.chart_axis_visible(self.ax_esense_at_value, visible)
        self.ax_esense_at_value.cla()
        self.chart_axis_visible(self.ax_esense_med_value, visible)
        self.ax_esense_med_value.cla()
        self.chart_axis_visible(self.ax_gen_at_line, visible)
        self.ax_gen_at_line.cla()
        self.chart_axis_visible(self.ax_gen_med_line, visible)
        self.ax_gen_med_line.cla()

    def confirm_reset(self):
        #if self.__raw_eeg_data.length() > 0:
            #messagebox.showinfo('Important', 'The monitoring window has been reset.', parent=self)
        self.reset_monitoring_data()
    
    def clock_time(self) -> None:
        string = strftime('%H:%M:%S (%m/%d/%Y)')
        #string = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3] + strftime(' (%m/%d/%Y)')
        self.__clock.config(text=string)
        self.__clock.after(1, self.clock_time)

    def headset_quality_signal(self) -> None:
        if self.__signal < 50: self.__signallabel.config(image=self.CONN4)
        elif self.__signal < 100: self.__signallabel.config(image=self.CONN3)
        elif self.__signal < 150: self.__signallabel.config(image=self.CONN2)
        elif self.__signal < 200: self.__signallabel.config(image=self.CONN1)
        else: self.__signallabel.config(image=self.CONN0)

    def gen_at_opt_selected(self, *args):
        print(self.__gen_at_opt.get())
        self.confirm_reset()

    def gen_med_opt_selected(self, *args):
        print(self.__gen_med_opt.get())
        self.confirm_reset()

    def quit(self) -> None:
        self.destroy()

    def __init__(self, parent, exportpath) -> None:
        #self = Toplevel()
        super().__init__(parent)

        self.title('Brain Monitor')
        self.iconbitmap('./icon/favicon.ico')
        self.attributes('-fullscreen',True)
        #self.grab_set()
        
        self.__export_path = exportpath
        self.__read_mindwave_data = False
        self.__record_mindwave_data = False
        self.__show_average = IntVar()
        self.__show_gen_values = IntVar()
        
        self.__gen_at_opts = ['Theta/highBeta','Theta/lowBeta']
        self.__gen_at_opt = StringVar()
        self.__gen_at_opt.set(self.__gen_at_opts[0])
        
        self.__gen_med_opts = ['highAlpha','lowAlpha']
        self.__gen_med_opt = StringVar()
        self.__gen_med_opt.set(self.__gen_med_opts[0])

        self.__win_esense_range = IntVar()
        self.__win_esense_range.set(30)
        self.__win_gen_range = IntVar()
        self.__win_gen_range.set(100)
        self.__subjectid = ''
        self.subjectid_config()
        self.init_values()

        self.RECORD = PhotoImage(file = r"./imgs/record.png")
        self.STOP = PhotoImage(file = r"./imgs/stop.png")
        self.CONN0 = PhotoImage(file = r"./imgs/conn0.png")
        self.CONN1 = PhotoImage(file = r"./imgs/conn1.png")
        self.CONN2 = PhotoImage(file = r"./imgs/conn2.png")
        self.CONN3 = PhotoImage(file = r"./imgs/conn3.png")
        self.CONN4 = PhotoImage(file = r"./imgs/conn4.png")
        self.START = PhotoImage(file = r"./imgs/start.png")
        self.PAUSE = PhotoImage(file = r"./imgs/pause.png")
        self.CONFIG = PhotoImage(file = r"./imgs/config.png")
        self.USER = PhotoImage(file = r"./imgs/user_small.png")
        self.SCAN = PhotoImage(file = r"./imgs/scan.png")
        
        fig = Figure()
        fig.subplots_adjust(bottom=0.10, top=0.96, left=0.04, right=0.96, hspace=1, wspace=1)
        
        grid = fig.add_gridspec(7, 18)
        self.ax_raw = fig.add_subplot(grid[0:3,0:8])
        self.ax_eeg_power = fig.add_subplot(grid[3:,0:8])
        self.ax_esense_at_line = fig.add_subplot(grid[0:3,8:12])
        self.ax_esense_at_bar = fig.add_subplot(grid[0,13])
        self.ax_esense_med_line = fig.add_subplot(grid[3:6,8:12])
        self.ax_esense_med_bar = fig.add_subplot(grid[3,13])
        self.ax_blink = fig.add_subplot(grid[-1,8:12])
        self.ax_esense_at_value = fig.add_subplot(grid[0,12])
        self.ax_esense_med_value = fig.add_subplot(grid[3,12])
        self.ax_gen_at_line = fig.add_subplot(grid[0:3,-4:])
        self.ax_gen_med_line = fig.add_subplot(grid[3:6,-4:])
        self.set_charts_states(False)
        
        def animate(i):
            if self.__read_mindwave_data == False: 
                return

            if len(self.__raw_eeg_data.get()) > 0:
                self.ax_raw.cla()
                self.ax_raw.tick_params(labelsize=8)
                self.ax_raw.set_ylim(min(self.__raw_eeg_data.get()), max(self.__raw_eeg_data.get()))
                self.ax_raw.set_xlim(self.__raw_eeg_data.length()-len(self.__raw_eeg_data.get()), self.__raw_eeg_data.length())
                
                self.ax_raw.set_title('Raw EEG')
                self.ax_raw.plot(np.arange(self.__raw_eeg_data.length()-len(self.__raw_eeg_data.get()), self.__raw_eeg_data.length(), 1), 
                        self.__raw_eeg_data.get(), lw=1, color='black')
                self.ax_raw.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
                if self.__show_average.get() == 1:
                    self.ax_raw.axhline(np.mean(self.__raw_eeg_data.get()), color='black', lw=0.5)
            else:
                self.ax_raw.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense at
            if len(self.__attention_esense.get()) > 0:
                self.ax_esense_at_line.cla()
                self.ax_esense_at_line.tick_params(labelsize=8)
                self.ax_esense_at_line.set_ylim(0,101)
                self.ax_esense_at_line.set_xlim(self.__attention_esense.length()-len(self.__attention_esense.get()), self.__attention_esense.length())
                self.ax_esense_at_line.set_title('eSense Attention')
                self.ax_esense_at_line.plot(np.arange(self.__attention_esense.length()-len(self.__attention_esense.get()), self.__attention_esense.length(), 1), 
                        self.__attention_esense.get(), lw=2, color='red', label='Attention')
                self.ax_esense_at_line.yaxis.tick_right()
                if self.__show_average.get() == 1:
                    self.ax_esense_at_line.axhline(np.mean(self.__attention_esense.get()), color='black', lw=0.5)
            else:
                self.ax_esense_at_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense med
            if len(self.__meditation_esense.get()) > 0:
                self.ax_esense_med_line.cla()
                self.ax_esense_med_line.tick_params(labelsize=8)
                self.ax_esense_med_line.set_ylim(0,101)
                self.ax_esense_med_line.set_xlim(self.__meditation_esense.length()-len(self.__meditation_esense.get()), self.__meditation_esense.length())
                self.ax_esense_med_line.set_title('eSense Meditation')
                self.ax_esense_med_line.plot(np.arange(self.__meditation_esense.length()-len(self.__meditation_esense.get()), self.__meditation_esense.length(), 1), 
                        self.__meditation_esense.get(), lw=2, color='blue', label='Meditation')
                self.ax_esense_med_line.yaxis.tick_right()
                if self.__show_average.get() == 1:
                    self.ax_esense_med_line.axhline(np.mean(self.__meditation_esense.get()), color='black', lw=0.5)
            else:
                self.ax_esense_med_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # generated at
            if len(self.__attention_gen.get()) > 0:
                self.ax_gen_at_line.cla()
                self.ax_gen_at_line.tick_params(labelsize=8)
                self.ax_gen_at_line.set_xlim(self.__attention_gen.length()-len(self.__attention_gen.get()), self.__attention_gen.length())
                self.ax_gen_at_line.set_title('Generated Attention (theta/beta)')
                self.ax_gen_at_line.plot(np.arange(self.__attention_gen.length()-len(self.__attention_gen.get()), self.__attention_gen.length(), 1), 
                        self.__attention_gen.get(), lw=2, color='red', label='Attention')
                self.ax_gen_at_line.yaxis.tick_right()
                if self.__show_average.get() == 1:
                    self.ax_gen_at_line.axhline(np.mean(self.__attention_gen.get()), color='black', lw=0.5)
            else:
                self.ax_gen_at_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # generated med
            if len(self.__meditation_gen.get()) > 0:
                self.ax_gen_med_line.cla()
                self.ax_gen_med_line.tick_params(labelsize=8)
                self.ax_gen_med_line.set_xlim(self.__meditation_gen.length()-len(self.__meditation_gen.get()), self.__meditation_gen.length())
                self.ax_gen_med_line.set_title('Generated Meditation (alpha)')
                self.ax_gen_med_line.plot(np.arange(self.__meditation_gen.length()-len(self.__meditation_gen.get()), self.__meditation_gen.length(), 1), 
                        self.__meditation_gen.get(), lw=2, color='blue', label='Meditation')
                self.ax_gen_med_line.yaxis.tick_right()
                if self.__show_average.get() == 1:
                    self.ax_gen_med_line.axhline(np.mean(self.__meditation_gen.get()), color='black', lw=0.5)
            else:
                self.ax_gen_med_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # blink
            if len(self.__raw_eeg_data.get()) > 0:
                self.ax_blink.cla()
                self.ax_blink.set_ylim(0,3)
                self.ax_blink.set_xlim(0,3)
                self.ax_blink.axes.xaxis.set_visible(False)
                self.ax_blink.axes.yaxis.set_visible(False)
                self.ax_blink.set_title('Blink Detection')
                if self.__blink != 0:
                    circle = Circle((1.5,1.5), self.__blink/100, color='red')
                    self.ax_blink.add_patch(circle)
                    self.__blink = 0
            else:
                self.ax_blink.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # eeg power
            if len(self.__raw_eeg_data.get()) > 0:
                self.ax_eeg_power.cla()
                self.ax_eeg_power.tick_params(labelsize=8)
                self.ax_eeg_power.set_title('EEG Power')
                self.ax_eeg_power.bar(*zip(*self.__eeg_power.items()), color='black')
                self.ax_eeg_power.tick_params(rotation=30)
                self.ax_eeg_power.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
            else:
                self.ax_eeg_power.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense attention bar
            if len(self.__attention_esense.get()) > 0:
                self.ax_esense_at_bar.cla()
                self.ax_esense_at_bar.bar(*zip(*{'Attention': self.__attention_esense.get()[-1]}.items()), color='red', width=0.1)
                self.ax_esense_at_bar.set_ylim(0,100)
                self.ax_esense_at_bar.axes.xaxis.set_visible(False)
                self.ax_esense_at_bar.tick_params(labelsize=5)
                self.ax_esense_at_bar.yaxis.tick_right()
                self.ax_esense_at_bar.set_yticks([0,25,50,75,100])
                
            # esense meditation bar
            if len(self.__meditation_esense.get()) > 0:
                self.ax_esense_med_bar.cla()
                self.ax_esense_med_bar.bar(*zip(*{'Meditation': self.__meditation_esense.get()[-1]}.items()), color='blue', width=0.2)
                self.ax_esense_med_bar.set_ylim(0,100)
                self.ax_esense_med_bar.axes.xaxis.set_visible(False)
                self.ax_esense_med_bar.tick_params(labelsize=5)
                self.ax_esense_med_bar.yaxis.tick_right()
                self.ax_esense_med_bar.set_yticks([0,25,50,75,100])

            # attention value
            self.ax_esense_at_value.cla()
            self.ax_esense_at_value.axes.xaxis.set_visible(False)
            self.ax_esense_at_value.axes.yaxis.set_visible(False)
            self.ax_esense_at_value.spines['top'].set_visible(False)
            self.ax_esense_at_value.spines['right'].set_visible(False)
            self.ax_esense_at_value.spines['bottom'].set_visible(False)
            self.ax_esense_at_value.spines['left'].set_visible(False)
            if len(self.__attention_esense.get()) > 0:
                try: curr_at = self.__attention_esense.get()[-1]
                except Exception: curr_at = 0
                self.ax_esense_at_value.text(0, 0, curr_at, color='red', size=38)
                self.ax_esense_at_value.set_ylim(0,50)
                self.ax_esense_at_value.set_xlim(0,20)
            else:
                self.ax_esense_at_value.text(0, 0, '-', color='black', size=38)

            # meditation value
            self.ax_esense_med_value.cla()
            self.ax_esense_med_value.axes.xaxis.set_visible(False)
            self.ax_esense_med_value.axes.yaxis.set_visible(False)
            self.ax_esense_med_value.spines['top'].set_visible(False)
            self.ax_esense_med_value.spines['right'].set_visible(False)
            self.ax_esense_med_value.spines['bottom'].set_visible(False)
            self.ax_esense_med_value.spines['left'].set_visible(False)
            if len(self.__meditation_esense.get()) > 0:
                try: curr_med = self.__meditation_esense.get()[-1]
                except Exception: curr_med = 0
                self.ax_esense_med_value.text(0, 0, curr_med, color='blue', size=38)
                self.ax_esense_med_value.set_ylim(0,50)
                self.ax_esense_med_value.set_xlim(0,20)
            else:
                self.ax_esense_med_value.text(0, 0, '-', color='black', size=38)
        
        def handle_close():
            self.__read_mindwave_data = False
            self.destroy()

        # TOP FRAME
        topframe = Frame(self, padx=70, pady=20, bg='white')
        topframe.pack(fill='x', side='top')

        Label(topframe, text='Subject ID', bg='white', fg='black', font=("Arial", 12)).pack(side='left', padx=5)
        self.__subjectid_label = Label(topframe, text=self.__subjectid, bg='white', fg='black', font=("Arial", 20, font.BOLD))
        self.__subjectid_label.pack(side='left')
        Hovertip(self.__subjectid_label, 'Subject ID.')

        self.__clock = Label(topframe, bg='white', font=("Arial", 20))
        self.__clock.pack(side='right')
        self.clock_time()
        Hovertip(self.__clock, 'Current time (and date).')
        Label(topframe, text='Time (date)', bg='white', fg='black', font=("Arial", 12)).pack(side='right', padx=5)

        # MIDDLE FRAME
        midframe = Frame(self)
        midframe.pack(expand=True, fill='both')

        self.canvas = FigureCanvasTkAgg(fig, master=midframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='both')
        self.animation = FuncAnimation(fig, func=animate, interval=100)
        
        # BOTTOM FRAME
        botframe = Frame(self, padx=5, pady=5)
        botframe.pack(fill='x', side='bottom')

        self.__config_button = Button(botframe, text='Configure', image=self.USER, command=self.subjectid_config)
        self.__config_button.pack(side='left', padx=5)
        Hovertip(self.__subjectid_label, 'Set the Subject ID.')

        self.__start_pause_button = Button(botframe, text='Start', image=self.START, command=self.start_pause_monitoring)
        self.__start_pause_button.pack(side='left')
        Hovertip(self.__start_pause_button, 'Starts/pauses the monitoring.')

        self.__recordbutton = Button(botframe, text='Record', image=self.RECORD, command=self.start_pause_recording, state='disabled')
        self.__recordbutton.pack(side='left', padx=5)
        Hovertip(self.__recordbutton, 'Records the read data into a file.')

        self.__resetbutton = Button(botframe, text='Reset', command=self.reset_monitoring_data, state='disabled')
        self.__resetbutton.pack(side='left')
        Hovertip(self.__resetbutton, 'Resets the monitoring window by cleaning the charts.')
        
        self.__check_show_average = Checkbutton(botframe, text='Show average of values', variable=self.__show_average, onvalue=1, offvalue=0)
        self.__check_show_average.pack(side='left',padx=5)

        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        win_esense_range_frame = Frame(botframe)
        win_esense_range_frame.pack(side='left', padx=5)

        Label(win_esense_range_frame, text='eSense (AT & MED) X-range').pack(side='left')
        self.__radio_esense_10 = Radiobutton(win_esense_range_frame, text='10', variable=self.__win_esense_range, value=10, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_esense_10.pack(side='left')
        self.__radio_esense_30 = Radiobutton(win_esense_range_frame, text='30', variable=self.__win_esense_range, value=30, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_esense_30.pack(side='left')
        self.__radio_esense_60 = Radiobutton(win_esense_range_frame, text='60', variable=self.__win_esense_range, value=60, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_esense_60.pack(side='left')
        
        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        win_gen_range_frame = Frame(botframe)
        win_gen_range_frame.pack(side='left', padx=5)
        Label(win_gen_range_frame, text='Generated (AT & MED) X-range').pack(side='left')
        self.__radio_gen_50 = Radiobutton(win_gen_range_frame, text='50', variable=self.__win_gen_range, value=50, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_gen_50.pack(side='left')
        self.__radio_gen_100 = Radiobutton(win_gen_range_frame, text='100', variable=self.__win_gen_range, value=100, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_gen_100.pack(side='left')
        self.__radio_gen_200 = Radiobutton(win_gen_range_frame, text='200', variable=self.__win_gen_range, value=200, indicator=0, selectcolor=LIGHT_GREY, command=self.confirm_reset)
        self.__radio_gen_200.pack(side='left')

        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        win_gen_options = Frame(botframe)
        win_gen_options.pack(side='left', padx=5)
        Label(win_gen_options, text='Generated Attention').pack(side='left')
        self.__combo_gen_at = Combobox(win_gen_options, values=self.__gen_at_opts, textvariable=self.__gen_at_opt, state='readonly')
        self.__combo_gen_at.pack(side='left', padx=5)
        self.__gen_at_opt.trace('w',self.gen_at_opt_selected)
        Label(win_gen_options, text='Generated Meditation').pack(side='left')
        self.__combo_gen_med = Combobox(win_gen_options, values=self.__gen_med_opts, textvariable=self.__gen_med_opt, state='readonly')
        self.__combo_gen_med.pack(side='left', padx=5)
        self.__gen_med_opt.trace('w',self.gen_med_opt_selected)

        Button(botframe, text='Close', command=handle_close).pack(side='right')
        
        self.__signallabel = Label(botframe, image=self.CONN0)
        self.__signallabel.pack(side='right', padx=5)
        Hovertip(self.__signallabel, 'The current signal quality from the headset.')