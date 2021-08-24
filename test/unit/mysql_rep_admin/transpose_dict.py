#!/usr/bin/python
# Classification (U)

"""Program:  transpose_dict.py

    Description:  Unit testing of transpose_dict in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/transpose_dict.py

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
import mysql_rep_admin
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_matches2
        test_no_matches
        test_empty_data
        test_multiple_bools2
        test_multiple_bools
        test_multiple_ints
        test_multiple_nones
        test_single_bool_no_key
        test_single_bool2
        test_single_bool
        test_single_int_no_key
        test_single_int
        test_single_str_no_key
        test_single_empty
        test_single_none

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = [{}]
        self.data2 = [{"a": "None"}]
        self.data3 = [{"a": ""}]
        self.data4 = [{"a": "1"}]
        self.data5 = [{"a": "True"}]
        self.data5a = [{"a": "False"}]
        self.data6 = [{"a": "None"}, {"a": ""}]
        self.data7 = [{"a": "1"}, {"a": "1"}]
        self.data8 = [{"a": "True"}, {"a": "True"}]
        self.data8a = [{"a": "False"}, {"a": "False"}]

        self.data_key = {}
        self.data_key2 = {"a": "None"}
        self.data_key3 = {"a": "int"}
        self.data_key4 = {"a": "bool"}
        self.data_key5 = {"b": "None"}

        self.results = [{"a": "None"}]
        self.results2 = [{"a": None}]
        self.results3 = [{"a": 1}]
        self.results4 = [{"a": "1"}]
        self.results5 = [{"a": True}]
        self.results5a = [{"a": False}]
        self.results6 = [{"a": "True"}]
        self.results7 = [{"a": None}, {"a": None}]
        self.results8 = [{"a": 1}, {"a": 1}]
        self.results9 = [{"a": True}, {"a": True}]
        self.results9a = [{"a": False}, {"a": False}]

    def test_no_matches2(self):

        """Function:  test_no_matches2

        Description:  Test with no intersect matches.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data7, self.data_key5), self.data7)

    def test_no_matches(self):

        """Function:  test_no_matches

        Description:  Test with no intersect matches.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data2, self.data_key5), self.results)

    def test_empty_data(self):

        """Function:  test_empty_data

        Description:  Test with an empty data list.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data, self.data_key2), self.data)

    def test_multiple_bools2(self):

        """Function:  test_multiple_bools2

        Description:  Test with a multiple boolean entries.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data8a, self.data_key4), self.results9a)

    def test_multiple_bools(self):

        """Function:  test_multiple_bools

        Description:  Test with a multiple boolean entries.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data8, self.data_key4), self.results9)

    def test_multiple_ints(self):

        """Function:  test_multiple_ints

        Description:  Test with a multiple integer entries.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data7, self.data_key3), self.results8)

    def test_multiple_nones(self):

        """Function:  test_multiple_nones

        Description:  Test with a multiple none entries.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data6, self.data_key2), self.results7)

    def test_single_bool_no_key(self):

        """Function:  test_single_bool_no_key

        Description:  Test with an empty data key for boolean.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data5, self.data_key), self.results6)

    def test_single_bool2(self):

        """Function:  test_single_bool2

        Description:  Test with a single boolean entry.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data5a, self.data_key4), self.results5a)

    def test_single_bool(self):

        """Function:  test_single_bool

        Description:  Test with a single boolean entry.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data5, self.data_key4), self.results5)

    def test_single_int_no_key(self):

        """Function:  test_single_int_no_key

        Description:  Test with an empty data key for integer.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data4, self.data_key), self.results4)

    def test_single_int(self):

        """Function:  test_single_int

        Description:  Test with a single integer entry.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data4, self.data_key3), self.results3)

    def test_single_str_no_key(self):

        """Function:  test_single_str_no_key

        Description:  Test with an empty data key for string.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data2, self.data_key), self.results)

    def test_single_empty(self):

        """Function:  test_single_empty

        Description:  Test with a single empty entry.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data3, self.data_key2), self.results2)

    def test_single_none(self):

        """Function:  test_single_none

        Description:  Test with a single none entry.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.transpose_dict(
                self.data2, self.data_key2), self.results2)


if __name__ == "__main__":
    unittest.main()
