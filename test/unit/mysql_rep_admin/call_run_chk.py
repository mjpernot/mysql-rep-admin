#!/usr/bin/python
# Classification (U)

"""Program:  call_run_chk.py

    Description:  Unit testing of call_run_chk in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/call_run_chk.py

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


def chk_mst_log(master, slaves, form, ofile, db_tbl, class_cfg):

    """Method:  chk_mst_log

    Description:  Function stub holder for mysql_rep_admin.chk_mst_log.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder
        form -> Stub holder
        ofile -> Stub holder
        db_tbl -> Stub holder
        class_cfg -> Stub holder

    """

    return True


def chk_slv_thr(master, slaves, form, ofile, db_tbl, class_cfg):

    """Method:  chk_slv_thr

    Description:  Function stub holder for mysql_rep_admin.chk_slv_thr.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder
        form -> Stub holder
        ofile -> Stub holder
        db_tbl -> Stub holder
        class_cfg -> Stub holder

    """

    return True


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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

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

        self.name = "Master_Name"


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

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

        self.name = "Slave_Name"


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

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.func_dict = {"-A": ["-C", "-S"], "-C": chk_mst_log,
                          "-S": chk_slv_thr, "-D": rpt_slv_log}
        self.args_array = {"-A": True, "-D": True}
        self.args_array2 = {"-D": True}

    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_single_func(self, mock_cfg):

        """Function:  test_single_func

        Description:  Test with single function call.

        Arguments:

        """

        mock_cfg.return_value = "MongoCfg"

        self.assertFalse(mysql_rep_admin.call_run_chk(self.args_array,
                                                      self.func_dict,
                                                      self.master,
                                                      [self.slave]))

    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_argsarray_all(self, mock_cfg):

        """Function:  test_argsarray_all

        Description:  Test with all option in args_array.

        Arguments:

        """

        mock_cfg.return_value = "MongoCfg"

        self.assertFalse(mysql_rep_admin.call_run_chk(self.args_array,
                                                      self.func_dict,
                                                      self.master,
                                                      [self.slave]))


if __name__ == "__main__":
    unittest.main()
