#!/usr/bin/python
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


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        get_log_info
        get_name

    """

    def __init__(self, gtid_mode="ON"):

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
        test_no_slaves
        test_rpt_slv_log

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave1 = SlaveRep()
        self.slave2 = SlaveRep()
        self.slave2.name = "Slave2"
        self.slaves = [self.slave1]
        self.slaves2 = [self.slave1, self.slave2]
        self.results = {
            "SlaveLog": [{
                "ExecPosition": 4567, "MasterFile": "MasterLog",
                "MasterPosition": 3456, "RelayFile": "MasterRelay",
                "RetrievedGTID": 12345678, "Slave": "Slave1"}]}

    def test_no_slaves(self):

        """Function:  test_no_slaves

        Description:  Test no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.rpt_slv_log(self.master, []))

# STOPPED HERE - test_two_slaves, test_gtid
    def test_one_slave(self):

        """Function:  test_one_slave

        Description:  Test with one slave.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.rpt_slv_log(slaves=self.slaves), self.results)


if __name__ == "__main__":
    unittest.main()
