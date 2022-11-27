import os
import chardet
import glob
import pandas as pd

name_csv = os.getenv('NAME')

cwd = os.path.abspath('')
filelist = os.listdir(cwd)
csv_files = glob.glob('*.{}'.format('csv'))

def run():
    df_append = pd.DataFrame()

    for file in csv_files:
        with open(file, 'rb') as f:
            enc = chardet.detect(f.read())
        df = pd.read_csv(file, encoding=enc['encoding'])
        df_append = pd.concat([df_append, df], ignore_index=True)

    df_append.to_csv(name_csv)