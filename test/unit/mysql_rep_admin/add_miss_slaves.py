#!/usr/bin/python
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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.
        show_slv_hosts -> Stub method holder for MasterRep.show_slv_hosts.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.name = "Master_Name"
        self.slv_hosts = [{"Host": "slave1"}, {"Host": "slave2"},
                          {"Host": "slave3"}]

    def show_slv_hosts(self):

        """Method:  show_slv_hosts

        Description:  Stub method holder for SlaveRep.get_err_stat.

        Arguments:

        """

        return self.slv_hosts


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Initialize testing environment.
        test_no_slv_miss -> Test with no slave missing.
        test_one_slv_miss -> Test with one slave missing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.outdata = {"Slaves": [{"Name": "slave1", "Lag_Time": None},
                                   {"Name": "slave2", "Lag_Time": None}]}
        self.outdata2 = {"Slaves": [{"Name": "slave1", "Lag_Time": None},
                                    {"Name": "slave2", "Lag_Time": None},
                                    {"Name": "slave3", "Lag_Time": None}]}
        self.final_list = {"Slaves": [{"Name": "slave1", "Lag_Time": None},
                                      {"Name": "slave2", "Lag_Time": None},
                                      {"Name": "slave3", "Lag_Time": None}]}

    def test_no_slv_miss(self):

        """Function:  test_no_slv_miss

        Description:  Test with no slave missing.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.add_miss_slaves(self.master,
                                                         self.outdata2),
                         self.final_list)

    def test_one_slv_miss(self):

        """Function:  test_one_slv_miss

        Description:  Test with one slave missing.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.add_miss_slaves(self.master,
                                                         self.outdata),
                         self.final_list)


if __name__ == "__main__":
    unittest.main()
