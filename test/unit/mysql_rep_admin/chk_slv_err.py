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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Master_Name"


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.
        get_err_stat -> Stub method holder for SlaveRep.get_err_stat.
        get_name -> Stub method holder for SlaveRep.get_name.

    """

    def __init__(self, ios="Error", sql="Error", conn="Connection"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave_Name"
        self.io = ios
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

        return self.io, self.sql, self.io_msg, self.sql_msg, self.io_time, \
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
        setUp -> Initialize testing environment.
        test_no_conn -> Test with no connection.
        test_sql_error -> Test with sql error present.
        test_io_error -> Test with io error present.
        test_no_slv_present -> Test with no slaves present.
        test_no_error -> Test with no errors present.
        test_iosql_error -> Test with io and sql errors present.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.slave2 = SlaveRep(ios=None, sql=None)
        self.slave3 = SlaveRep(sql=None)
        self.slave4 = SlaveRep(ios=None)
        self.slave5 = SlaveRep(ios=None, sql=None, conn=None)

    def test_no_conn(self):

        """Function:  test_no_conn

        Description:  Test with no connection.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_err(self.master,
                                                         [self.slave5]))

    def test_sql_error(self):

        """Function:  test_sql_error

        Description:  Test with sql error present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_err(self.master,
                                                         [self.slave4]))

    def test_io_error(self):

        """Function:  test_io_error

        Description:  Test with io error present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_err(self.master,
                                                         [self.slave3]))

    def test_no_slv_present(self):

        """Function:  test_no_slv_present

        Description:  Test with no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_err(self.master, []))

    def test_no_error(self):

        """Function:  test_no_error

        Description:  Test with no errors present.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin.chk_slv_err(self.master,
                                                     [self.slave2]))

    def test_iosql_error(self):

        """Function:  test_iosql_error

        Description:  Test with io and sql errors present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_err(self.master,
                                                         [self.slave]))


if __name__ == "__main__":
    unittest.main()
