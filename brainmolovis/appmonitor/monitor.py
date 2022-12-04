import socket
from threading import Thread
from time import strftime, sleep
from datetime import datetime
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
from brainmolovis.appconfig.config import get_export_path, get_logger_filename, get_logger_file_content_reduced
from brainmolovis.apputils.mindwavedata import *

development = True

class MonitoringWindow(Toplevel):
    # adicionar dados do jeito que chegam numa pilha e botar uma thread paralela para processar e mostrar no monitor
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
            try: print(skt.recv(4096).decode('utf-8'))
            except UnicodeDecodeError:
                messagebox.showinfo('Something went wrong!', 'Please, restart the monitoring process!', parent=self)
                self.destroy()

            while self.read_mindwave_data:
                data = skt.recv(4096)
                if not data:
                    messagebox.showinfo('Something went wrong!', 'Please, restart the monitoring process!', parent=self)
                    self.destroy()

                else:
                    packet = data.decode('utf-8')

                    if self.record_mindwave_data:
                        with open(self.export_file_temp_log, 'a') as file:
                            file.write(packet)

                    if 'rawEeg' in packet: self.raw_eeg_data.append(get_raweeg(packet))
                            
                    if 'attention' in packet: 
                        if self.show_esenseat.get() == 1: self.attention_esense.append(get_attention(packet))

                    if 'meditation' in packet:    
                        if self.show_esensemed.get() == 1: self.meditation_esense.append(get_meditation(packet))

                    if 'blinkStrength' in packet: self.blink = get_blink_strength(packet)

                    if 'eegPower' in packet:
                        self.eeg_power['delta'] = get_delta(packet)
                        self.eeg_power['theta'] = get_theta(packet)
                        self.eeg_power['lowAlpha'] = get_low_alpha(packet)
                        self.eeg_power['highAlpha'] = get_high_alpha(packet)
                        self.eeg_power['lowBeta'] = get_low_beta(packet)
                        self.eeg_power['highBeta'] = get_high_beta(packet)
                        self.eeg_power['lowGamma'] = get_low_gamma(packet)
                        self.eeg_power['highGamma'] = get_high_gamma(packet)

                        try:
                            if self.gen_at_opt.get() == self.gen_at_opts[0]: # ['Theta/highBeta','Theta/lowBeta','None']
                                value = round(get_theta(packet)/get_high_beta(packet),2)
                                self.attention_gen.append(value)
                            elif self.gen_at_opt.get() == self.gen_at_opts[1]:
                                value = round(get_theta(packet)/get_low_beta(packet),2)
                                self.attention_gen.append(value)
                            elif self.gen_at_opt.get() == self.gen_at_opts[2]:
                                pass
                            
                            if self.gen_med_opt.get() == self.gen_med_opts[0]: # ['highAlpha','lowAlpha','None]
                                self.meditation_gen.append(get_high_alpha(packet))
                            elif self.gen_med_opt.get() == self.gen_med_opts[1]:
                                self.meditation_gen.append(get_low_alpha(packet))
                            elif self.gen_med_opt.get() == self.gen_med_opts[2]:
                                pass

                        except Exception: self.raw_eeg_data.append(0)

                    if 'poorSignalLevel' in packet:
                        self.signal = get_signal_level(packet)
                        self.headset_quality_signal()

    def stream_from_file(self) -> None:        
        with open('streamdata.csv', 'r') as file:
            while self.read_mindwave_data:
                data = file.readline()
                
                if not data: self.destroy()
                else:
                    packet = data

                    if self.record_mindwave_data:
                        with open(self.export_file_temp_log, 'a') as file:
                            file.write(packet)

                    if 'rawEeg' in packet: self.raw_eeg_data.append(get_raweeg(packet))
                            
                    if 'attention' in packet: 
                        if self.show_esenseat.get() == 1: self.attention_esense.append(get_attention(packet))

                    if 'meditation' in packet:    
                        if self.show_esensemed.get() == 1: self.meditation_esense.append(get_meditation(packet))

                    if 'blinkStrength' in packet: self.blink = get_blink_strength(packet)

                    if 'eegPower' in packet:
                        self.eeg_power['delta'] = get_delta(packet)
                        self.eeg_power['theta'] = get_theta(packet)
                        self.eeg_power['lowAlpha'] = get_low_alpha(packet)
                        self.eeg_power['highAlpha'] = get_high_alpha(packet)
                        self.eeg_power['lowBeta'] = get_low_beta(packet)
                        self.eeg_power['highBeta'] = get_high_beta(packet)
                        self.eeg_power['lowGamma'] = get_low_gamma(packet)
                        self.eeg_power['highGamma'] = get_high_gamma(packet)

                        try:
                            if self.gen_at_opt.get() == self.gen_at_opts[0]: # ['Theta/highBeta','Theta/lowBeta','None']
                                value = round(get_theta(packet)/get_high_beta(packet),2)
                                self.attention_gen.append(value)
                            elif self.gen_at_opt.get() == self.gen_at_opts[1]:
                                value = round(get_theta(packet)/get_low_beta(packet),2)
                                self.attention_gen.append(value)
                            elif self.gen_at_opt.get() == self.gen_at_opts[2]:
                                pass
                            
                            if self.gen_med_opt.get() == self.gen_med_opts[0]: # ['highAlpha','lowAlpha','None]
                                self.meditation_gen.append(get_high_alpha(packet))
                            elif self.gen_med_opt.get() == self.gen_med_opts[1]:
                                self.meditation_gen.append(get_low_alpha(packet))
                            elif self.gen_med_opt.get() == self.gen_med_opts[2]:
                                pass

                        except Exception: self.raw_eeg_data.append(0)

                    if 'poorSignalLevel' in packet:
                        self.signal = get_signal_level(packet)
                        self.headset_quality_signal()
                    
                sleep(0.0000000000001)

    def start_pause_monitoring(self) -> None:
        if self.read_mindwave_data == True:
            self.read_mindwave_data = False
            self.start_pause_button.config(text='Start', image=self.START)
            self.recordbutton.config(state='disabled')
            self.resetbutton.config(state='active')
            self.config_button.config(state='active')
            self.check_show_average.config(state='active')
            self.combo_win_range.config(state='active')
            self.combo_gen_at.config(state='active')
            self.combo_gen_med.config(state='active')
        else:
            self.read_mindwave_data = True
            self.start_pause_button.config(text='Pause', image=self.PAUSE)
            self.recordbutton.config(state='active')
            self.resetbutton.config(state='disabled')
            self.config_button.config(state='disabled')
            self.check_show_average.config(state='disabled')
            self.combo_win_range.config(state='disabled')
            self.combo_gen_at.config(state='disabled')
            self.combo_gen_med.config(state='disabled')

            self.set_charts_states(True)
            
            if development:
                thread = Thread(target=self.stream_from_file)
                thread.daemon = True
                thread.start()
            else:
                thread = Thread(target=self.receive_socket_mindwave_data)
                thread.daemon = True
                thread.start()

    def start_pause_recording(self):
        if self.record_mindwave_data == True:
            self.record_mindwave_data = False
            self.recordbutton.config(image=self.RECORD)
            self.start_pause_button.config(state='active')

            with open(self.export_file_temp_log, 'r') as filein:
                output_row = ['']*len(self.file_format_seq)
                for line in filein:
                    
                    if 'rawEeg' in line and 'raweeg' in self.file_format_seq:
                            output_row[self.file_format['raweeg']] = output_row[self.file_format['raweeg']] + str(get_raweeg(line)) + ','
                            continue
                            
                    if 'attention' in line and 'esenseat' in self.file_format_seq:
                            output_row[self.file_format['esenseat']] = str(get_attention(line))
                        
                    if 'meditation' in line and 'esensemed' in self.file_format_seq:
                            output_row[self.file_format['esensemed']] = str(get_meditation(line))
                        
                    if 'eegPower' in line:

                        value = 0
                        if self.gen_at_opt.get() == self.gen_at_opts[0]: # ['Theta/highBeta','Theta/lowBeta','None']
                            value = round(get_theta(line)/get_high_beta(line),2)
                        elif self.gen_at_opt.get() == self.gen_at_opts[1]:
                            value = round(get_theta(line)/get_low_beta(line),2)
                        output_row[self.file_format['genat']] = str(value)
                        
                        value = 0
                        if self.gen_med_opt.get() == self.gen_med_opts[0]: # ['highAlpha','lowAlpha','None]
                            value = get_high_alpha(line)
                        elif self.gen_med_opt.get() == self.gen_med_opts[1]:
                            value = get_low_alpha(line)
                        output_row[self.file_format['genmed']] = str(value)

                        if 'delta' in self.file_format_seq: output_row[self.file_format['delta']] = str(get_delta(line))
                        if 'theta' in self.file_format_seq: output_row[self.file_format['theta']] = str(get_theta(line))
                        if 'lowalpha' in self.file_format_seq: output_row[self.file_format['lowalpha']] = str(get_low_alpha(line))
                        if 'highalpha' in self.file_format_seq: output_row[self.file_format['highalpha']] = str(get_high_alpha(line))
                        if 'lowbeta' in self.file_format_seq: output_row[self.file_format['lowbeta']] = str(get_low_beta(line))
                        if 'highbeta' in self.file_format_seq: output_row[self.file_format['highbeta']] = str(get_high_beta(line))
                        if 'lowgamma' in self.file_format_seq: output_row[self.file_format['lowgamma']] = str(get_low_gamma(line))
                        if 'highgamma' in self.file_format_seq: output_row[self.file_format['highgamma']] = str(get_high_gamma(line))

                        with open(self.export_file, 'a') as fileout:
                            fileout.write(str(self.sep).join(output_row) + '\n')
                            output_row = ['']*len(self.file_format_seq)
                            
        else:
            filename_tokens = []
            for key, value in get_logger_filename().items():
                if value != -1:
                    if key == 'subject': filename_tokens.append(self.subjectid)
                    elif key == 'date': filename_tokens.append(strftime('%m-%d-%Y'))
                    elif key == 'time': filename_tokens.append(strftime('%Hh%Mmin%Sseg'))
            self.export_file = self.export_path + '\\' + '_'.join(filename_tokens) + '.csv'
            self.export_file_temp_log = self.export_path + '\\' + 'temp_log_' + '_'.join(filename_tokens) + '.csv'

            with open(self.export_file, 'w') as file:
                output = str(self.sep).join(self.file_format_seq) + '\n'
                output = output.replace('genat','genat_' + self.gen_at_opt.get())
                output = output.replace('genmed','genmed_' + self.gen_med_opt.get())
                file.write(output)

            with open(self.export_file_temp_log, 'w') as file: pass

            self.record_mindwave_data = True
            self.recordbutton.config(image=self.STOP)
            self.start_pause_button.config(state='disabled')

    def init_values(self) -> None:
        self.raw_eeg_data = SafeList(100)
        self.attention_esense = SafeList(self.win_range.get())
        self.meditation_esense = SafeList(self.win_range.get())
        self.attention_gen = SafeList(self.win_range.get())
        self.meditation_gen = SafeList(self.win_range.get())
        self.blink = 0
        self.eeg_power = {'delta': 0, 'theta': 0, 'lowAlpha': 0, 'highAlpha': 0, 'lowBeta': 0, 'highBeta': 0, 'lowGamma': 0, 'highGamma': 0}

    def subjectid_config(self):
        inputsubject = InputSubjectWindow(self, self.subjectid)
        self.wait_variable(inputsubject.get_inputed())
        
        if self.subjectid != '':
            self.subjectid = inputsubject.get_subjectid()
            self.subjectid_label.config(text=self.subjectid)
        else:
            self.subjectid = inputsubject.get_subjectid()

    def reset_monitoring_data(self) -> None:
        if self.read_mindwave_data == False:
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
        #if self.raw_eeg_data.length() > 0:
        messagebox.showinfo('Important', 'The monitoring window has been reset.', parent=self)
        self.reset_monitoring_data()
    
    def clock_time(self) -> None:
        string = strftime('%H:%M:%S (%m/%d/%Y)')
        #string = datetime.utcnow().strftime('%H:%M:%S.%f')[:-5] + strftime(' (%m/%d/%Y)')
        self.clock.config(text=string)
        self.clock.after(1, self.clock_time)

    def headset_quality_signal(self) -> None:
        if self.signal < 50: self.signallabel.config(image=self.CONN4)
        elif self.signal < 100: self.signallabel.config(image=self.CONN3)
        elif self.signal < 150: self.signallabel.config(image=self.CONN2)
        elif self.signal < 200: self.signallabel.config(image=self.CONN1)
        else: self.signallabel.config(image=self.CONN0)

    def win_range_opt_selected(self, *args):
        self.confirm_reset()
    
    def gen_at_opt_selected(self, *args):
        self.confirm_reset()

    def gen_med_opt_selected(self, *args):
        self.confirm_reset()

    def show_esense_at_selected(self, *args):
        self.confirm_reset()

    def show_esense_med_selected(self, *args):
        self.confirm_reset()

    def quit(self) -> None:
        self.destroy()

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.title('Brain Monitor')
        self.iconbitmap('./icon/favicon.ico')
        self.attributes('-fullscreen',True)
        
        self.export_path = get_export_path()
        self.file_format_seq, self.file_format, self.sep = get_logger_file_content_reduced()
        
        self.read_mindwave_data = False
        self.record_mindwave_data = False
        self.signal = 0
        self.show_average = IntVar()
        self.show_esenseat = IntVar()
        self.show_esenseat.set(1)
        self.show_esensemed = IntVar()
        self.show_esensemed.set(1)
        
        self.gen_at_opts = ['Theta/highBeta','Theta/lowBeta','None']
        self.gen_at_opt = StringVar()
        self.gen_at_opt.set(self.gen_at_opts[0])
        
        self.gen_med_opts = ['highAlpha','lowAlpha','None']
        self.gen_med_opt = StringVar()
        self.gen_med_opt.set(self.gen_med_opts[0])

        self.win_range_opts = [10,30,60]
        self.win_range = IntVar()
        self.win_range.set(30)
        self.subjectid = ''
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
            if self.read_mindwave_data == False: 
                return

            if len(self.raw_eeg_data.get()) > 0:
                self.ax_raw.cla()
                self.ax_raw.tick_params(labelsize=8)
                self.ax_raw.set_ylim(min(self.raw_eeg_data.get()), max(self.raw_eeg_data.get()))
                self.ax_raw.set_xlim(self.raw_eeg_data.length()-len(self.raw_eeg_data.get()), self.raw_eeg_data.length())
                
                self.ax_raw.set_title('Raw EEG')
                self.ax_raw.plot(np.arange(self.raw_eeg_data.length()-len(self.raw_eeg_data.get()), self.raw_eeg_data.length(), 1), 
                        self.raw_eeg_data.get(), lw=1, color='black')
                self.ax_raw.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
                if self.show_average.get() == 1:
                    self.ax_raw.axhline(np.mean(self.raw_eeg_data.get()), color='black', lw=0.5)
            else:
                self.ax_raw.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense at
            if self.show_esenseat.get() == 0:
                self.ax_esense_at_line.text(0.5, 0.5, 'Disabled', color='gray', horizontalalignment='center', verticalalignment='center')
                self.chart_axis_visible(self.ax_esense_at_line, False)
            else:
                if len(self.attention_esense.get()) > 0:
                    self.ax_esense_at_line.cla()
                    self.ax_esense_at_line.tick_params(labelsize=8)
                    self.ax_esense_at_line.set_ylim(0,101)
                    self.ax_esense_at_line.set_xlim(self.attention_esense.length()-len(self.attention_esense.get()), self.attention_esense.length())
                    self.ax_esense_at_line.set_title('eSense Attention')
                    self.ax_esense_at_line.plot(np.arange(self.attention_esense.length()-len(self.attention_esense.get()), self.attention_esense.length(), 1), 
                            self.attention_esense.get(), lw=2, color='red', label='Attention')
                    self.ax_esense_at_line.yaxis.tick_right()
                    if self.show_average.get() == 1:
                        self.ax_esense_at_line.axhline(np.mean(self.attention_esense.get()), color='black', lw=0.5)
                else:
                    self.ax_esense_at_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense med
            if self.show_esensemed.get() == 0:
                self.ax_esense_med_line.text(0.5, 0.5, 'Disabled', color='gray', horizontalalignment='center', verticalalignment='center')
                self.chart_axis_visible(self.ax_esense_med_line, False)
            else:
                if len(self.meditation_esense.get()) > 0:
                    self.ax_esense_med_line.cla()
                    self.ax_esense_med_line.tick_params(labelsize=8)
                    self.ax_esense_med_line.set_ylim(0,101)
                    self.ax_esense_med_line.set_xlim(self.meditation_esense.length()-len(self.meditation_esense.get()), self.meditation_esense.length())
                    self.ax_esense_med_line.set_title('eSense Meditation')
                    self.ax_esense_med_line.plot(np.arange(self.meditation_esense.length()-len(self.meditation_esense.get()), self.meditation_esense.length(), 1), 
                            self.meditation_esense.get(), lw=2, color='blue', label='Meditation')
                    self.ax_esense_med_line.yaxis.tick_right()
                    if self.show_average.get() == 1:
                        self.ax_esense_med_line.axhline(np.mean(self.meditation_esense.get()), color='black', lw=0.5)
                else:
                    self.ax_esense_med_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # generated at
            if self.gen_at_opt.get() == self.gen_at_opts[2]:
                self.ax_gen_at_line.text(0.5, 0.5, 'Disabled', color='gray', horizontalalignment='center', verticalalignment='center')
                self.chart_axis_visible(self.ax_gen_at_line, False)
            else:
                if len(self.attention_gen.get()) > 0:
                    self.ax_gen_at_line.cla()
                    self.ax_gen_at_line.tick_params(labelsize=8)
                    self.ax_gen_at_line.set_xlim(self.attention_gen.length()-len(self.attention_gen.get()), self.attention_gen.length())
                    self.ax_gen_at_line.set_title('Generated Attention (' + self.gen_at_opt.get() + ')')
                    self.ax_gen_at_line.plot(np.arange(self.attention_gen.length()-len(self.attention_gen.get()), self.attention_gen.length(), 1), 
                            self.attention_gen.get(), lw=2, color='red', label='Attention')
                    self.ax_gen_at_line.yaxis.tick_right()
                    if self.show_average.get() == 1:
                        self.ax_gen_at_line.axhline(np.mean(self.attention_gen.get()), color='black', lw=0.5)
                else:
                    self.ax_gen_at_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # generated med
            if self.gen_med_opt.get() == self.gen_med_opts[2]:
                self.ax_gen_med_line.text(0.5, 0.5, 'Disabled', color='gray', horizontalalignment='center', verticalalignment='center')
                self.chart_axis_visible(self.ax_gen_med_line, False)
            else:
                if len(self.meditation_gen.get()) > 0:
                    self.ax_gen_med_line.cla()
                    self.ax_gen_med_line.tick_params(labelsize=8)
                    self.ax_gen_med_line.set_xlim(self.meditation_gen.length()-len(self.meditation_gen.get()), self.meditation_gen.length())
                    self.ax_gen_med_line.set_title('Generated Meditation (' + self.gen_med_opt.get() + ')')
                    self.ax_gen_med_line.plot(np.arange(self.meditation_gen.length()-len(self.meditation_gen.get()), self.meditation_gen.length(), 1), 
                            self.meditation_gen.get(), lw=2, color='blue', label='Meditation')
                    self.ax_gen_med_line.yaxis.tick_right()
                    if self.show_average.get() == 1:
                        self.ax_gen_med_line.axhline(np.mean(self.meditation_gen.get()), color='black', lw=0.5)
                else:
                    self.ax_gen_med_line.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # blink
            if len(self.raw_eeg_data.get()) > 0:
                self.ax_blink.cla()
                self.ax_blink.set_ylim(0,3)
                self.ax_blink.set_xlim(0,3)
                self.ax_blink.axes.xaxis.set_visible(False)
                self.ax_blink.axes.yaxis.set_visible(False)
                self.ax_blink.set_title('Blink Detection')
                if self.blink != 0:
                    circle = Circle((1.5,1.5), self.blink/100, color='red')
                    self.ax_blink.add_patch(circle)
                    self.blink = 0
            else:
                self.ax_blink.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # eeg power
            if len(self.raw_eeg_data.get()) > 0:
                self.ax_eeg_power.cla()
                self.ax_eeg_power.tick_params(labelsize=8)
                self.ax_eeg_power.set_title('EEG Power')
                self.ax_eeg_power.bar(*zip(*self.eeg_power.items()), color='black')
                self.ax_eeg_power.tick_params(rotation=30)
                self.ax_eeg_power.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
            else:
                self.ax_eeg_power.text(0.5, 0.5, 'Unavailable data', horizontalalignment='center', verticalalignment='center')

            # esense attention bar
            if len(self.attention_esense.get()) > 0:
                self.ax_esense_at_bar.cla()
                self.ax_esense_at_bar.bar(*zip(*{'Attention': self.attention_esense.get()[-1]}.items()), color='red', width=0.1)
                self.ax_esense_at_bar.set_ylim(0,100)
                self.ax_esense_at_bar.axes.xaxis.set_visible(False)
                self.ax_esense_at_bar.tick_params(labelsize=5)
                self.ax_esense_at_bar.yaxis.tick_right()
                self.ax_esense_at_bar.set_yticks([0,25,50,75,100])
                
            # esense meditation bar
            if len(self.meditation_esense.get()) > 0:
                self.ax_esense_med_bar.cla()
                self.ax_esense_med_bar.bar(*zip(*{'Meditation': self.meditation_esense.get()[-1]}.items()), color='blue', width=0.2)
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
            if len(self.attention_esense.get()) > 0:
                try: curr_at = self.attention_esense.get()[-1]
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
            if len(self.meditation_esense.get()) > 0:
                try: curr_med = self.meditation_esense.get()[-1]
                except Exception: curr_med = 0
                self.ax_esense_med_value.text(0, 0, curr_med, color='blue', size=38)
                self.ax_esense_med_value.set_ylim(0,50)
                self.ax_esense_med_value.set_xlim(0,20)
            else:
                self.ax_esense_med_value.text(0, 0, '-', color='black', size=38)
        
        def handle_close():
            self.read_mindwave_data = False
            self.destroy()

        # TOP FRAME
        topframe = Frame(self, padx=70, pady=20, bg='white')
        topframe.pack(fill='x', side='top')

        Label(topframe, text='Subject ID', bg='white', fg='black', font=("Arial", 12)).pack(side='left', padx=5)
        self.subjectid_label = Label(topframe, text=self.subjectid, bg='white', fg='black', font=("Arial", 20, font.BOLD))
        self.subjectid_label.pack(side='left')
        Hovertip(self.subjectid_label, 'Subject ID.')

        self.clock = Label(topframe, bg='white', font=("Arial", 20))
        self.clock.pack(side='right')
        self.clock_time()

        #thread_clock = Thread(target=self.clock_time)
        #thread_clock.daemon = True
        #thread_clock.start()

        Hovertip(self.clock, 'Current time (and date).')
        Label(topframe, text='Time (date)', bg='white', fg='black', font=("Arial", 12)).pack(side='right', padx=5)

        # MIDDLE FRAME
        midframe = Frame(self)
        midframe.pack(expand=True, fill='both')

        self.canvas = FigureCanvasTkAgg(fig, master=midframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill='both')
        self.animation = FuncAnimation(fig, func=animate, interval=250)
        
        # BOTTOM FRAME
        botframe = Frame(self, padx=5, pady=5)
        botframe.pack(fill='x', side='bottom')

        self.config_button = Button(botframe, text='Configure', image=self.USER, command=self.subjectid_config)
        self.config_button.pack(side='left', padx=5)
        Hovertip(self.subjectid_label, 'Set the Subject ID.')

        self.start_pause_button = Button(botframe, text='Start', image=self.START, command=self.start_pause_monitoring)
        self.start_pause_button.pack(side='left')
        Hovertip(self.start_pause_button, 'Starts/pauses the monitoring.')

        self.recordbutton = Button(botframe, text='Record', image=self.RECORD, command=self.start_pause_recording, state='disabled')
        self.recordbutton.pack(side='left', padx=5)
        Hovertip(self.recordbutton, 'Records the read data into a file.')

        self.resetbutton = Button(botframe, text='Reset', command=self.reset_monitoring_data, state='disabled')
        self.resetbutton.pack(side='left')
        Hovertip(self.resetbutton, 'Resets the monitoring window by cleaning the charts.')
        
        self.check_show_average = Checkbutton(botframe, text='Show average of values', variable=self.show_average, onvalue=1, offvalue=0)
        self.check_show_average.pack(side='left',padx=5)

        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        win_range_frame = Frame(botframe)
        win_range_frame.pack(side='left', padx=5)

        Label(win_range_frame, text='Attention and Meditation X-range').pack(side='left')
        self.combo_win_range = Combobox(win_range_frame, values=self.win_range_opts, textvariable=self.win_range, state='readonly')
        self.combo_win_range.pack(side='left', padx=5)
        self.win_range.trace('w',self.win_range_opt_selected)

        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        win_gen_options = Frame(botframe)
        win_gen_options.pack(side='left', padx=5)
        Label(win_gen_options, text='Generated Attention').pack(side='left')
        self.combo_gen_at = Combobox(win_gen_options, values=self.gen_at_opts, textvariable=self.gen_at_opt, state='readonly')
        self.combo_gen_at.pack(side='left', padx=5)
        self.gen_at_opt.trace('w',self.gen_at_opt_selected)
        Label(win_gen_options, text='Generated Meditation').pack(side='left')
        self.combo_gen_med = Combobox(win_gen_options, values=self.gen_med_opts, textvariable=self.gen_med_opt, state='readonly')
        self.combo_gen_med.pack(side='left', padx=5)
        self.gen_med_opt.trace('w',self.gen_med_opt_selected)

        Separator(botframe, orient='vertical').pack(fill='y', side='left')
        self.check_show_esenseat = Checkbutton(botframe, text='Show eSense Attention', variable=self.show_esenseat, onvalue=1, offvalue=0)
        self.check_show_esenseat.pack(side='left',padx=5)
        self.show_esenseat.trace('w',self.show_esense_at_selected)
        self.check_show_esensemed = Checkbutton(botframe, text='Show eSense Meditation', variable=self.show_esensemed, onvalue=1, offvalue=0)
        self.check_show_esensemed.pack(side='left',padx=5)
        self.show_esensemed.trace('w',self.show_esense_med_selected)

        Button(botframe, text='Close', command=handle_close).pack(side='right')
        
        self.signallabel = Label(botframe, image=self.CONN0)
        self.signallabel.pack(side='right', padx=5)
        Hovertip(self.signallabel, 'The current signal quality from the headset.')