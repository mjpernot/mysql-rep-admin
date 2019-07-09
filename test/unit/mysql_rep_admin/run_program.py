#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/run_program.py

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


def rpt_slv_log(master, slaves, form, ofile, db_tbl, class_cfg):

    """Method:  rpt_slv_log

    Description:  Function stub holder for mysql_rep_admin.rpt_slv_log.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder
        form -> Stub holder
        ofile -> Stub holder
        db_tbl -> Stub holder
        class_cfg -> Stub holder

    """

    return True


class MstCfg(object):

    """Class:  MstCfg

    Description:  Class stub holder for gen_libs.load_module class.

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

        self.name = "MasterName"
        self.sid = 11
        self.user = "UserName"
        self.passwd = "pwd"
        self.server_os = "Linux"
        self.host = "HostName"
        self.port = 3306
        self.cfg_file = "CfgFile"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Initialize testing environment.
        test_single_func -> Test with single function call.
        test_argsarray_all -> Test with all option in args_array.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mstcfg = MstCfg()
        self.func_dict = {"-D": rpt_slv_log}
        self.args_array = {"-D": True, "-m": "Mongo", "-d": "cfg"}
        self.cfg_array = [{"name": "HOST_NAME", "passwd": "PWD",
                           "cfg_file": "None", "host": "SERVER",
                           "user": "root", "serv_os": "Linux", "sid": "11",
                           "port": "3306"},
                          {"name": "HOST_NAME2", "passwd": "PWD",
                           "cfg_file": "None", "host": "SERVER2",
                           "user": "root", "serv_os": "Linux", "sid": "21",
                           "port": "3306"}]

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect")
    @mock.patch("mysql_rep_admin.call_run_chk")
    @mock.patch("mysql_rep_admin.cmds_gen.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_single_func(self, mock_cfg, mock_array, mock_call, mock_dis):

        """Function:  test_single_func

        Description:  Test with single function call.

        Arguments:

        """

        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_call.return_value = True
        mock_dis.return_value = True

        self.assertFalse(mysql_rep_admin.run_program(self.args_array,
                                                      self.func_dict))


if __name__ == "__main__":
    unittest.main()
