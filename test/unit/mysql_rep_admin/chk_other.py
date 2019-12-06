#!/usr/bin/python
# Classification (U)

"""Program:  chk_other.py

    Description:  Unit testing of chk_other in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_other.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_retry_error -> Test with retry error detected.
        test_tmp_tbl_error -> Test with tmp table error detected.
        test_skip_error -> Test with skip error detected.
        test_no_errors -> Test with no errors detected.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """
        # with gen_libs.no_std_out():
        self.skip0 = 0
        self.skip1 = 1
        self.tmp_tbl0 = 0
        self.tmp_tbl6 = 6
        self.retry0 = 0
        self.retry1 = 1
        self.name = "SlaveName"

    def test_retry_error(self):

        """Function:  test_retry_error

        Description:  Test with retry error detected.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin._chk_other(
                self.skip0, self.tmp_tbl0, self.retry1, self.name))

    def test_tmp_tbl_error(self):

        """Function:  test_tmp_tbl_error

        Description:  Test with tmp table error detected.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin._chk_other(
                self.skip0, self.tmp_tbl6, self.retry0, self.name))

    def test_skip_error(self):

        """Function:  test_skip_error

        Description:  Test with skip error detected.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin._chk_other(
                self.skip1, self.tmp_tbl0, self.retry0, self.name))

    def test_no_errors(self):

        """Function:  test_no_errors

        Description:  Test with no errors detected.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl0, self.retry0, self.name))


if __name__ == "__main__":
    unittest.main()
