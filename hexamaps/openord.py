#!/usr/bin/env python2.7
"""Wraps igraph's openOrd implementation in a sklearn-like interface."""

from igraph import Graph
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import scipy.stats


def rank_transform(X):
    """Perform a rank transform on a dat a matrix."""
    # Complain about Na's because the rank transform silently replaces Nas
    # with a real value, which is misleading and should not be tolerated.
    na_values_present = np.isnan(X).sum()
    if na_values_present:
        raise ValueError("Na's found in data matrix.")

    return np.apply_along_axis(scipy.stats.rankdata, 0, X)


def make_adjacency_matrix(X, metric="correlation", n_neighbors=6):
    """Make a graph representation out of the rows of a matrix."""
    knn = NearestNeighbors(n_neighbors=n_neighbors,
                           metric=metric,
                           algorithm="brute"
                           ).fit(X)
    adjacency_matrix = knn.kneighbors_graph(X).toarray()
    return adjacency_matrix


class OpenOrd(object):
    """Sklearn like interface to openOrd layout algorithm."""

    def __init__(self, n_neighbors=6, dim=2, seed=None):
        """Set the parameters for the algorithm."""
        self.n_neighbors = n_neighbors
        self.dim = dim
        self.seed = seed

    def fit_transform(self, X):
        """Produce XY placement for rows of X."""
        using_pandas = type(X) == pd.core.frame.DataFrame

        if using_pandas:
            df = X
            X = X.as_matrix()

        X = rank_transform(X)
        adjacency_matrix = make_adjacency_matrix(X,
                                                 n_neighbors=self.n_neighbors
                                                 )
        # Construct graph and run layout generator.
        layout = Graph().Adjacency(adjacency_matrix.tolist()
                                   ).layout_drl(seed=self.seed,
                                                dim=self.dim)

        # Construct the output.
        if using_pandas:
            xys = pd.DataFrame(vars(layout)["_coords"],
                               index=df.index,
                               )
        else:
            xys = vars(layout)["_coords"]

        return xys
