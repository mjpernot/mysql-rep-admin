#!/usr/bin/python
# Classification (U)

"""Program:  is_time_lag.py

    Description:  Unit testing of is_time_lag in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/is_time_lag.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_missing_slave
        test_time_lag_multiple_slaves3
        test_time_lag_multiple_slaves2
        test_time_lag_multiple_slaves
        test_time_lag_single_slave
        test_no_time_lag_multiple_slaves
        test_no_time_lag_single_slave

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 0}]}}]}
        self.data2 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 0},
                               {"Name": "slave2", "LagTime": 0}]}}]}
        self.data3 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 1}]}}]}
        self.data4 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 1},
                               {"Name": "slave2", "LagTime": 0}]}}]}
        self.data5 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 0},
                               {"Name": "slave2", "LagTime": 1}]}}]}
        self.data6 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 1},
                               {"Name": "slave2", "LagTime": 1}]}}]}
        self.data7 = {
            "Checks": [{
                "CheckSlaveTime": {
                    "Slaves": [{"Name": "slave1", "LagTime": 0},
                               {"Name": "slave2", "LagTime": None}]}}]}

    def test_missing_slave(self):

        """Function:  test_missing_slave

        Description:  Test with missing slave.

        Arguments:

        """

        self.assertTrue(mysql_rep_admin.is_time_lag(self.data7))

    def test_time_lag_multiple_slaves3(self):

        """Function:  test_time_lag_multiple_slaves3

        Description:  Test with time lag with multiple slaves.

        Arguments:

        """

        self.assertTrue(mysql_rep_admin.is_time_lag(self.data6))

    def test_time_lag_multiple_slaves2(self):

        """Function:  test_time_lag_multiple_slaves2

        Description:  Test with time lag with multiple slaves.

        Arguments:

        """

        self.assertTrue(mysql_rep_admin.is_time_lag(self.data5))

    def test_time_lag_multiple_slaves(self):

        """Function:  test_time_lag_multiple_slaves

        Description:  Test with time lag with multiple slaves.

        Arguments:

        """

        self.assertTrue(mysql_rep_admin.is_time_lag(self.data4))

    def test_time_lag_single_slave(self):

        """Function:  test_time_lag_single_slave

        Description:  Test with time lag with single slave.

        Arguments:

        """

        self.assertTrue(mysql_rep_admin.is_time_lag(self.data3))

    def test_no_time_lag_multiple_slaves(self):

        """Function:  test_no_time_lag_multiple_slaves

        Description:  Test with no time lag with multiple slaves.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin.is_time_lag(self.data2))

    def test_no_time_lag_single_slave(self):

        """Function:  test_no_time_lag_single_slave

        Description:  Test with no time lag with single slave.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin.is_time_lag(self.data))


if __name__ == "__main__":
    unittest.main()
