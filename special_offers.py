import numpy as np
import pandas as pd
import tabula
import chardet
from dotenv import load_dotenv
import os

load_dotenv('index.env')

# This is what you can modify
input_pdf = os.getenv('INPUT_PDF')
name_csv = os.getenv('SPECIAL_OFFERS')
page_range = os.getenv('RANGE_SPECIAL_OFFERS')
types = os.getenv('TYPE_SPECIAL_OFFERS')

def run():

    tabula.convert_into(input_pdf, name_csv, output_format='csv', pages=page_range)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])

    if not dataframe.columns[0] == 'Code':
        rowsNr = dataframe.shape[0]
        for i in range(0, rowsNr):
            if dataframe.iloc[i, 0] == 'Code':
                headerPos = i
                break
        header = dataframe.iloc[headerPos]
        dataframe.columns = header

    section = dataframe.iloc[0,0]
    dataframe = dataframe[2:]

    dataframe.insert(0, 'Type', types)
    dataframe.insert(1, 'Section', '')

    rowsNr = dataframe.shape[0]
    for i in range(0, rowsNr):
        sectionR = dataframe.iloc[i]
        if type(sectionR[3]) == float and type(sectionR[2]) == str:
            section = sectionR[2]
        if 'section' in locals():
            dataframe.loc[i + 2, 'Section'] = section

    dataframe.to_csv(name_csv)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])

    rowsNr = dataframe.shape[0]
    for i in range(0, rowsNr):
        if type(dataframe.loc[i, 'List Price']) == float or dataframe.loc[i, 'List Price'] == 'List Price':
            dataframe.drop(axis=0, index=i, inplace=True)

    dataframe.to_csv(name_csv)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])

    rowsNr = dataframe.shape[0]
    colNr = dataframe.shape[1]
    colIndex = colNr - 1
    for i in range(0, rowsNr):
        if type(dataframe.iloc[i, colIndex]) == np.float64 and np.isnan(dataframe.iloc[i, colIndex]):
            dataframe.iloc[i, colIndex] = dataframe.iloc[i, colIndex - 1]
            dataframe.iloc[i, colIndex - 1] = dataframe.iloc[i, colIndex - 2]
            dataframe.iloc[i, colIndex - 2] = ''

    dataframe.to_csv(name_csv)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])
    dataframe = dataframe.drop([dataframe.columns[0], dataframe.columns[1], dataframe.columns[2],dataframe.columns[10]], axis=1)
    dataframe.to_csv(name_csv)