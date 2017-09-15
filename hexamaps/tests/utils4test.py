
from scipy import stats
import pandas as pd


def random_numpy(nrows=50,ncols=50,mu=0,std=1):
    '''
    :param nrows: number of rows in the 2d array
    :param ncols: number of cols in the 2d array
    :param mu:    mean for random generation
    :param std:   standard deviation for random generation
    :return: returns a random 2d numpy array, generated with normal distribution
    '''

    return stats.norm.rvs(loc=mu, scale=std, size=(nrows,ncols))

def random_pandas():
    return pd.DataFrame(random_numpy())