import pandas as pd
import tabula
import chardet
from dotenv import load_dotenv
import os
load_dotenv()

# This is what you can modify
input_pdf = os.getenv('INPUT_PDF')
name_csv = os.getenv('BESTSELLERS')
page_range = os.getenv('RANGE_BESTSELLERS')
types = os.getenv('TYPE_BESTSELLERS')

def run():

    tabula.convert_into(input_pdf, name_csv, output_format='csv', pages=page_range)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])

    header = dataframe.iloc[1]
    section = dataframe.iloc[0][0]
    dataframe = dataframe[2:]
    dataframe.columns = header
    dataframe.insert(0, 'Type', types)
    dataframe.insert(1, 'Section', '')

    rowsNr = dataframe.shape[0]
    for i in range(0, rowsNr):
        sectionR = dataframe.iloc[i]
        if type(sectionR[3]) == float and type(sectionR[2]) == str:
            section = sectionR[2]
        if 'section' in locals():
            dataframe.loc[i + 1, 'Section'] = section

    dataframe.to_csv(name_csv)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])

    rowsNr = dataframe.shape[0]
    for i in range(0, rowsNr):
        if type(dataframe.loc[i, 'Product Code']) == float or type(dataframe.loc[i, 'Description']) == float or dataframe.loc[i, 'Product Code'] == 'Product Code':
            dataframe.drop(axis=0, index=i, inplace=True)


    dataframe.to_csv(name_csv)

    with open(name_csv, 'rb') as f:
        enc = chardet.detect(f.read())

    dataframe = pd.read_csv(name_csv, encoding=enc['encoding'])
    dataframe = dataframe.drop([dataframe.columns[0], dataframe.columns[1]], axis=1)
    dataframe.to_csv(name_csv)


