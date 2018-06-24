import argparse
from config import *

import tushare as ts
import os


def retrieve(start, end, code):
    """
    Function to retrieve the dataset from tushare
    Saves the dataset as a csv in data/raw directory

    Args:
        start: Start date to retrieve
        end:   End date to retrieve
        code:  Stock code to retrieve
    Returns:
    """
    path = ['data', 'raw', 'raw_stock.csv']
    cur_path = os.getcwd()
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
    data_path = os.path.join(cur_path, *path)
    data = ts.get_hist_data(code=code, start=start, end=end)
    data.to_csv(data_path)


def parse():
    """
    Function to interact with user to get the arguments
    Args:
    Returns:
        dictionary<str,str>
        arguments for retrieval of stock dataset
    """
    parser = argparse.ArgumentParser(description='Retrieve dataset from tushare and save it as csv')
    parser.add_argument('--start', help='Start Date', default=START_DATE)
    parser.add_argument('--end', help='End Date', default=END_DATE)
    parser.add_argument('--code', help='Code for the stock index', default=CODE)
    arguments = vars(parser.parse_args())
    return arguments


if __name__ == '__main__':
    """
    Main function to retrieve and store the raw dataset
    Args:
    Returns:
    """
    args = parse()
    retrieve(args['start'], args['end'], args['code'])
