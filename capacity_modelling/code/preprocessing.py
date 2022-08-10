import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
import re

from decimal import *

### GLOBAL VARIABLE ###
# Change column name, if this is not the default format.
COL_NAME = ['volume name', 'capacity (GiB)', 'used physical (GiB)',
            'used logical (GiB)', 'free (GiB)', 'used %',
            'regular files', 'symbolic links', 'max file size (GiB)',
            'median file size (bytes)', 'average file size (bytes)',
            'directories', 'directories with subdirectories only',
            'empty directories', 'max dir size (GiB)', 'run_time']

# Change, add or remove volume name if required.
VOL_NAME = ['Bioinf', 'Projects', 'General', 'Genomics',
            'Home', 'System', 'Img', 'ImageData',
            'SBPM', 'Sysbio', 'Admin', 'Archive', 'DBkp']

############################ FUNCTIONS ############################

def load_csv_files(directory, filenames = [], col_name = COL_NAME):
    '''
    A function to load csv files from directory and selected filenames.

    Parameters
    ----------
        - directory : Path Directory
            Example. 'C:/desktop/folder' or '../raw_data'
        - filenames : List
            List of filenames that want to be load. If empty, read all csv
            files inside directory.
        - col_name : List
            List of all column names of the csv files. Default is set to
            GLOBAL COL_NAME.

    Returns
    -------
        - combined_df : Pandas Dataframe
            Combination of all csv files.
        - flagged_df : Pandas Dataframe
            Csv files that doesn't have the same column names as col_name.
    '''
    assert len(os.listdir(directory)) != 0, \
        "Please ensure directory is not empty."

    # If filenames are not specified, read all files
    if len(filenames) == 0:
        filenames = os.listdir(directory)

    assert len(filenames) != 0 and \
        all(file in os.listdir(directory) for file in filenames), \
        "Please ensure file exists inside the directory."

    list_df = []
    flagged_df = []

    for file in filenames:
        temp_df = pd.read_csv(os.path.join(directory, file))
        if temp_df.columns.all() != col_name:
            list_df.append(temp_df)
        else:
            flagged_df.append(temp_df)

    combined_df = pd.concat(list_df)

    return combined_df, flagged_df

###################################################################

def clean_html(column):
    '''
    A function to clean html tags out of a string.

    Parameters
    ----------
        - column : Pandas Series
            Targeted Column.
    Returns
    -------
        - column : Pandas Series
            Cleaned Column.
    '''
    html = re.compile('<.*?>')
    column = html.sub(r'', column)
    return column

###################################################################

def search_column(string, column = COL_NAME):
    '''
    A function to search a string in the columns.

    Parameters
    ----------
        - string : str
            String searched.
        - column : List
            List of columns that want to be searched.

    Returns
    -------
        A list of columns containing the string.
    '''
    return [name for name in column if string in name]

###################################################################

def convert_GiB_to_TB(column):
    '''
    A function to convert Gigabyte to Terabyte.

    Parameters
    ----------
        - column : Pandas Series
            Targeted Column.

    Returns
    -------
        Column in Terabyte format. (column / 1024)
    '''
    return column / 1024

###################################################################

def convert_bytes_to_TB(column):
    '''
    A function to convert byte to Terabyte.

    Parameters
    ----------
        - column : Pandas Series
            Targeted Column.

    Returns
    -------
        Column in Terabyte format. (column * 1e-12)
    '''
    return column * 1e-12

###################################################################

def preprocessed_date(column):
    '''
    A function to extract date.

    Parameters
    ----------
        - column : Pandas Series
            Targeted Column.

    Returns
    -------
        Pandas Series containing date only in datetime format.
    '''
    return pd.to_datetime(column, dayfirst = True).dt.date

###################################################################

def separate_by_volume(dataframe, volume = VOL_NAME):
    '''
    A function to separate dataframe by volume.

    Parameters
    ----------
        - dataframe : Pandas Dataframe
            Loaded and Preprocessed Dataframe.
        - volume : List
            List of Volume. Default is GLOBAL VOL_NAME.

    Returns
    -------
        - volume_df : Dictionary
            A dictionary with volume name as its key and dataframe as the value.
    '''
    volume_df = {}
    for name in volume:
        tmp_df = dataframe[dataframe['volume name'] == name]
        volume_df[name] = tmp_df.reset_index(drop = True)
    return volume_df

###################################################################

def preprocess_pipeline(dataframe, columns = COL_NAME):
    '''
    A function to preprocess the loaded csv files as a pipeline.

    Parameters
    ----------
        - dataframe : Pandas Dataframe
            Loaded csv dataframe
        - columns : List
            List of columns names selected. Default is GLOBAL COL_NAME.

    Returns
    -------
        - dataframe : Pandas Dataframe
            Preprocessed Dataframe with selected columns.
    '''
    dataframe['volume name'] = dataframe['volume name'].apply(clean_html)
    dataframe['date'] = preprocessed_date(dataframe['run_time'])

    dataframe = dataframe.sort_values(['volume name', 'date'],
                                        ascending = [True, True])

    dataframe = dataframe[columns].replace(9.99, np.nan)

    return dataframe
