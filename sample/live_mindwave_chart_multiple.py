from multiprocessing import Process
from random import randint
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import socket

host = '127.0.0.1'
port = 13854
param = '{"enableRawOutput": true, "format": "Json"}'

raw_eeg_data = []
attention, meditation, blink = [], [], 0
x_data = []
read_data = True

open('output_mindwave.txt', 'w').close()

def reading_data():
    global blink

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
        skt.connect((host, port))
        
        skt.sendall(str.encode(param))
        print(skt.recv(2048).decode('utf-8'))

        while read_data:
            data = skt.recv(2048)
            if not data: 
                print('no data')
                break

            else:
                with open('output_mindwave.txt', 'a') as file:
                    temp = data.decode('utf-8')
                    file.write(temp)
                    if 'rawEeg' in temp and 'attention' not in temp:
                        try: raw_eeg_data.append(int(temp.split('rawEeg":')[1].split('}')[0]))
                        except ValueError: raw_eeg_data.append(0)
                    
                    if 'attention' in temp:
                        try: attention.append(int(temp.split('attention":')[1].split(',')[0]))
                        except ValueError: attention.append(0)

                    if 'meditation' in temp:    
                        try: meditation.append(int(temp.split('meditation":')[1].split('}')[0]))
                        except ValueError: meditation.append(0)

                    if 'blinkStrength' in temp:
                        try: blink = int(temp.split('blinkStrength":')[1].split('}')[0])
                        except ValueError: blink = 0

thread = Thread(target=reading_data)
thread.start()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

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
    global blink

    ax3.cla()

    x_data = np.arange(0+len(raw_eeg_data))

    if len(raw_eeg_data) > 0:
        ax1.set_ylim(min(raw_eeg_data[-100:]), max(raw_eeg_data[-100:]))
    ax1.set_xlim(int(len(x_data)/100)*100, int(len(x_data)/100)*100+100)
    
    ax1.set_title('Raw EEG')
    line_raweeg.set_ydata(raw_eeg_data[-100:])
    line_raweeg.set_xdata(x_data[-100:])

    # esense at
    x_data = np.arange(0+len(attention))
    ax2.set_xlim(int(len(x_data)/20)*20, int(len(x_data)/20)*20+20)

    ax2.set_title('eSense Attention')
    line_atesense.set_ydata(attention[-20:])
    line_atesense.set_xdata(x_data[-20:])

    # esense med
    x_data = np.arange(0+len(meditation))
    ax4.set_xlim(int(len(x_data)/20)*20, int(len(x_data)/20)*20+20)

    ax4.set_title('eSense Meditation')
    line_medesense.set_ydata(meditation[-20:])
    line_medesense.set_xdata(x_data[-20:])
    
    # blink
    ax3.set_ylim(0,3)
    ax3.set_xlim(0,3)
    ax3.axes.xaxis.set_visible(False)
    ax3.axes.yaxis.set_visible(False)
    ax3.set_title('Blink Detection')
    if blink != 0:
        circle = plt.Circle((1.5,1.5), blink/100, color='red')
        ax3.add_patch(circle)
        blink = 0

def handle_close(e):
    global read_data
    read_data = False

animation = FuncAnimation(fig, func=animate, interval=250)
fig.canvas.mpl_connect('close_event', handle_close)
plt.tight_layout()
plt.show()