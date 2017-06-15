#!/usr/bin/env python2.7
"""This holds methods for reading in data."""

import pandas as pd


def tabfile(filename):
    """
    Read a tab delimited file into a pandas dataframe.

    :param filename: path to tab separated matrix
    :return:
    """
    return pd.read_table(filename, index_col=0)
