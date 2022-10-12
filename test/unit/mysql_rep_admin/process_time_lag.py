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
import mysql_rep_admin
import version

__version__ = version.__version__


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_time
        upd_slv_time

    """

    def __init__(self, lag_time=1, conn="Connection Instance"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.lag_time = lag_time
        self.conn = conn

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
        setUp
        test_mysql_down_std
        test_mysql_down_json
        test_lag_one2
        test_lag_one
        test_lag_zero
        test_lag_none
        test_lag_json
        test_no_lag

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.slave2 = SlaveRep(lag_time=None)
        self.slave3 = SlaveRep(lag_time=0)
        self.slave4 = SlaveRep(lag_time=None, conn=None)
        self.time_lag0 = 0
        self.time_lag1 = 1
        self.time_lag2 = None

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_mysql_down_std(self):

        """Function:  test_mysql_down_std

        Description:  Test with MySQL is down in standard format.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave4, self.time_lag2),
            self.time_lag2)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_mysql_down_json(self):

        """Function:  test_mysql_down_json

        Description:  Test with MySQL is down in JSON format.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave4, self.time_lag2),
            self.time_lag2)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_one2(self):

        """Function:  test_lag_one2

        Description:  Test with time lag set to one and then clears.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave3, self.time_lag1),
            self.time_lag0)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_one(self):

        """Function:  test_lag_one

        Description:  Test with time lag set to one.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave, self.time_lag1),
            self.time_lag1)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_zero(self):

        """Function:  test_lag_zero

        Description:  Test with time lag set to zero.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave, self.time_lag0),
            self.time_lag0)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_none(self):

        """Function:  test_lag_none

        Description:  Test with time lag set to None.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave2, self.time_lag2),
            self.time_lag2)

    @mock.patch("time.sleep", mock.Mock(return_value=True))
    def test_lag_json(self):

        """Function:  test_lag_json

        Description:  Test with time lag to JSON.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave, self.time_lag1),
            self.time_lag1)

    def test_no_lag(self):

        """Function:  test_no_lag

        Description:  Test with no time lag.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._process_time_lag(self.slave, self.time_lag0),
            self.time_lag0)


if __name__ == "__main__":
    unittest.main()
