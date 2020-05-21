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
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_help_true -> Test help if returns true.
        test_help_false -> Test help if returns false.
        test_req_or_false -> Test arg_req_or_lst if returns false.
        test_req_or_true -> Test arg_req_or_lst if returns true.
        test_arg_req_true -> Test arg_require if returns true.
        test_arg_req_false -> Test arg_require if returns false.
        test_arg_cond_false -> Test arg_cond_req if returns false.
        test_arg_cond_true -> Test arg_cond_req if returns true.
        test_arg_dir_true -> Test arg_dir_chk_crt if returns true.
        test_arg_dir_false -> Test arg_dir_chk_crt if returns false.
        test_arg_file_true -> Test arg_file_chk if returns true.
        test_arg_file_false -> Test arg_file_chk if returns false.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "CfgFile", "-d": "CfgDir", "-C": True}

    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_help_false(self, mock_arg, mock_help, mock_or):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = False

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_req_or_false(self, mock_arg, mock_help, mock_or):

        """Function:  test_req_or_false

        Description:  Test arg_req_or_lst if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = False

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_req_or_true(self, mock_arg, mock_help, mock_or, mock_req):

        """Function:  test_req_or_true

        Description:  Test arg_req_or_lst if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_arg_req_true(self, mock_arg, mock_help, mock_or, mock_req):

        """Function:  test_arg_req_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_cond_req")
    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_arg_req_false(self, mock_arg, mock_help, mock_or, mock_req,
                           mock_cond):

        """Function:  test_arg_req_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = False
        mock_cond.return_value = False

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_cond_req")
    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_arg_cond_false(self, mock_arg, mock_help, mock_or, mock_req,
                            mock_cond):

        """Function:  test_arg_cond_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = False
        mock_cond.return_value = False

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("mysql_rep_admin.arg_parser.arg_file_chk")
    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_arg_cond_true(self, mock_arg, mock_help, mock_or, mock_req,
                           mock_cond, mock_dir):

        """Function:  test_arg_cond_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = False
        mock_cond.return_value = True
        mock_dir.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("mysql_rep_admin.arg_parser.arg_file_chk")
    @mock.patch("mysql_rep_admin.arg_parser.arg_require")
    @mock.patch("mysql_rep_admin.arg_parser.arg_req_or_lst")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser.arg_parse2")
    def test_arg_dir_true(self, mock_arg, mock_help, mock_or, mock_req,
                          mock_cond, mock_dir):

        """Function:  test_arg_dir_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_or.return_value = True
        mock_req.return_value = False
        mock_cond.return_value = True
        mock_dir.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser")
    def test_arg_dir_false(self, mock_arg, mock_help):

        """Function:  test_arg_dir_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_req_or_lst.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_file_chk.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = True

        self.assertFalse(mysql_rep_admin.main())

    @mock.patch("mysql_rep_admin.run_program")
    @mock.patch("mysql_rep_admin.gen_libs.help_func")
    @mock.patch("mysql_rep_admin.arg_parser")
    def test_arg_file_false(self, mock_arg, mock_help, mock_run):

        """Function:  test_arg_file_false

        Description:  Test arg_file_chk if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_req_or_lst.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_file_chk.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_run.return_value = True

        self.assertFalse(mysql_rep_admin.main())


if __name__ == "__main__":
    unittest.main()
