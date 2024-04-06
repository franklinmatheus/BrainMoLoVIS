from seaborn import lineplot, heatmap, regplot, histplot
from numpy import arange, corrcoef, full
from scipy.stats import spearmanr
from pandas import DataFrame

from brainmolovis.apputils.mindwavedata import *
from brainmolovis.appviewer.datavis import VisualizationWindow

class SingleFileVisualizationWindow(VisualizationWindow):

    def p_value_interpretation(self, pvalue) -> str:
        if pvalue < 0.001: return '***'
        elif pvalue < 0.01: return '**'
        elif pvalue < 0.05: return '*'
        
        return ''
    
    def spearman_corr_matrix_labels(self, corr_values, p_values) -> list[list[str]]:
        corr_values = DataFrame.from_dict(corr_values)
        p_values = DataFrame.from_dict(p_values)

        matrix_shape = corr_values.to_numpy().shape
        labels = []
        for i in range(0,matrix_shape[0]):
            row = []
            for j in range(0,matrix_shape[1]):
                row.append(str(round(corr_values.to_numpy()[i][j],3)) + '\nρ = ' + str(round(p_values.to_numpy()[i][j],3)) + '\n' + self.p_value_interpretation(p_values.to_numpy()[i][j]))
            labels.append(row)

        return labels

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
                yticklabels=False, xticklabels=False)
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
                    yticklabels=False, xticklabels=False)
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

    def esense_power_bands_pearson_correlation(self) -> None:
        bands = ['delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma']

        values = {}
        for band in bands:
            if band not in values: values[band] = []
            values[band].append(corrcoef(self.df[band].to_list(), self.df['esenseat'].to_list())[0][1])
            values[band].append(corrcoef(self.df[band].to_list(), self.df['esensemed'].to_list())[0][1])

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap(DataFrame.from_dict(values), cmap='Spectral_r', ax=ax, annot=True, vmin=-1, vmax=1)

        ax.set_title('Power Bands Pearson Correlation Matrix')
        ax.set_yticklabels(['eSense Attention', 'eSense Meditation'], rotation=0)
        ax.set_xticklabels(bands, rotation=90)

        self.canvas.draw()

    def power_bands_pearson_correlation(self) -> None:
        bands = ['delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma']
        cols = list(set(bands) & set(self.df.columns))

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap(self.df[cols].corr(method='pearson'), cmap='Spectral_r', ax=ax, annot=True, vmin=-1, vmax=1)

        ax.set_title('Power Bands Pearson Correlation Matrix')
        xticks = ax.get_xticklabels()
        ax.set_xticklabels(xticks, rotation=90)
        yticks = ax.get_yticklabels()
        ax.set_yticklabels(yticks, rotation=0)

        self.canvas.draw()

    def esense_power_bands_spearman_correlation(self) -> None:
        bands = ['delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma']
        cols = list(set(bands) & set(self.df.columns))

        corr_values = {}
        p_values = {}
        for band in cols:
            if band not in corr_values: corr_values[band] = []
            if band not in p_values: p_values[band] = []
            
            corr, pval = spearmanr(self.df[band].to_list(), self.df['esenseat'].to_list())
            corr_values[band].append(corr)
            p_values[band].append(pval)

            corr, pval = spearmanr(self.df[band].to_list(), self.df['esensemed'].to_list())
            corr_values[band].append(corr)
            p_values[band].append(pval)

        labels = self.spearman_corr_matrix_labels(corr_values, p_values)

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap(DataFrame.from_dict(corr_values), cmap='Spectral_r', ax=ax, annot=labels, fmt='', vmin=-1, vmax=1)

        ax.set_title('Power Bands Spearman Correlation Matrix')
        ax.set_yticklabels(['eSense Attention', 'eSense Meditation'], rotation=0)
        ax.set_xticklabels(bands, rotation=90)

        self.canvas.draw()

    def power_bands_spearman_correlation(self) -> None:
        bands = ['delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma']
        cols = list(set(bands) & set(self.df.columns))

        corr_values = {}
        p_values = {}
        for band_i in cols:
            for band_j in cols:

                if band_i not in corr_values: corr_values[band_i] = []
                if band_i not in p_values: p_values[band_i] = []
                
                corr, pval = spearmanr(self.df[band_i].to_list(), self.df[band_j].to_list())
                corr_values[band_i].append(corr)
                p_values[band_i].append(pval)

        labels = self.spearman_corr_matrix_labels(corr_values, p_values)

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        heatmap(DataFrame.from_dict(corr_values), cmap='Spectral_r', ax=ax, annot=labels, fmt='', vmin=-1, vmax=1)

        ax.set_title('Power Bands Spearman Correlation Matrix')
        xticks = ax.get_xticklabels()
        ax.set_xticklabels(xticks, rotation=90)
        yticks = ax.get_yticklabels()
        ax.set_yticklabels(cols, rotation=0)

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

        self.create_singledatavis_opt('eSense Attention Lineplot', self.esense_attention_history_line)
        self.create_singledatavis_opt('eSense Attention Heatmap', self.esense_attention_history_heatmap)
        self.create_singledatavis_opt('eSense Attention Histogram', self.esense_attention_histogram)
        self.create_singledatavis_opt('eSense Meditation Lineplot', self.esense_meditation_history_line)
        self.create_singledatavis_opt('eSense Meditation Heatmap', self.esense_meditation_history_heatmap)
        self.create_singledatavis_opt('eSense Meditation Histogram', self.esense_meditation_histogram)
        
        self.create_multipledatavis_opt('eSense and Power Bands Pearson Correlation', self.esense_power_bands_pearson_correlation)
        self.create_multipledatavis_opt('Power Bands Pearson Correlation', self.power_bands_pearson_correlation)
        self.create_multipledatavis_opt('eSense and Power Bands Spearman Correlation', self.esense_power_bands_spearman_correlation)
        self.create_multipledatavis_opt('Power Bands Spearman Correlation', self.power_bands_spearman_correlation)
        self.create_multipledatavis_opt('eSense Attention and Meditation History', self.esense_attention_meditation_history)