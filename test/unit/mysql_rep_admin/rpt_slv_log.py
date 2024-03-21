# Classification (U)

"""Program:  rpt_slv_log.py

    Description:  Unit testing of rpt_slv_log in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/rpt_slv_log.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

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
        get_log_info
        get_name
        is_connected

    """

    def __init__(self, gtid_mode=None):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave1"
        self.mst_file = "MasterLog"
        self.relay_file = "MasterRelay"
        self.read_pos = 3456
        self.exec_pos = 4567
        self.gtid_mode = gtid_mode
        self.retrieved_gtid = 12345678
        self.exe_gtid = 23456789
        self.connected = True

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
        test_slave_down
        test_no_slaves
        test_slave
        test_gtid

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.results = {"SlaveLogs": []}
        self.results2 = {
            "SlaveLogs": [{
                "ExecPosition": 4567, "MasterFile": "MasterLog",
                "MasterPosition": 3456, "RelayFile": "MasterRelay",
                "Slave": "Slave1"}]}
        self.results3 = {
            "SlaveLogs": [{
                "ExecPosition": 4567, "MasterFile": "MasterLog",
                "MasterPosition": 3456, "RelayFile": "MasterRelay",
                "RetrievedGTID": 12345678, "Slave": "Slave1"}]}
        self.results4 = {
            "SlaveLogs": [{
                "ExecPosition": "Unknown", "MasterFile": "Unknown",
                "MasterPosition": "Unknown", "RelayFile": "Unknown",
                "Slave": "Slave1"}]}

    def test_slave_down(self):

        """Function:  test_slave_down

        Description:  Test with slave down.

        Arguments:

        """

        slave = SlaveRep()
        slave.connected = False

        self.assertEqual(
            mysql_rep_admin.rpt_slv_log(slaves=[slave]), self.results4)

    def test_no_slaves(self):

        """Function:  test_no_slaves

        Description:  Test no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_admin.rpt_slv_log(slaves=[]), self.results)

    def test_slave(self):

        """Function:  test_slave

        Description:  Test with slave present.

        Arguments:

        """

        slave = SlaveRep()

        self.assertEqual(
            mysql_rep_admin.rpt_slv_log(slaves=[slave]), self.results2)

    def test_gtid(self):

        """Function:  test_gtid

        Description:  Test with GTID present.

        Arguments:

        """

        slave = SlaveRep(gtid_mode="ON")

        self.assertEqual(
            mysql_rep_admin.rpt_slv_log(slaves=[slave]), self.results3)


if __name__ == "__main__":
    unittest.main()
