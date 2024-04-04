from tkinter import Button, Label, PhotoImage, Toplevel, Frame, font, LabelFrame, IntVar, StringVar, Entry, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from seaborn import set_theme, lineplot, heatmap, regplot, boxplot, histplot
from numpy import arange
from pandas import concat
from sklearn.preprocessing import MinMaxScaler

from brainmolovis.apputils.mindwavedata import *

class VisualizationWindow(Toplevel):

    def create_singledatavis_opt(self, title, func) -> None:
        opframe = Frame(self.singledatavisframe, pady=5)
        opframe.pack(side='top', anchor='w')
        self.buttonop1 = Button(opframe, image=self.SHOWICON, command=func)
        self.buttonop1.pack(side='left')
        Label(opframe, text=title).pack(side='left')

    def create_multipledatavis_opt(self, title, func) -> None:
        opframe = Frame(self.multipledatavisframe, pady=5)
        opframe.pack(side='top', anchor='w')
        self.buttonop5 = Button(opframe, image=self.SHOWICON, command=func)
        self.buttonop5.pack(side='left')
        Label(opframe, text=title).pack(side='left')

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

        Label(self.optionsframe, text='Choose a vizualization to be displayed', font=("Arial", 12, font.BOLD)).pack(side='top', anchor='w')
        
        self.SHOWICON = PhotoImage(file = r"./imgs/show.png")

        self.singledatavisframe = LabelFrame(self.optionsframe, text='Single Data Visualizations', padx=5, pady=5)
        self.singledatavisframe.pack(fill='x', pady=5)

        self.multipledatavisframe = LabelFrame(self.optionsframe, text='Multiple Data Visualizations', padx=5, pady=5)
        self.multipledatavisframe.pack(fill='x', pady=5)

        self.chartframe = Frame(mainframe, background='white', highlightbackground='black', highlightthickness=1, padx=5, pady=5)
        self.chartframe.pack(expand=True, fill='both', side='right')

        self.fig = Figure()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a visualization', horizontalalignment='center', verticalalignment='center')
        
        def on_key_press(event):
            key_press_handler(event, self.canvas, self.toolbar)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chartframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chartframe)
        self.toolbar.config(background='white')
        self.toolbar._message_label.config(background='white')
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        self.canvas.mpl_connect("key_press_event", on_key_press)

        set_theme()

        botframe = Frame(self)
        Button(botframe, text='Close', command=self.handle_close).pack(anchor='e')
        botframe.pack(fill='x', side='bottom', padx=10, pady=(0,10))


