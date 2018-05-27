import os
import sys
import pandas as pd


def get_data(path):
    """
    Function to retrieve raw dataset
    Args:
        list<str>: path to data file from project root
    Returns:
        DataFrame<...>
        dataframe of stocks data
    """
    cur_path = os.getcwd()
    data_path = os.path.join(cur_path, *path)
    try:
        data = pd.read_csv(data_path)
    except IOError:
        print('Unable to retrieve data. Please get dataset from tushare and store it in the data or raw directory')
        sys.exit()
    return data
