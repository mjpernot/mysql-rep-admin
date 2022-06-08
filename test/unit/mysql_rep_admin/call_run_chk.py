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
import mysql_rep_admin
import version

__version__ = version.__version__


def chk_mst_log(master, slaves, **kwargs):

    """Method:  chk_mst_log

    Description:  Function stub holder for mysql_rep_admin.chk_mst_log.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder

    """

    status = True
    json_fmt = kwargs.get("json_fmt", None)

    if master and slaves and json_fmt:
        status = True

    return status


def chk_slv_thr(master, slaves, **kwargs):

    """Method:  chk_slv_thr

    Description:  Function stub holder for mysql_rep_admin.chk_slv_thr.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder

    """

    status = True
    json_fmt = kwargs.get("json_fmt", None)

    if master and slaves and json_fmt:
        status = True

    return status


def rpt_slv_log(master, slaves, **kwargs):

    """Method:  rpt_slv_log

    Description:  Function stub holder for mysql_rep_admin.rpt_slv_log.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder

    """

    status = True
    json_fmt = kwargs.get("json_fmt", None)

    if master and slaves and json_fmt:
        status = True

    return status


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_exist
        get_args
        get_args_keys
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {"-A": True, "-D": True, "-m": "Mongo", "-d": "cfg"}

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return True if arg in self.args_array else False

    def get_args(self):

        """Method:  get_args

        Description:  Method stub holder for gen_class.ArgParser.get_args.

        Arguments:

        """

        return self.args_array

    def get_args_keys(self):

        """Method:  get_args_keys

        Description:  Method stub holder for gen_class.ArgParser.get_args_keys.

        Arguments:

        """

        return self.args_array.keys()

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class MasterRep(object):

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


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Slave_Name"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_flatten_json
        test_file_append
        test_single_func
        test_argsarray_all

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.args = ArgParser()
        self.func_dict = {"-A": ["-C", "-S"], "-C": chk_mst_log,
                          "-S": chk_slv_thr, "-D": rpt_slv_log}

    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_flatten_json(self, mock_cfg):

        """Function:  test_flatten_json

        Description:  Test with flatten option for JSON format.

        Arguments:

        """

        self.args.args_array["-f"] = True

        mock_cfg.return_value = "MongoCfg"

        self.assertFalse(mysql_rep_admin.call_run_chk(
            self.args, self.func_dict, self.master, [self.slave]))

    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_file_append(self, mock_cfg):

        """Function:  test_file_append

        Description:  Test with file append mode.

        Arguments:

        """

        self.args.args_array["-a"] = True

        mock_cfg.return_value = "MongoCfg"

        self.assertFalse(mysql_rep_admin.call_run_chk(
            self.args, self.func_dict, self.master, [self.slave]))

    @mock.patch("mysql_rep_admin.gen_class.setup_mail")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_single_func(self, mock_cfg, mock_mail):

        """Function:  test_single_func

        Description:  Test with single function call.

        Arguments:

        """

        del self.args.args_array["-A"]

        self.args.args_array["-t"] = "ToMail"

        mock_cfg.return_value = "MongoCfg"
        mock_mail.return_value = "MailInstance"

        self.assertFalse(mysql_rep_admin.call_run_chk(
            self.args, self.func_dict, self.master, [self.slave]))

    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_argsarray_all(self, mock_cfg):

        """Function:  test_argsarray_all

        Description:  Test with all option in args_array.

        Arguments:

        """

        mock_cfg.return_value = "MongoCfg"

        self.assertFalse(mysql_rep_admin.call_run_chk(
            self.args, self.func_dict, self.master, [self.slave]))


if __name__ == "__main__":
    unittest.main()
