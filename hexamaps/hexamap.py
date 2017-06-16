#!/usr/bin/env python2.7
"""The hexamap class dispatches methods used in the Tumor Map pipeline."""


class Hexamap(object):
    """This object is a jumping point for relevant methods."""

    def __init__(self, data=None, attributes=None):
        """
        Intialize the class.

        :param data:  Pandas Dataframe, Feature X Sample matrix.
        :param attributes:  Pandas Dataframe, Sample X Attribute matrix.
        :return: A instance of Hexamap class.
        """
        self.data = data
        self.attributes = attributes
        self.points = None

    def get_attribute_ids(self):
        """Get all attribute ids."""
        return self.attributes.columns.to_list()

    def set_data_nas_with_0(self):
        """Put 0 in place of "NA" values in the data matrix."""
        data_df = self.data
        data_df = data_df.fillna(0)
        self.data = data_df

    def set_data_nas_with_col_median(self):
        """Put 0 in place of "NA" values in the data matrix."""
        data_df = self.data
        medians = data_df.median()
        data_df = data_df.fillna(medians)
        self.data = data_df

    def data_inspection(self):
        """
        Summarizes common gatchas with clustering data.

        :return: None. Writes out complaints to logger.
        """
        return None

    def run_drl(self, **kwargs):
        """Perform Clustering on the data."""
        return None

    def run_tsne(self, **kwargs):
        """Perform Clustering on the data."""
        return None

    def allbyall_stats(self):
        """Run all by all stat tests on attributes."""
        return None

    def single_stats(self, attributeid):
        """Run one by all on attributes."""
        return None

    def allbyall_sca(self):
        """Run all by all spatial correlation analysis on attributes."""
        return None

    def onebyall_sca(self, attributeid):
        """Run one by all leesL."""
        return None

    def all_density(self):
        """Find density of all attributes."""
        return None

    def one_density(self, attributeid):
        """Density of single attribute."""
        return None

    def allbyall_similarity(self, method="spearman"):
        """Run all by all similarity."""
        return None

    def onebyall_similarity(self, method="spearman"):
        """Run one by all similarity."""
        return None

    def _datatype_determination(self):
        attr_df = self.attributes
