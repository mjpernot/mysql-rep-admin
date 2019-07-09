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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, gtid_mode="ON"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.gtid_mode = gtid_mode


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.
        get_log_info -> Stub method holder for SlaveRep.get_log_info.
        get_name -> Stub method holder for SlaveRep.get_name.

    """

    def __init__(self, gtid_mode="ON"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.name = "Server_Name"
        self.mst_file = "Master_Log_Name"
        self.relay_file = "Slave_Relay_Name"
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

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Initialize testing environment.
        test_no_slaves -> Test no slaves present.
        test_rpt_slv_log -> Test rpt_slv_log method.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.master = MasterRep()

    def test_no_slaves(self):

        """Function:  test_no_slaves

        Description:  Test no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.rpt_slv_log(self.master, []))

    def test_rpt_slv_log(self):

        """Function:  test_rpt_slv_log

        Description:  Test rpt_slv_log method.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.rpt_slv_log(self.master,
                                                         [self.slave]))


if __name__ == "__main__":
    unittest.main()
