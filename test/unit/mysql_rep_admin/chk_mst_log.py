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
        __init__ -> Class initialization.
        get_log_info -> Stub method holder for MasterRep.get_log_info.

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
        __init__ -> Class initialization.
        get_log_info -> Stub method holder for SlaveRep.get_log_info.
        get_name -> Stub method holder for SlaveRep.get_name.

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
        setUp -> Initialize testing environment.
        test_no_present -> Test with no master or slave present.
        test_slv_present -> Test with slave only present.
        test_mst_slv_present -> Test with master and slave present.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()

    def test_no_present(self):

        """Function:  test_no_present

        Description:  Test with no master or slave present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_mst_log(None, []))

    @mock.patch("mysql_rep_admin.chk_slv")
    def test_slv_present(self, mock_chk):

        """Function:  test_slv_present

        Description:  Test with slave only present.

        Arguments:

        """

        mock_chk.return_value = True

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_mst_log(None, [self.slave]))

    @mock.patch("mysql_rep_admin.chk_slv")
    def test_mst_slv_present(self, mock_chk):

        """Function:  test_mst_slv_present

        Description:  Test with master and slave present.

        Arguments:

        """

        mock_chk.return_value = True

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_mst_log(self.master,
                                                         [self.slave]))


if __name__ == "__main__":
    unittest.main()
