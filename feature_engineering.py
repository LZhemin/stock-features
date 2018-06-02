import argparse
import util
import numpy as np
import pandas as pd
from config import *
import os


def add_rsi(data):
    """
    Function to add new feature, Relative Strength Index (rsi) to dataframe
    Args:
        DataFrame<...>: Old dataframe
    Returns:
        DataFrame<...>
        New dataframe of stocks data with new feature(rsi)
    """
    data.set_index('date', inplace=True)

    # get gain and loss feature
    data['gain'] = np.where(data['price_change'] > 0, data['price_change'], 0)
    data['loss'] = np.where(data['price_change'] < 0, abs(data['price_change']), 0)

    # get avg gain and loss over PERIOD
    df2 = (data.rolling(center=False, window=PERIOD, min_periods=PERIOD)
           .mean()
           .reset_index()
           .drop_duplicates())
    df2.set_index('date', inplace=True)
    df2 = df2[df2.columns[-2:]]
    df2 = df2.rename(index=str, columns={'gain': 'avg_gain', 'loss': 'avg_loss'})

    # add the new avg_gain and avg_loss feature
    data = pd.concat([data, df2], axis=1)

    # First RS value is straightforward: divide the Average Gain by the Average Loss.
    # All subsequent RS calculations use the previous period's Average Gain and Average Loss for smoothing purposes
    # For calculation of Smoothed RS,
    # refer to http://cns.bu.edu/~gsc/CN710/fincast/Technical%20_indicators/Relative%20Strength%20Index%20(RSI).htm
    data = data.reset_index()
    for i in range(PERIOD, len(data)):
        data.at[i, 'avg_gain'] = (data.loc[i - 1]['avg_gain'] * (PERIOD - 1) + data.loc[i]['gain']) / PERIOD
        data.at[i, 'avg_loss'] = (data.loc[i - 1]['avg_loss'] * (PERIOD - 1) + data.loc[i]['loss']) / PERIOD

    # calculate relative strength
    data['rs'] = data['avg_gain'] / data['avg_loss']

    # calculate RSI
    data['rsi'] = 100 - (100 / (1 + data['rs']))

    # drop gain and loss feature as it is already captured in price_change
    data = data.drop(['gain', 'loss'], axis=1)

    return data


def add_bband(data):
    """
    Function to add new feature, Bollinger Bands (bband) to dataframe
    Args:
        DataFrame<...>: Old dataframe
    Returns:
        DataFrame<...>
        New dataframe of stocks data with new feature(bband)
    """

    # FutureWarning: pd.rolling_mean is deprecated for Series and will be removed in a future version
    # MA = pd.Series(pd.rolling_mean(data['close'], PERIOD))
    # MSD = pd.Series(pd.rolling_std(data['close'], PERIOD))

    MA = data['close'].rolling(window=PERIOD, center=False).mean()
    MSD = data['close'].rolling(window=PERIOD, center=False).std()
    b1 = 4 * MSD / MA
    B1 = pd.Series(b1, name='BollingerB_' + str(PERIOD))
    data = data.join(B1)

    b2 = (data['close'] - MA + 2 * MSD) / (4 * MSD)
    B2 = pd.Series(b2, name='Bollinger%b_' + str(PERIOD))
    data = data.join(B2)
    return data


def parse():
    """
    Function to interact with user to get the arguments
    Args:
    Returns:
        dictionary<str,bool>
        new features and its flag
    """
    parser = argparse.ArgumentParser(
        description='Perform feature engineering to get new features to be experimented with.')
    parser.add_argument('--rsi', action='store_true', help='Add RSI feature to the dataset')
    parser.add_argument('--bband', action='store_true', help='Add bband feature to the dataset')
    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.error('No arguments provided, please set the flag at least one of the following: rsi')
    return args


if __name__ == '__main__':
    """
    Main function to add new features to the dataset
    Saves the new dataset with new features to data directory
    Args:
    Returns:
    """
    path = ['data', 'raw', 'stock.csv']
    df = util.get_data(path)
    arguments = parse()
    name = 'stock'
    for feature in arguments:
        if arguments[feature]:
            name += '_' + feature
            method = 'add_' + feature
            print('Adding ' + feature.upper() + ' feature to dataset')
            df = globals()[method](df)
    path = os.path.join('data', name + '.csv')
    df.to_csv(path)
