# Stock Features
Repository for my undergraduate research program titled "Application of Deep Learning in Stock Market Index Prediction"

Repository contains mainly codes for:
- Data Visualization
- Technical Analysis
- Feature Engineering
- Dimensionality Reduction

Final Submitted paper can be found [here](URECA_Final.pdf)

## Getting Started Guide

### Getting Started for macOS and Unix-like

To run the server for this project, we will do the following:

1. Install `pip3`
2. Install `virtualenv` and activate it
3. Install all python dependencies for this project
4. Run the python script

First, we will install pip by following command: 

```shell
$ sudo apt-get install python3-pip
```

Next, we will install `virtualenv` using `pip3`, create a virtual environment, and activate the 
environment. 

```shell
$ sudo pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

Next, we will install all requirements/dependencies for this project using `pip3`.

```
$ pip3 install -r requirements.txt
```

Finally, we can view how to use each script by running the python module with the -h flag:

```shell
# Make sure you are in <project-root> folder before running the script
$ python3 visualize.py
usage: visualize.py [-h] [--pca] [--ica] [--tsne]

Process and visualization of dataset using Dimensionality Reduction Techniques
like PCA, ICA and t-SNE.

optional arguments:
  -h, --help  show this help message and exit
  --pca       Using PCA to reduce dimensions
  --ica       Using ICA to reduce dimensions
  --tsne      Using t-SNE to reduce dimensions

$ python visualize.py --pca
```

At the end of our development, we call `deactivate` in command line to deactivate `virtualenv`.

We don't install these dependecies everytime when we want to develop for this project. A normal 
workflow would be:

```shell
$ source venv/bin/activate

$ python visualize.py --pca

# When you are done
$ deactivate
```

Contributors
------------
Done by [Liu Zhemin](https://github.com/LZhemin) for academic year 2017-2018

