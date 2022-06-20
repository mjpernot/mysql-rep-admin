#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_err.py

    Description:  Unit testing of chk_slv_err in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv_err.py

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


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_err_stat
        get_name

    """

    def __init__(self, ios="Error", sql="Error", conn="Connection"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave_Name"
        self.ios = ios
        self.sql = sql
        self.io_msg = "IO_Message"
        self.sql_msg = "SQL_Message"
        self.io_time = "IO_Time"
        self.sql_time = "SQL_Time"
        self.conn = conn

    def get_err_stat(self):

        """Method:  get_err_stat

        Description:  Stub method holder for SlaveRep.get_err_stat.

        Arguments:

        """

        return self.ios, self.sql, self.io_msg, self.sql_msg, self.io_time, \
            self.sql_time

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for SlaveRep.get_name.

        Arguments:

        """

        return self.name


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_conn
        test_sql_error
        test_io_error
        test_no_slv_present
        test_no_error
        test_iosql_error

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """
        self.maxDiff=None
        self.slave = SlaveRep()
        self.slave2 = SlaveRep(ios=None, sql=None)
        self.slave3 = SlaveRep(sql=None)
        self.slave4 = SlaveRep(ios=None)
        self.slave5 = SlaveRep(ios=None, sql=None, conn=None)
        self.data = {"Name": self.slave.name, "Connection": "Up", "IO": {},
                     "SQL": {}}

        self.results = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}
        self.results["CheckSlaveError"]["Slaves"][0]["Connection"] = "Down"

        self.results2 = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}
        self.results2["CheckSlaveError"]["Slaves"][0]["SQL"]["Error"] = "Error"
        self.results2[
            "CheckSlaveError"]["Slaves"][0]["SQL"]["Message"] = "SQL_Message"
        self.results2[
            "CheckSlaveError"]["Slaves"][0]["SQL"]["Timestamp"] = "SQL_Time"

        self.results3 = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}

        self.results4 = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}

        self.results5 = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}

        self.results6 = {"CheckSlaveError": {"Slaves": [dict(self.data)]}}

    def test_no_conn(self):

        """Function:  test_no_conn

        Description:  Test with no connection.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[self.slave5]),
                         self.results)

    def test_sql_error(self):

        """Function:  test_sql_error

        Description:  Test with sql error present.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[self.slave4]),
                         self.results2)

# STOPPED HERE
    def test_io_error(self):

        """Function:  test_io_error

        Description:  Test with io error present.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[self.slave3]),
                         self.results)

    def test_no_slv_present(self):

        """Function:  test_no_slv_present

        Description:  Test with no slaves present.

        Arguments:

        """

        #with gen_libs.no_std_out():
        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[]), self.results)

    def test_no_error(self):

        """Function:  test_no_error

        Description:  Test with no errors present.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[self.slave2]),
                         self.results)

    def test_iosql_error(self):

        """Function:  test_iosql_error

        Description:  Test with io and sql errors present.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin.chk_slv_err(slaves=[self.slave]),
                         self.results)


if __name__ == "__main__":
    unittest.main()
