# Classification (U)

"""Program:  chk_slv.py

    Description:  Unit testing of chk_slv in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

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
        get_log_info
        get_name

    """

    def __init__(self, gtid_mode="ON", mst_file="FileName",
                 relay_file="FileName", read_pos=3456, exec_pos=4567):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Server_Name"
        self.mst_file = mst_file
        self.relay_file = relay_file
        self.read_pos = read_pos
        self.exec_pos = exec_pos
        self.gtid_mode = gtid_mode
        self.retrieved_gtid = 12345678
        self.exe_gtid = 23456789

    def get_log_info(self):

        """Method:  get_log_info

        Description:  Stub method holder for SlaveRep.get_log_info.

        Arguments:

        """

        return self.mst_file, self.relay_file, self.read_pos, self.exec_pos

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
        test_chk_slv_lag_gtid
        test_chk_slv_lag
        test_chk_slv_ok

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.results = {"Name": "Server_Name", "Status": "OK"}
        self.results2 = {
            "Name": "Server_Name",
            "Status": "Warning:  Slave might be lagging in execution of log",
            "Info": {
                "ReadLog": "FileName",
                "ReadPosition": 3456, "ExecLog": "FileName",
                "ExecPosition": 4567}}
        self.results3 = {
            "Name": "Server_Name",
            "Status": "Warning:  Slave might be lagging in execution of log",
            "Info": {
                "ReadLog": "FileName",
                "ReadPosition": 3456, "ExecLog": "FileName",
                "ExecPosition": 4567,
                "RetrievedGTID": 12345678, "ExecutedGTID": 23456789}}

    def test_chk_slv_lag_gtid(self):

        """Function:  test_chk_slv_lag_gtid

        Description:  Test with slave with lag problem with GTID mode.

        Arguments:

        """

        slave = SlaveRep()

        self.assertEqual(mysql_rep_admin.chk_slv(slave), self.results3)

    def test_chk_slv_lag(self):

        """Function:  test_chk_slv_lag

        Description:  Test with slave with lag problem.

        Arguments:

        """

        slave = SlaveRep()
        slave.gtid_mode = None

        self.assertEqual(mysql_rep_admin.chk_slv(slave), self.results2)

    def test_chk_slv_ok(self):

        """Function:  test_chk_slv_ok

        Description:  Test with slave with OK status.

        Arguments:

        """

        slave = SlaveRep(read_pos=4567)

        self.assertEqual(mysql_rep_admin.chk_slv(slave), self.results)


if __name__ == "__main__":
    unittest.main()
