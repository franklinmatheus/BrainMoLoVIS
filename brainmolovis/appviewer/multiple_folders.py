from tkinter import Button, Label, Toplevel, Frame, font, IntVar, StringVar, IntVar, Entry, messagebox
from seaborn import lineplot, boxplot, heatmap, swarmplot, regplot
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
        
        self.df = concat(dfs, ignore_index=True)