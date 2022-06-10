#!/usr/bin/python
# Classification (U)

"""Program:  rpt_mst_log.py

    Description:  Unit testing of rpt_mst_log in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/rpt_mst_log.py

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
import lib.gen_libs as gen_libs
import mysql_rep_admin
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__
        get_log_info
        get_name

    """

    def __init__(self, gtid_mode="ON"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Server_Name"
        self.fname = "Master_Log_Name"
        self.gtid_mode = gtid_mode
        self.exe_gtid = 12345678
        self.log_pos = 2345

    def get_log_info(self):

        """Method:  get_log_info

        Description:  Stub method holder for MasterRep.get_log_info.

        Arguments:

        """

        return self.fname, self.log_pos

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for MasterRep.get_name.

        Arguments:

        """

        return self.name


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_master
        test_gtid
        test_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.results = {
            "MasterLog": {
                "LogPosition": 2345, "Master": "Server_Name",
                "MasterLog": "Master_Log_Name"}}
        self.results2 = {
            "MasterLog": {
                "GTIDPosition": 12345678, "LogPosition": 2345,
                "Master": "Server_Name", "MasterLog": "Master_Log_Name"}}
        self.results3 = {"MasterLog": {}}

    def test_no_master(self):

        """Function:  test_no_master

        Description:  Test with no master present.

        Arguments:

        """

        with gen_libs.no_std_out():
            data=mysql_rep_admin.rpt_mst_log(master=None)

        self.assertEqual(data, self.results3)

    def test_gtid(self):

        """Function:  test_gtid

        Description:  Test with GTID setting.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.rpt_mst_log(master=self.master), self.results2)

    def test_default(self):

        """Function:  test_default

        Description:  Test with default settings.

        Arguments:

        """

        self.master.gtid_mode = None

        self.assertEqual(
            mysql_rep_admin.rpt_mst_log(master=self.master), self.results)


if __name__ == "__main__":
    unittest.main()
