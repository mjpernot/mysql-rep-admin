#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_thr.py

    Description:  Unit testing of chk_slv_thr in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv_thr.py

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
        get_thr_stat -> Stub method holder for SlaveRep.get_thr_stat.
        get_name -> Stub method holder for SlaveRep.get_name.

    """

    def __init__(self, thr="OFF", io_thr="OFF", sql_thr="OFF", run="OFF"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave_Name"
        self.thr = thr
        self.io_thr = io_thr
        self.sql_thr = sql_thr
        self.run = run

    def get_thr_stat(self):

        """Method:  get_thr_stat

        Description:  Stub method holder for SlaveRep.get_thr_stat.

        Arguments:

        """

        return self.thr, self.io_thr, self.sql_thr, self.run

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
        test_no_slv_present -> Test with no slaves present.
        test_sqlthr_down -> Test with sql_thr attribute set to OFF.
        test_iothr_down -> Test with io_thr attribute set to OFF.
        test_thr_run_down -> Test with thr and run attributes set to OFF.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()

    def test_no_slv_present(self):

        """Function:  test_no_slv_present

        Description:  Test with no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_thr(self.master, []))

    def test_sqlthr_down(self):

        """Function:  test_sqlthr_down

        Description:  Test with sql_thr attribute set to OFF.

        Arguments:

        """

        self.slave = SlaveRep(thr="ON", run="ON", io_thr="ON")

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_thr(self.master,
                                                         [self.slave]))

    def test_iothr_down(self):

        """Function:  test_iothr_down

        Description:  Test with io_thr attribute set to OFF.

        Arguments:

        """

        self.slave = SlaveRep(thr="ON", run="ON")

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_thr(self.master,
                                                         [self.slave]))

    def test_thr_run_down(self):

        """Function:  test_thr_run_down

        Description:  Test with thr and run attributes set to OFF.

        Arguments:

        """

        self.slave = SlaveRep()

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_thr(self.master,
                                                         [self.slave]))


if __name__ == "__main__":
    unittest.main()
