from os.path import join, isfile
from os import listdir
from pandas import DataFrame, read_csv

from brainmolovis.appconfig.config import get_logger_file_sep

def load_dataframe(filename) -> DataFrame:
    sep = get_logger_file_sep()

    try: 
        df = read_csv(filename, sep=sep)
        cols = sorted(list(set(df.columns) - set(['raweeg','esenseat','esensemed','delta','theta','lowalpha','highalpha','lowbeta','highbeta','lowgamma','highgamma'])))
        gens = [i.split('_')[0] for i in cols if 'genat' in i or 'genmed' in i]
        
        if len(gens) == len(cols): return df
        else: return DataFrame()
    except Exception: return DataFrame()
        
def load_folder_dataframes(folder) -> tuple[list: DataFrame, list: str, str]:
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    dfs = []

    for file in files:
        df = load_dataframe(folder + '/' + file)
        if df.empty: return [], [], file
        dfs.append(df)

    return dfs, files, ''