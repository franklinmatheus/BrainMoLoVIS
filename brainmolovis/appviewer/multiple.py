from tkinter import Button, Label, Toplevel, Frame, font, IntVar, StringVar, Entry, messagebox
from seaborn import lineplot, boxplot, heatmap
from numpy import arange, array, corrcoef
from pandas import concat, DataFrame

from brainmolovis.apputils.mindwavedata import *
from brainmolovis.appviewer.datavis import VisualizationWindow

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

    def get_mask(self, data):
        return array([[True if x < 0 else False for x in line] for line in data.to_numpy()])

    def esense_attention_history(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        values = {}
        longer = self.df['tag'].value_counts().index[0]
        for tag in self.df['tag'].unique():
            values[tag] = self.df[self.df['tag'] == tag]['esenseat'].to_list()
            
            if tag != longer: values[tag].extend([-1]* (len(self.df[self.df['tag'] == longer].index) - len(self.df[self.df['tag'] == tag].index)) )
        
        data = DataFrame.from_dict(values).transpose()
        mask = self.get_mask(data)

        heatmap(data, cmap='YlOrBr', ax=ax, mask=mask,
            yticklabels=True, xticklabels=False,
            cbar_kws=dict(use_gridspec=False, location="bottom", shrink=0.5))
        
        ax.set_title('eSense Attention Heatmap')
        ax.set_xlabel('Samples')
        ax.set_ylabel('Files')
        self.canvas.draw()

    def esense_attention_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y='esenseat', x='tag', ax=ax, linewidth=1,
                medianprops=dict(color='#750101', linewidth=2),
                boxprops=dict(facecolor='#ff8f87', edgecolor='black'))
        ax.set_xlabel('Files')
        ax.set_ylabel('eSense Attention')
        ax.set_title('eSense Attention Variation')

        self.canvas.draw()

    def esense_meditation_history(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        values = {}
        longer = self.df['tag'].value_counts().index[0]
        for tag in self.df['tag'].unique():
            values[tag] = self.df[self.df['tag'] == tag]['esensemed'].to_list()
            
            if tag != longer: values[tag].extend([-1]* (len(self.df[self.df['tag'] == longer].index) - len(self.df[self.df['tag'] == tag].index)) )
        
        data = DataFrame.from_dict(values).transpose()
        mask = mask = self.get_mask(data)

        heatmap(data, cmap='Blues', ax=ax, mask=mask,
            yticklabels=True, xticklabels=False,
            cbar_kws=dict(use_gridspec=False, location="bottom", shrink=0.5))
        
        ax.set_title('eSense Meditation Heatmap')
        ax.set_xlabel('Samples')
        ax.set_ylabel('Files')
        self.canvas.draw()

    def esense_meditation_variation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        boxplot(data=self.df, y='esensemed', x='tag', ax=ax, linewidth=1,
                medianprops=dict(color='#012775', linewidth=2),
                boxprops=dict(facecolor='#678ee0', edgecolor='black'))
        ax.set_xlabel('Files')
        ax.set_ylabel('eSense Meditation')
        ax.set_title('eSense Meditation Variation')

        self.canvas.draw()

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

    def attention_correlation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        vars = []
        corr = []
        for tag in self.df['tag'].unique():
            corr.append(
                corrcoef(self.df[self.df['tag'] == tag]['esenseat'].to_list(),
                         self.df[self.df['tag'] == tag][self.genat_type].to_list())[0][1]
            )

            vars.append(tag)

        heatmap([corr], cmap='Spectral_r', ax=ax, annot=True, vmin=-1, vmax=1,
                    yticklabels=False, xticklabels=vars)
        ax.set_title('eSense Attention and ' + self.genat_type.split('_')[1] + ' Pearson Correlation')
        ax.set_xlabel('Correlations')

        self.canvas.draw()

    def meditation_correlation(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        vars = []
        corr = []
        for tag in self.df['tag'].unique():
            corr.append(
                corrcoef(self.df[self.df['tag'] == tag]['esensemed'].to_list(),
                         self.df[self.df['tag'] == tag][self.genmed_type].to_list())[0][1]
            )

            vars.append(tag)

        heatmap([corr], cmap='Spectral_r', ax=ax, annot=True, vmin=-1, vmax=1,
                    yticklabels=False, xticklabels=vars)
        ax.set_title('eSense Meditation and ' + self.genmed_type.split('_')[1] + ' Pearson Correlation')
        ax.set_xlabel('Correlations')

        self.canvas.draw()

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
            self.create_singledatavis_opt('Generated Attention Variation', self.generated_attention_variation)
        if self.genmed_type != 'None':
            self.create_singledatavis_opt('Generated Meditation Variation', self.generated_meditation_variation)

        self.create_multipledatavis_opt('eSense and Generated Attention Correlation', self.attention_correlation)
        self.create_multipledatavis_opt('eSense and Generated Meditation Correlation', self.meditation_correlation)