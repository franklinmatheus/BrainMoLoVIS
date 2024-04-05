from tkinter import Button, Label, Toplevel, Frame, font, IntVar, StringVar, IntVar, Entry, messagebox
from seaborn import lineplot, boxplot, heatmap, swarmplot, regplot, stripplot, scatterplot
from numpy import arange, array, corrcoef
from pandas import concat, DataFrame

from brainmolovis.apputils.mindwavedata import *
from brainmolovis.appviewer.datavis import VisualizationWindow

class SetFolderTagWindow(Toplevel):

    def get_inputed(self): return self.inputed
    def get_ids(self): return [id.get() for id in self.file_ids]
    def get_folder_tag(self): return self.folder_tag.get()

    def process_input(self):
        allvalid = True
        for id in self.file_ids:
            if id.get() == None: 
                allvalid = False
                break
        
        if self.folder_tag == '': allvalid = False

        if allvalid: 
            self.inputed.set(1)
            self.destroy()
        else: messagebox.showinfo('Error', 'You must inform all entries!', parent=self)

    def process_close(self):
        self.inputed.set(2)
        self.destroy()

    def __init__(self, parent, folder, files) -> None:
        super().__init__(parent)

        self.title('File Tags')
        #self.geometry('720x480')
        self.resizable(False, False)
        self.config(padx=10, pady=10)
        self.protocol('WM_DELETE_WINDOW', self.process_close)
        
        self.inputed = IntVar(value=0)
        self.folder_tag = StringVar(self)
        self.folder_tag.set(folder)
        self.file_ids = []

        Label(self, text='Set the Folder Tag and File IDs', font=("Arial", 10, font.BOLD)).pack(anchor='center', pady=(0,10))

        inputsgrid = Frame(self)
        inputsgrid.grid_columnconfigure(1, weight=1)

        Label(inputsgrid, text='Folder Tag (current folder: ../' + folder +')', font=("Arial", 12, font.BOLD)).grid(row=0, column=0, pady=(0,10), sticky='w', padx=(0,10))
        input = Entry(inputsgrid, textvariable=self.folder_tag, border=1)
        input.grid(row=0, column=1, pady=0, sticky='ew')

        Label(inputsgrid, text='File IDs:', font=("Arial", 12, font.BOLD)).grid(row=1, column=0, pady=(0,10), sticky='w', padx=(0,10))

        for i in range(0,len(files)):
            self.file_ids.append(IntVar(self))
            self.file_ids[i].set(i)

            Label(inputsgrid, text=files[i]).grid(row=i+2, column=0, pady=(0,10), sticky='nsw', padx=(0,10))
            input = Entry(inputsgrid, textvariable=self.file_ids[i], border=1)
            input.grid(row=i+2, column=1, pady=0, sticky='ew')
        
        inputsgrid.pack(fill='x', anchor='center')

        Button(self, text='Open', command=self.process_input).pack(anchor='center', side='bottom')


class MultipleFoldersVisualizationWindow(VisualizationWindow):

    def esense_attention_boxplot(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        boxplot(data=self.df, y='esenseat', x='tag', ax=ax, linewidth=1,
                medianprops=dict(color='#750101', linewidth=2),
                boxprops=dict(facecolor='#ff8f87', edgecolor='black'))

        ax.set_xlabel('Folders')
        ax.set_ylabel('eSense Attention')
        ax.set_title('eSense Attention Variation')

        self.canvas.draw()

    def esense_meditation_boxplot(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        boxplot(data=self.df, y='esensemed', x='tag', ax=ax, linewidth=1,
                medianprops=dict(color='#012775', linewidth=2),
                boxprops=dict(facecolor='#678ee0', edgecolor='black'))

        ax.set_xlabel('Folders')
        ax.set_ylabel('eSense Meditation')
        ax.set_title('eSense Attention Meditation')

        self.canvas.draw()

    def __init__(self, parent, dfs, folders, tags) -> None:
        super().__init__(parent)
        self.title('Visualization Module [Multiple Folders]')

        self.folders = folders
        self.tags = tags
        self.genat_type = ''
        self.genmed_type = ''

        for i in range(0,len(dfs)): 
            dfs[i]['tag'] = self.tags[i]
            
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
        
        self.create_singledatavis_opt('eSense Attention Boxplot', self.esense_attention_boxplot)
        self.create_singledatavis_opt('eSense Attention Scatterplot', self.esense_attention_scatterplot)
        
        self.df = concat(dfs, ignore_index=True)