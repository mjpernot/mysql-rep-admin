#!/usr/bin/python
# Classification (U)

"""Program:  rpt_mst_log.py

    Description:  Unit testing of rpt_mst_log in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/rpt_mst_log.py

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

    Methods:
        __init__ -> Class initialization.
        get_log_info -> Stub method holder for MasterRep.get_log_info.
        get_name -> Stub method holder for MasterRep.get_name.

    """

    def __init__(self, gtid_mode="ON"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Server_Name"
        self.fname = "Master_Log_Name"
        self.gtid_mode = gtid_mode
        self.exe_gtid = 12345678
        self.log_pos = 2345

    def get_log_info(self):

        """Method:  get_log_info

        Description:  Stub method holder for MasterRep.get_log_info.

        Arguments:

        """

        return self.fname, self.log_pos

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for MasterRep.get_name.

        Arguments:

        """

        return self.name


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, gtid_mode="ON"):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = gtid_mode


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_master -> Test no master present.
        test_rpt_mst_log -> Test rpt_msg_log method.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.master = MasterRep()

    def test_no_master(self):

        """Function:  test_no_master

        Description:  Test no master present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.rpt_mst_log(None, [self.slave]))

    def test_rpt_mst_log(self):

        """Function:  test_rpt_mst_log

        Description:  Test rpt_msg_log method.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.rpt_mst_log(self.master,
                                                         [self.slave]))


if __name__ == "__main__":
    unittest.main()