class SingleFileVisualizationWindow(VisualizationWindow):

    def esense_attention_history_line(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(self.df['esenseat'], color='red', ax=ax)
        regplot(x=arange(0,len(self.df['esenseat']),1), y=self.df['esenseat'], fit_reg=True, ax=ax, color='black', scatter_kws=dict(alpha=0))
        
        ax.set_title('eSense Attention History')
        ax.set_ylabel('eSense Attention')
        ax.set_xlabel('Samples')

        self.canvas.draw()
    
    def esense_attention_history_heatmap(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap([self.df['esenseat']], cmap='Spectral_r', ax=ax, 
                    yticklabels=False, xticklabels=False,
                    cbar_kws=dict(use_gridspec=False, location="bottom", shrink=0.5))
        ax.set_title('eSense Attention Heatmap')
        ax.set_xlabel('Samples')

        self.canvas.draw()

    def esense_meditation_history_line(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(self.df['esensemed'], color='blue', ax=ax)
        regplot(x=arange(0,len(self.df['esensemed']),1), y=self.df['esensemed'], fit_reg=True, ax=ax, color='black', scatter_kws=dict(alpha=0)) 
        
        ax.set_title('eSense Meditation History')
        ax.set_ylabel('eSense Meditation')
        ax.set_xlabel('Samples')

        self.canvas.draw()
    
    def esense_meditation_history_heatmap(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap([self.df['esensemed']], cmap='Spectral_r', ax=ax, 
                    yticklabels=False, xticklabels=False,
                    cbar_kws=dict(use_gridspec=False, location="bottom", shrink=0.5))
        ax.set_title('eSense Meditation Heatmap')
        ax.set_xlabel('Samples')

        self.canvas.draw()

    def esense_attention_histogram(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        histplot(self.df['esenseat'], bins=10, ax=ax, color='red')
        
        ax.set_title('eSense Attention Histogram')
        ax.set_xlabel('eSense Attention')
        ax.set_ylabel('Frequency')
        ax.set_xlim(0,100)
        self.canvas.draw()

    def esense_meditation_histogram(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        histplot(self.df['esensemed'], bins=10, ax=ax, color='blue')
        
        ax.set_title('eSense Meditation Histogram')
        ax.set_xlabel('eSense Meditation')
        ax.set_ylabel('Frequency')
        ax.set_xlim(0,100)
        self.canvas.draw()

    # Generates a visualization with a line plot to each power band (the plots appear stacked in the visualization)
    def power_bands_line_plots(self) -> None:
        pass

    # Generates the Power Spectral Density of the Raw EEG signal (usin FFT: fast fourier transform)
    def psd_fft_raweeg(self) -> None:
        pass

    def power_bands_correlation(self) -> None:
        bands = ['delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma']
        cols = list(set(bands) & set(self.df.columns))

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap(self.df[cols].corr(method='pearson'), cmap='rocket_r', ax=ax, annot=True,
                cbar_kws=dict(location="bottom", shrink=0.5))

        ax.set_title('Power Bands Pearson Correlation Matrix')

        self.canvas.draw()

    def esense_attention_meditation_history(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(self.df['esenseat'], color='red', ax=ax, label='Attention')
        regplot(x=arange(0,len(self.df['esenseat']),1), y=self.df['esenseat'], fit_reg=True, ax=ax, color='#570202', scatter_kws=dict(alpha=0))
        lineplot(self.df['esensemed'], color='blue', ax=ax, label='Meditation')
        regplot(x=arange(0,len(self.df['esensemed']),1), y=self.df['esensemed'], fit_reg=True, ax=ax, color='#020357', scatter_kws=dict(alpha=0))

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_title('eSense Attention and Meditation History')
        ax.set_xlabel('Samples')
        ax.set_ylabel('Attention and Medidation Level')

        self.canvas.draw()

    def __init__(self, parent, df) -> None:
        super().__init__(parent)
        self.title('Visualization Module [Single File]')

        self.df = df

        self.create_singledatavis_opt('eSense Attention History', self.esense_attention_history_line)
        self.create_singledatavis_opt('eSense Attention Heatmap', self.esense_attention_history_heatmap)
        self.create_singledatavis_opt('eSense Meditation History', self.esense_meditation_history_line)
        self.create_singledatavis_opt('eSense Meditation Heatmap', self.esense_meditation_history_heatmap)
        self.create_singledatavis_opt('eSense Attention Histogram', self.esense_attention_histogram) # TODO
        self.create_singledatavis_opt('eSense Meditation Histogram', self.esense_meditation_histogram) # TODO
        self.create_singledatavis_opt('Raw EEG Power Spectral Density (FFT)', self.psd_fft_raweeg) # TODO
        
        self.create_multipledatavis_opt('Power Bands Line Plots', self.power_bands_line_plots) # TODO
        self.create_multipledatavis_opt('Power Bands Pearson Correlation', self.power_bands_correlation)
        self.create_multipledatavis_opt('eSense Attention and Meditation History', self.esense_attention_meditation_history)

class SetFilesTagsWindow(Toplevel):

    def get_inputed(self): return self.inputed
    def get_tags(self): return [tag.get() for tag in self.tags]

    def process_input(self):
        allvalid = True
        for tag in self.tags:
            if tag.get() == '': 
                allvalid = False
                break
        
        if allvalid: 
            self.inputed.set(1)
            self.destroy()
        else: messagebox.showinfo('Error', 'You must inform all tags!', parent=self)

    def process_close(self):
        self.inputed.set(2)
        self.destroy()

    def __init__(self, parent, files) -> None:
        super().__init__(parent)

        self.title('File Tags')
        #self.geometry('720x480')
        self.resizable(False, False)
        self.config(padx=10, pady=10)
        self.protocol('WM_DELETE_WINDOW', self.process_close)
        
        self.inputed = IntVar(value=0)
        self.tags = []

        Label(self, text='Set the File Tags', font=("Arial", 10, font.BOLD)).pack(anchor='center', pady=(0,10))

        inputsgrid = Frame(self)
        inputsgrid.grid_columnconfigure(1, weight=1)

        for i in range(0,len(files)):
            self.tags.append(StringVar(self))
            self.tags[i].set('File'+str(i))

            Label(inputsgrid, text=files[i]).grid(row=i, column=0, pady=(0,10), sticky='e', padx=(0,10))
            input = Entry(inputsgrid, textvariable=self.tags[i], border=1)
            input.grid(row=i, column=1, pady=0, sticky='ew')
        
        inputsgrid.pack(fill='x', anchor='center')

        Button(self, text='Open', command=self.process_input).pack(anchor='center', side='bottom')


class MultipleFilesVisualizationWindow(VisualizationWindow):

    def esense_attention_history(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(data=self.df, x='seq', y='esenseat', hue='tag', ax=ax)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel('Samples')
        ax.set_ylabel('eSense Attention')
        ax.set_title('eSense Attention History')

        self.canvas.draw()

    def esense_attention_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y='esenseat', x='tag', hue='tag', ax=ax, dodge=False)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xticklabels([])
        ax.set_xlabel('Files')
        ax.set_ylabel('eSense Attention')
        ax.set_title('eSense Attention Variation')

        self.canvas.draw()

    def esense_meditation_history(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        lineplot(data=self.df, x='seq', y='esensemed', hue='tag', ax=ax)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel('Samples')
        ax.set_ylabel('eSense Meditation')
        ax.set_title('eSense Meditation History')

        self.canvas.draw()

    def esense_meditation_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y='esensemed', x='tag', hue='tag', ax=ax, dodge=False)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xticklabels([])
        ax.set_xlabel('Files')
        ax.set_ylabel('eSense Meditation')
        ax.set_title('eSense Meditation Variation')

        self.canvas.draw()

    def generated_attention_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y=self.genat_type, x='tag', hue='tag', ax=ax, dodge=False)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xticklabels([])
        ax.set_xlabel('Files')
        ax.set_ylabel('Generated Attention')
        ax.set_title('Generated Attention ('+ str(self.genat_type.split('_')[1]) +') Variation')

        self.canvas.draw()

    def generated_attention_history(self) -> None:
        pass

    def generated_meditation_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y=self.genmed_type, x='tag', hue='tag', ax=ax, dodge=False)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xticklabels([])
        ax.set_xlabel('Files')
        ax.set_ylabel('Generated Meditation')
        ax.set_title('Generated Meditation ('+ str(self.genmed_type.split('_')[1]) +') Variation')

        self.canvas.draw()

    def generated_meditation_history(self) -> None:
        pass

    def esense_attention_correlation(self) -> None:
        pass

    def esense_meditation_correlation(self) -> None:
        pass

    def generated_attention_correlation(self) -> None:
        pass

    def generated_meditation_correlation(self) -> None:
        pass

    def __init__(self, parent, dfs, files, tags) -> None:
        super().__init__(parent)
        self.title('Visualization Module [Multiple Files]')

        self.files = files
        self.tags = tags
        self.genat_type = ''
        self.genmed_type = ''

        for i in range(0,len(dfs)): 
            dfs[i]['tag'] = self.tags[i]
            dfs[i]['seq'] = arange(0,len(dfs[i].index),1)
            
            gens = {i.split('_')[0]:i for i in dfs[i].columns if 'gen' in i}
            
            if 'genat' in gens:
                if self.genat_type == '': self.genat_type = gens['genat']
                elif self.genat_type == 'None': pass
                elif self.genat_type != gens['genat']: self.genat_type = 'None'
            else: self.genat_type = 'None'

            if 'genmed' in gens:
                if self.genmed_type == '': self.genmed_type = gens['genmed']
                elif self.genmed_type == 'None': pass
                elif self.genmed_type != gens['genmed']: self.genmed_type = 'None'
            else: self.genmed_type = 'None'

            #scaler = MinMaxScaler((0,100))
            #dfs[i][[self.genat_type,self.genmed_type]] = scaler.fit_transform(dfs[i][[self.genat_type,self.genmed_type]])
            
        self.df = concat(dfs, ignore_index=True)

        self.create_singledatavis_opt('eSense Attention History', self.esense_attention_history)
        self.create_singledatavis_opt('eSense Attention Variation', self.esense_attention_variation)
        self.create_singledatavis_opt('eSense Meditation History', self.esense_meditation_history)
        self.create_singledatavis_opt('eSense Meditation Variation', self.esense_meditation_variation)

        if self.genat_type != 'None':
            self.create_singledatavis_opt('Generated Attention History', self.generated_attention_history)
            self.create_singledatavis_opt('Generated Attention Variation', self.generated_attention_variation)
        if self.genmed_type != 'None':
            self.create_singledatavis_opt('Generated Meditation History', self.generated_meditation_history)
            self.create_singledatavis_opt('Generated Meditation Variation', self.generated_meditation_variation)

        self.create_multipledatavis_opt('eSense Attention Correlation', self.esense_attention_correlation)
        self.create_multipledatavis_opt('eSense Meditation Correlation', self.esense_meditation_correlation)
        self.create_multipledatavis_opt('Generated Attention Correlation', self.generated_attention_correlation)
        self.create_multipledatavis_opt('Generated Meditation Correlation', self.generated_meditation_correlation)