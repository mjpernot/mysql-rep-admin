#!/usr/bin/python
# Classification (U)

"""Program:  process_time_lag.py

    Description:  Unit testing of process_time_lag in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/process_time_lag.py

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
import mock

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
        __init__ -> Class initialization.
        get_time -> Stub method holder for SlaveRep.get_time.
        upd_slv_time -> Stub method holder for SlaveRep.upd_slv_time.

    """

    def __init__(self, lag_time=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.lag_time = lag_time

    def get_time(self):

        """Method:  get_time

        Description:  Stub method holder for SlaveRep.get_time.

        Arguments:

        """

        return self.lag_time

    def upd_slv_time(self):

        """Method:  upd_slv_time

        Description:  Stub method holder for SlaveRep.upd_slv_time.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_lag_json -> Test with time lag to JSON.
        test_lag_stdout -> Test with time lag to standard out.
        test_no_lag -> Test with no time lag.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.name = "SlaveName"
        self.frmt = "standard"
        self.frmt2 = "JSON"
        self.time_lag0 = 0
        self.time_lag1 = 1

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_json(self):

        """Function:  test_lag_json

        Description:  Test with time lag to JSON.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_time_lag(
            self.slave, self.time_lag1, self.name, self.frmt2))

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_stdout(self):

        """Function:  test_lag_stdout

        Description:  Test with time lag to standard out.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin._process_time_lag(
                self.slave, self.time_lag1, self.name, self.frmt))

    def test_no_lag(self):

        """Function:  test_no_lag

        Description:  Test with no time lag.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_time_lag(
            self.slave, self.time_lag0, self.name, self.frmt))


if __name__ == "__main__":
    unittest.main()
