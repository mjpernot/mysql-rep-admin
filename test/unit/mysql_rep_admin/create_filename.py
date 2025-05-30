# Classification (U)

"""Program:  create_filename.py

    Description:  Unit testing of create_filename in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/create_filename.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin                          # pylint:disable=E0401,C0413
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_exist
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {}

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_filename_all
        test_filename_host_msecs
        test_filename_host_dtg
        test_filename_dtg_msecs
        test_filename_msecs
        test_filename_dtg
        test_filename_hostname
        test_filename

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.dtg = gen_class.TimeFormat()
        self.dtg.create_time()

        # -f = FileName
        # -n = True|False - Use Hostname
        # -g = True|False - Use DTG
        # -m = True|False - Use Microseconds
        self.args_array1 = {"-f": "FileName"}
        self.args_array2 = {"-f": "FileName"}
        self.args_array4 = {"-f": "FileName", "-n": True}
        self.args_array5 = {"-f": "FileName", "-g": True}
        self.args_array6 = {"-f": "FileName", "-m": True}
        self.args_array7 = {"-f": "FileName", "-g": True, "-m": True}
        self.args_array8 = {"-f": "FileName", "-g": True, "-n": True}
        self.args_array9 = {"-f": "FileName", "-m": True, "-n": True}
        self.args_array10 = {
            "-f": "FileName", "-g": True, "-n": True, "-m": True}

        dtg = self.dtg.get_time("dtg")
        msecs = self.dtg.msecs
        json = ".json"
        fname = "FileName."
        fname_host = "FileName.Hostname."
        self.results1 = "FileName.json"
        self.results2 = "FileName.json"
        self.results4 = "FileName.Hostname.json"
        self.results5 = fname + dtg + json
        self.results6 = fname + msecs + json
        self.results7 = fname + dtg + "." + msecs + json
        self.results8 = fname_host + dtg + json
        self.results9 = fname_host + msecs + json
        self.results10 = fname_host + dtg + "." + msecs + json

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_all(self):

        """Function:  test_filename_all

        Description:  Test with subject and hostname and dtg and microseconds.

        Arguments:

        """

        self.args.args_array = self.args_array10

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results10)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_host_msecs(self):

        """Function:  test_filename_host_msecs

        Description:  Test with filename and hostname and microseconds.

        Arguments:

        """

        self.args.args_array = self.args_array9

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results9)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_host_dtg(self):

        """Function:  test_filename_host_dtg

        Description:  Test with filename and hostname and dtg.

        Arguments:

        """

        self.args.args_array = self.args_array8

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results8)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_dtg_msecs(self):

        """Function:  test_filename_dtg_msecs

        Description:  Test with filename and dtg and microseconds.

        Arguments:

        """

        self.args.args_array = self.args_array7

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results7)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_msecs(self):

        """Function:  test_filename_msecs

        Description:  Test with filename and microseconds.

        Arguments:

        """

        self.args.args_array = self.args_array6

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results6)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_dtg(self):

        """Function:  test_filename_dtg

        Description:  Test with filename and DTG.

        Arguments:

        """

        self.args.args_array = self.args_array5

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results5)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename_hostname(self):

        """Function:  test_filename_hostname

        Description:  Test with filename and hostname.

        Arguments:

        """

        self.args.args_array = self.args_array4

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results4)

    @mock.patch("mysql_rep_admin.socket.gethostname",
                mock.Mock(return_value="Hostname"))
    def test_filename(self):

        """Function:  test_filename

        Description:  Test with filename option only.

        Arguments:

        """

        self.args.args_array = self.args_array1

        self.assertEqual(
            mysql_rep_admin.create_filename(
                self.args, dtg=self.dtg), self.results1)


if __name__ == "__main__":
    unittest.main()
