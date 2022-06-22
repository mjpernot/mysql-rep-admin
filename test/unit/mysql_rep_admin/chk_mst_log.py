#!/usr/bin/python
# Classification (U)

"""Program:  chk_mst_log.py

    Description:  Unit testing of chk_mst_log in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_mst_log.py

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

    Methods:
        __init__
        get_log_info

    """

    def __init__(self, gtid_mode="ON", fname="Master_Log2", log_pos=5678):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Master_Name"
        self.gtid_mode = gtid_mode
        self.fname = fname
        self.log_pos = log_pos

    def get_log_info(self):

        """Method:  get_log_info

        Description:  Stub method holder for SlaveRep.get_log_info.

        Arguments:

        """

        return self.fname, self.log_pos


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_log_info
        get_name

    """

    def __init__(self, gtid_mode="ON", mst_file="Master_Log",
                 relay_file="Slave_Relay", read_pos=3456, exec_pos=4567):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave_Name"
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
        test_no_present
        test_slv_present
        test_mst_slv_present_lag
        test_mst_slv_present_ok

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave2 = SlaveRep(mst_file="Master_Log2", read_pos=5678)
        self.slave = SlaveRep()
        self.chk_slv_data = {"Name": "SlaveName", "Status": "OK"}
        self.results = {"CheckMasterLog": {"MasterLog": {}, "SlaveLogs": []}}
        self.results2 = {
            "CheckMasterLog": {
                "MasterLog": {}, "SlaveLogs": [
                    {"Name": "SlaveName", "Status": "OK"}]}}
        self.results3 = {
            "CheckMasterLog": {
                "MasterLog": {
                    "Master": {
                        "Name": "Master_Name", "Log": "Master_Log2",
                        "Position": 5678},
                    "Slaves":
                        [{"Name": "Slave_Name",
                          "Info": {"Position": 3456, "Log": "Master_Log"},
                          "Status": "Warning:  Slave lagging in reading \
master log"}]},
                "SlaveLogs": [{"Name": "SlaveName", "Status": "OK"}]}}
        self.results4 = {
            "CheckMasterLog": {
                "MasterLog": {
                    "Master": {
                        "Name": "Master_Name", "Log": "Master_Log2",
                        "Position": 5678},
                    "Slaves": [{"Name": "Slave_Name", "Status": "OK"}]},
                "SlaveLogs": [{"Name": "SlaveName", "Status": "OK"}]}}

    def test_no_present(self):

        """Function:  test_no_present

        Description:  Test with no master or slave present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_admin.chk_mst_log(
                    master=None, slaves=[]), self.results)

    @mock.patch("mysql_rep_admin.chk_slv")
    def test_slv_present(self, mock_chk):

        """Function:  test_slv_present

        Description:  Test with slave only present.

        Arguments:

        """

        mock_chk.return_value = [dict(self.chk_slv_data)]

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_admin.chk_mst_log(
                    master=None, slaves=[self.slave]), self.results2)

    @mock.patch("mysql_rep_admin.chk_slv")
    def test_mst_slv_present_lag(self, mock_chk):

        """Function:  test_mst_slv_present_lag

        Description:  Test with master and slave present with lag.

        Arguments:

        """

        mock_chk.return_value = [dict(self.chk_slv_data)]

        self.assertEqual(
            mysql_rep_admin.chk_mst_log(
                master=self.master, slaves=[self.slave]), self.results3)

    @mock.patch("mysql_rep_admin.chk_slv")
    def test_mst_slv_present_ok(self, mock_chk):

        """Function:  test_mst_slv_present_ok

        Description:  Test with master and slave present with no lag.

        Arguments:

        """

        mock_chk.return_value = [dict(self.chk_slv_data)]

        self.assertEqual(
            mysql_rep_admin.chk_mst_log(
                master=self.master, slaves=[self.slave2]), self.results4)


if __name__ == "__main__":
    unittest.main()
