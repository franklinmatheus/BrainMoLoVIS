from seaborn import lineplot, heatmap, regplot, histplot
from numpy import arange

from brainmolovis.apputils.mindwavedata import *
from brainmolovis.appviewer.datavis import VisualizationWindow

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