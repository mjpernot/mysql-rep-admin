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
import unittest
import mock

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


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_time
        get_name
        upd_slv_time
        is_connected

    """

    def __init__(self, lag_time=1, conn="Connection Instance"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.lag_time = lag_time
        self.name = "Slave_Name"
        self.slave_uuid = "1"
        self.conn = conn
        self.connected = True

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

    def is_connected(self):

        """Method:  is_connected

        Description:  Stub method holder for SlaveRep.is_connected.

        Arguments:

        """

        return self.connected


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_down_slv
        test_no_slv
        test_json
        test_no_lag

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.results = {
            "CheckSlaveTime": {
                "Slaves": [
                    {'LagTime': 'DOWN', 'Slave_UUID': '1',
                     'Name': 'Slave_Name'}]}}
        self.results2 = {
            "CheckSlaveTime": {
                "Slaves": [
                    {'LagTime': 0, 'Slave_UUID': '1', 'Name': 'Slave_Name'}]}}
        self.results3 = {
            "CheckSlaveTime": {
                "Slaves": [
                    {'LagTime': 1, 'Slave_UUID': '1', 'Name': 'Slave_Name'}]}}

    @mock.patch("mysql_rep_admin.add_miss_slaves", mock.Mock(return_value=[]))
    def test_down_slv(self):

        """Function:  test_down_slv

        Description:  Test with down slave.

        Arguments:

        """

        self.slave.isconnected = False

        self.assertEqual(
            mysql_rep_admin.chk_slv_time(
                master=self.master, slaves=[self.slave]), self.results)

    @mock.patch("mysql_rep_admin.add_miss_slaves", mock.Mock(return_value=[]))
    def test_no_slv(self):

        """Function:  test_no_slv

        Description:  Test with no slaves present.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.chk_slv_time(
                master=self.master, slaves=[]), self.results)

    @mock.patch("mysql_rep_admin.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.add_miss_slaves", mock.Mock(return_value=[]))
    def test_lag(self):

        """Function:  test_lag

        Description:  Test with time lag.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.chk_slv_time(
                master=self.master, slaves=[self.slave]), self.results3)

    @mock.patch("mysql_rep_admin.time.sleep", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.add_miss_slaves", mock.Mock(return_value=[]))
    def test_no_lag(self):

        """Function:  test_std_no_lag

        Description:  Test with no time lag.

        Arguments:

        """

        self.slave = SlaveRep(lag_time=0)

        self.assertEqual(
            mysql_rep_admin.chk_slv_time(
                master=self.master, slaves=[self.slave]), self.results2)


if __name__ == "__main__":
    unittest.main()
