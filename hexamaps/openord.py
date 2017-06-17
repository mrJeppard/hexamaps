"""OpenOrd layout algorithm execution."""

from igraph import Graph
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import networkx as nx
import scipy.stats
import time


def na_complain(X):
    """Raise a value error if any nan's are found in given matrix."""
    na_values_present = np.isnan(X).sum()
    if na_values_present:
        raise ValueError("Na's found in data matrix.")


def rank_transform(X):
    """Perform a rank transform on a data matrix."""
    return np.apply_along_axis(scipy.stats.rankdata, 0, X)


def make_adjacency_matrix(X, metric="correlation", n_neighbors=6, n_jobs=1):
    """Make a graph representation out of the rows of a matrix."""
    knn = NearestNeighbors(n_neighbors=n_neighbors,
                           metric=metric,
                           algorithm="brute",
                           n_jobs=n_jobs,
                           ).fit(X)

    adjacency_matrix = knn.kneighbors_graph(X,
                                            mode="distance",
                                            ).toarray()

    return adjacency_matrix


def get_edges_and_weights(nx_edgelist):
    """Unpack a networkx edgelist into lists of edges and weights."""
    def unpack(v1, v2, edge):
        # (1 - weight) turns distance into similarity.
        return (v1, v2), 1 - edge["weight"]

    edges_weights = [unpack(v1, v2, edge) for v1, v2, edge in nx_edgelist]
    edges, weights = zip(*edges_weights)
    return list(edges), list(weights)


def transform_from_edgefile(filename, seed=None, dim=2):
    """Produce point positions from an edgefile."""
    g = Graph.Read_Ncol(filename)

    layout = g.layout_drl(seed=seed,
                          dim=dim,
                          )

    xy = pd.DataFrame(vars(layout)["_coords"], index=g.vs["name"])

    return xy


class OpenOrd(object):
    """Sklearn like interface to openOrd layout algorithm."""

    def __init__(self, n_neighbors=6, dim=2, seed=None, n_jobs=1):
        """Set the parameters for the algorithm."""
        self.n_neighbors = n_neighbors
        self.dim = dim
        self.seed = seed
        self.n_jobs = n_jobs

    def fit_transform(self, X):
        """Produce XY placement for rows of X."""
        using_pandas = type(X) == pd.core.frame.DataFrame

        if using_pandas:
            df = X
            X = X.as_matrix()

        na_complain(X)

        X = rank_transform(X)

        """
        print "starting graph construction"
        t = time.time()
        """

        adjacency_matrix = make_adjacency_matrix(X,
                                                 n_neighbors=self.n_neighbors,
                                                 n_jobs=self.n_jobs
                                                 )
        # print "adj mat complete in: " + str( (time.time() - t) / 60)
        # Take advantage of networkx sparse matrix construction
        g = nx.from_numpy_matrix(adjacency_matrix)
        edges, weights = get_edges_and_weights(nx.to_edgelist(g))
        g = Graph(edges=edges, edge_attrs={"weights": weights})

        """
        print "finished graph construction in " + str((time.time() - t)/60)
        print "starting drl"
        t = time.time()
        """

        layout = g.layout_drl(seed=self.seed,
                              dim=self.dim,
                              weights="weights"
                              )

        # print "finished drl in " + str( (time.time() - t)/60)
        # Format the output.
        if using_pandas:
            xys = pd.DataFrame(vars(layout)["_coords"],
                               index=df.index,
                               )
        else:
            xys = vars(layout)["_coords"]

        return xys
