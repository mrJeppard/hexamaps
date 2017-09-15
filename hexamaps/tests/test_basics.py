"""A starting point for unit tests."""

from unittest import TestCase
from hexamaps.hexamap import Hexamap
import numpy as np
from . import utils4test as utils

class Testings(TestCase):
    """Place holder running test class."""
    def test_no_dataframe_err_data(self):
        try:
            Hexamap(data=utils.random_numpy())
            passed = False
        except ValueError:
            passed =True

        self.assertTrue(passed, "Error not correctly thrown without pandas DF.")

    def test_no_dataframe_err_attr(self):
        try:
            Hexamap(attributes=utils.random_numpy())
            passed = False
        except ValueError:
            passed =True

        self.assertTrue(passed, "Error not correctly thrown without pandas DF.")

    def test_accept_pandas(self):
        try:
            Hexamap(data=utils.random_pandas(),
                    attributes=utils.random_pandas())
            passed = True
        except ValueError:
            passed =False

        self.assertTrue(passed, "Did not accept pandas DF.")