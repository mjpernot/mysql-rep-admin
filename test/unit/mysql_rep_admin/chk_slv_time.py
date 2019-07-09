#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_time.py

    Description:  Unit testing of chk_slv_time in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv_time.py

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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.name = "Master_Name"


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.
        get_time -> Stub method holder for SlaveRep.get_time.
        get_name -> Stub method holder for SlaveRep.get_name.
        upd_slv_time -> Stub method holder for SlaveRep.upd_slv_time.

    """

    def __init__(self, lag_time=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.lag_time = lag_time
        self.name = "Slave_Name"

    def get_time(self):

        """Method:  get_time

        Description:  Stub method holder for SlaveRep.get_time.

        Arguments:

        """

        return self.lag_time

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for SlaveRep.get_name.

        Arguments:

        """

        return self.name

    def upd_slv_time(self):

        """Method:  upd_slv_time

        Description:  Stub method holder for SlaveRep.upd_slv_time.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Initialize testing environment.
        test_no_slv -> Test with no slaves present.
        test_json -> Test with JSON format.
        test_std_no_lag -> Test standard out with no time lag.
        test_std_out -> Test standard out.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()

    def test_no_slv(self):

        """Function:  test_no_slv

        Description:  Test with no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_time(self.master, []))

    @mock.patch("mysql_rep_admin.mongo_libs.json_prt_ins_2_db")
    @mock.patch("mysql_rep_admin.add_miss_slaves")
    @mock.patch("mysql_rep_admin.time.sleep")
    def test_json(self, mock_sleep, mock_miss, mock_mongo):

        """Function:  test_json

        Description:  Test with JSON format.

        Arguments:

        """

        mock_sleep.return_value = True
        mock_miss.return_value = True
        mock_mongo.return_value = True

        self.assertFalse(mysql_rep_admin.chk_slv_time(self.master,
                                                      [self.slave],
                                                      form="JSON"))

    @mock.patch("mysql_rep_admin.time.sleep")
    def test_std_no_lag(self, mock_sleep):

        """Function:  test_std_no_lag

        Description:  Test standard out with no time lag.

        Arguments:

        """

        mock_sleep.return_value = True
        self.slave = SlaveRep(lag_time=None)        

        self.assertFalse(mysql_rep_admin.chk_slv_time(self.master,
                                                      [self.slave]))

    @mock.patch("mysql_rep_admin.time.sleep")
    def test_std_out(self, mock_sleep):

        """Function:  test_std_out

        Description:  Test standard out.

        Arguments:

        """

        mock_sleep.return_value = True

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_time(self.master,
                                                          [self.slave]))


if __name__ == "__main__":
    unittest.main()
