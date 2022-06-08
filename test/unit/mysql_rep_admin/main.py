#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/main.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_cond_req
        arg_dir_chk
        arg_file_chk
        arg_require
        arg_req_or_lst
        get_args
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()
        self.opt_req = None
        self.dir_perms_chk = None
        self.file_chk = None
        self.file_crt = None
        self.opt_con_req = None
        self.opt_req2 = True
        self.dir_perms_chk2 = True
        self.file_chk2 = True
        self.opt_con_req2 = True
        self.opt_or = None
        self.opt_or2 = True

    def arg_cond_req(self, opt_con_req):

        """Method:  arg_cond_req

        Description:  Method stub holder for gen_class.ArgParser.arg_cond_req.

        Arguments:

        """

        self.opt_con_req = opt_con_req

        return self.opt_con_req2

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_file_chk(self, file_chk, file_crt):

        """Method:  arg_file_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_file_chk.

        Arguments:

        """

        self.file_chk = file_chk
        self.file_crt = file_crt

        return self.file_chk2

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2

    def arg_req_or_lst(self, opt_or):

        """Method:  arg_req_or_lst

        Description:  Method stub holder for
            gen_class.ArgParser.arg_req_or_lst.

        Arguments:

        """

        self.opt_or = opt_or

        return self.opt_or2

    def get_args(self):

        """Method:  get_args

        Description:  Method stub holder for gen_class.ArgParser.get_args.

        Arguments:

        """

        return self.args_array

    def get_val(self, skey, def_val):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_true
        test_help_false
        test_req_or_false
        test_req_or_true
        test_arg_req_false
        test_arg_req_true
        test_arg_cond_false
        test_arg_cond_true
        test_arg_dir_false
        test_arg_dir_true
        test_arg_file_false
        test_arg_file_true
        test_run_program
        test_programlock_true
        test_programlock_false
        test_programlock_id

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

#        self.args_array = {"-c": "CfgFile", "-d": "CfgDir", "-C": True,
#                           "-s": "slave.txt"}
#        self.args_array2 = {"-c": "CfgFile", "-d": "CfgDir", "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")
        self.args = ArgParser()

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_help_true(self, mock_arg):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_help_false(self, mock_arg):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        self.args.opt_or2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_req_or_false(self, mock_arg):

        """Function:  test_req_or_false

        Description:  Test arg_req_or_lst if returns false.

        Arguments:

        """

        self.args.opt_or2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_req_or_true(self, mock_arg):

        """Function:  test_req_or_true

        Description:  Test arg_req_or_lst if returns true.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_req_false(self, mock_arg):

        """Function:  test_arg_req_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_req_true(self, mock_arg):

        """Function:  test_arg_req_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        self.args.opt_con_req2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_cond_false(self, mock_arg):

        """Function:  test_arg_cond_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        self.args.opt_con_req2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_cond_true(self, mock_arg):

        """Function:  test_arg_cond_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_dir_false(self, mock_arg):

        """Function:  test_arg_dir_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_dir_true(self, mock_arg):

        """Function:  test_arg_dir_true

        Description:  Test arg_dir_chk if returns true.

        Arguments:

        """

        self.args.file_chk2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_file_false(self, mock_arg):

        """Function:  test_arg_file_false

        Description:  Test arg_file_chk if returns false.

        Arguments:

        """

        self.args.file_chk2 = False

        mock_arg.return_value = self.args

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ProgramLock")
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_arg_file_true(self, mock_arg, mock_lock):

        """Function:  test_arg_file_true

        Description:  Test arg_file_chk if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ProgramLock")
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_run_program(self, mock_arg, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ProgramLock")
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_programlock_true(self, mock_arg, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ProgramLock")
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_programlock_false(self, mock_arg, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_lock.side_effect = \
            mysql_rep_admin.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.help_func",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_admin.gen_class.ProgramLock")
    @mock.patch("mysql_rep_admin.gen_class.ArgParser")
    def test_programlock_id(self, mock_arg, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock with flavor ID.

        Arguments:

        """

        self.args.args_array = {"-y": "flavor"}

        mock_arg.return_value = self.args
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_admin.main())


if __name__ == "__main__":
    unittest.main()
