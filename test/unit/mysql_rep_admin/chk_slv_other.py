# Classification (U)

"""Program:  chk_slv_other.py

    Description:  Unit testing of chk_slv_other in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv_other.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class MasterRep():                                      # pylint:disable=R0903

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


class SlaveRep():

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_name
        get_others
        is_connected

    """

    def __init__(self, skip=1, tmp_tbl=6, retry=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.tmp_tbl = str(tmp_tbl)
        self.retry = str(retry)
        self.name = "Slave_Name"
        self.skip = skip
        self.version = (5, 6, 31)
        self.connected = True

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for SlaveRep.get_name.

        Arguments:

        """

        return self.name

    def get_others(self):

        """Method:  get_others

        Description:  Stub method holder for SlaveRep.get_others.

        Arguments:

        """

        return self.skip, self.tmp_tbl, self.retry

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
        test_no_slv
        test_chk_slv_other

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.slave2 = SlaveRep(0, 0, 0)
        self.results = {
            "CheckSlaveOther": {"Slaves": [
                {"Name": "Slave_Name", "Status": "Good"}]}}
        self.results2 = {
            "CheckSlaveOther": {"Slaves": []}}
        self.results3 = {
            "CheckSlaveOther": {"Slaves": [
                {"Name": "Slave_Name", "RetryTransactionCount": "1",
                 "SkipCount": 1, "TempTableCount": "6", "Status": "Bad"}]}}
        self.results4 = {
            "CheckSlaveOther": {"Slaves": [
                {"Name": "Slave_Name", "Status": "DOWN"}]}}

    def test_down_slave(self):

        """Function:  test_down_slave

        Description:  Test with slave being down.

        Arguments:

        """

        self.slave.connected = False

        self.assertEqual(
            mysql_rep_admin.chk_slv_other(
                master=self.master, slaves=[self.slave]), self.results4)

    def test_chk_slv_other2(self):

        """Function:  test_chk_slv_other2

        Description:  Test with no errors detected.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.chk_slv_other(
                master=self.master, slaves=[self.slave2]), self.results)

    def test_no_slv(self):

        """Function:  test_no_slv

        Description:  Test with no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_admin.chk_slv_other(master=self.master, slaves=[]),
                self.results2)

    def test_chk_slv_other(self):

        """Function:  test_chk_slv_other

        Description:  Test chk_slv_other method.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.chk_slv_other(
                master=self.master, slaves=[self.slave]), self.results3)


if __name__ == "__main__":
    unittest.main()
