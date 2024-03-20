# Classification (U)

"""Program:  add_miss_slaves.py

    Description:  Unit testing of add_miss_slaves in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/add_miss_slaves.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Master_Name"
        self.slaves = [
            {"Replica_UUID": "1"}, {"Replica_UUID": "2"},
            {"Replica_UUID": "3"}]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_slv_miss
        test_one_slv_miss

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.data = {
            "CheckSlaveTime": {
                "Slaves": [{"Slave_UUID": "1",}, {"Slave_UUID": "2",}]}}
        self.data2 = {
            "CheckSlaveTime": {
                "Slaves": [{"Slave_UUID": "1"}, {"Slave_UUID": "2"},
                           {"Slave_UUID": "3"}]}}
        self.results = [{"Slave_UUID": "3", "LagTime": "UNK"}]

    def test_no_slv_miss(self):

        """Function:  test_no_slv_miss

        Description:  Test with no slave missing.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.add_miss_slaves(self.master, self.data2), list())

    def test_one_slv_miss(self):

        """Function:  test_one_slv_miss

        Description:  Test with one slave missing.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.add_miss_slaves(self.master, self.data),
            self.results)


if __name__ == "__main__":
    unittest.main()
