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
        setUp
        test_retry_80
        test_retry_pre80
        test_tmp_tbl_down
        test_skip_down
        test_retry_error
        test_tmp_tbl_error
        test_skip_error
        test_no_errors

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.skip0 = 0
        self.skip1 = 1
        self.skip2 = None
        self.tmp_tbl0 = unicode(0)
        self.tmp_tbl6 = unicode(6)
        self.tmp_tbl2 = None
        self.retry0 = unicode(0)
        self.retry1 = unicode(1)
        self.retry2 = None
        self.name = "SlaveName"
        self.version = (5, 6, 31)
        self.version2 = (8, 0, 23)
        self.results = {"Name": self.name}
        self.results2 = {"Name": self.name, "SkipCount": self.skip1}
        self.results3 = {"Name": self.name, "TempTableCount": self.tmp_tbl6}
        self.results4 = {
            "Name": self.name, "RetryTransactionCount": self.retry1}
        self.results5 = {"Name": self.name, "SkipCount": self.skip2}
        self.results6 = {"Name": self.name, "TempTableCount": self.tmp_tbl2}

    def test_retry_80(self):

        """Function:  test_retry_80

        Description:  Test with retry is set and 8.0 version.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl0, self.retry1, self.name,
            self.version2), self.results4)

    def test_retry_pre80(self):

        """Function:  test_retry_pre80

        Description:  Test with retry is set and pre 8.0 version.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl0, self.retry1, self.name,
            self.version), self.results4)

    def test_tmp_tbl_down(self):

        """Function:  test_tmp_tbl_down

        Description:  Test with tmp_tbl is down slave.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl2, self.retry0, self.name,
            self.version), self.results6)

    def test_skip_down(self):

        """Function:  test_skip_down

        Description:  Test with skip is down slave.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip2, self.tmp_tbl0, self.retry0, self.name,
            self.version), self.results5)

    def test_retry_error(self):

        """Function:  test_retry_error

        Description:  Test with retry error detected.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl0, self.retry1, self.name,
            self.version), self.results4)

    def test_tmp_tbl_error(self):

        """Function:  test_tmp_tbl_error

        Description:  Test with tmp table error detected.

        Arguments:

        """

        self.assertEqual(mysql_rep_admin._chk_other(
            self.skip0, self.tmp_tbl6, self.retry0, self.name,
            self.version), self.results3)

    def test_skip_error(self):

        """Function:  test_skip_error

        Description:  Test with skip error detected.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._chk_other(
                self.skip1, self.tmp_tbl0, self.retry0, self.name,
                self.version), self.results2)

    def test_no_errors(self):

        """Function:  test_no_errors

        Description:  Test with no errors detected.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin._chk_other(
                self.skip0, self.tmp_tbl0, self.retry0, self.name,
                self.version), self.results)


if __name__ == "__main__":
    unittest.main()
