import os
import sys
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import argparse


def visualize_pca():
    """
    Function to visualize dataset using PCA to reduce the dimensions
    Saves the visualization to plots directory
    Args:
    Returns:
    """
    path = os.getcwd()
    data_path = os.path.join(path, 'data', 'raw', 'stock.csv')
    try:
        data = pd.read_csv(data_path)
    except IOError:
        print('Unable to retrieve data. Please get dataset from tushare and store it in the data/raw directory')
        sys.exit()
    data = data[(data['date'] > '2015-01-01') & (data['date'] <= '2017-03-08')].reset_index()
    del data['date']
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
    np_scaled = min_max_scaler.fit_transform(data)
    data = pd.DataFrame(np_scaled)
    reduced_data = PCA(n_components=2).fit_transform(data)

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1

    fig = plt.figure(1)
    plt.clf()

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    for index, row in data.iterrows():
        plt.plot(reduced_data[index, 0], reduced_data[index, 1], '.', markersize=4)

    plt.xticks(())
    plt.yticks(())
    plt.title('Visualization of dataset after PCA')
    plt.show()
    if not os.path.exists('plots'):
        os.makedirs('plots')
    fig.savefig('plots/PCA_Visualization.png')
    plt.close(fig)


def visualize_ica():
    print('To be implemented')
    pass


def visualize_tsne():
    print('To be implemented')
    pass


def parse():
    """
    Function to interact with user to get the arguments
    Args:
    Returns:
        dictionary<str,bool>
        dimension reduction techniques and its flag
    """
    parser = argparse.ArgumentParser(description='Process and visualization of dataset using Dimensionality Reduction'
                                                 ' Techniques like PCA, ICA and t-SNE.')
    parser.add_argument('--pca', action='store_true', help='Using PCA to reduce dimensions')
    parser.add_argument('--ica', action='store_true', help='Using ICA to reduce dimensions')
    parser.add_argument('--tsne', action='store_true', help='Using t-SNE to reduce dimensions')
    arguments = vars(parser.parse_args())
    if not any(arguments.values()):
        parser.error('No arguments provided, please set the flag at least one of the following: pca, ica, tsne')
    return arguments


if __name__ == '__main__':
    """
    Main function to call various visualization using appropriate dimension reduction technique
    Args:
    Returns:
    """
    args = parse()
    for technique in args:
        method = 'visualize_' + technique
        if args[technique]:
            print('Visualizing using ' + technique.upper())
            globals()[method]()
