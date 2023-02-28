# Classification (U)

"""Program:  help_message.py

    Description:  Unit testing of help_message in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/help_message.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        test_help_message

    """

    def test_help_message(self):

        """Function:  test_help_message

        Description:  Test help_message function.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.help_message())


if __name__ == "__main__":
    unittest.main()
