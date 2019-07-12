#!/usr/bin/python
# Classification (U)

"""Program:  setup_mail.py

    Description:  Unit testing of setup_mail in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/setup_mail.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import socket
import getpass

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

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Unit testing initilization.
        test_with_from_line -> Test with from line passed.
        test_no_from_line -> Test with no from line passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.to_line = "email_address"
        self.subj = "subject_line"
        self.frm_line = "from_email_address"

    def test_with_from_line(self):

        """Function:  test_with_from_line

        Description:  Test with from line passed.

        Arguments:

        """

        mail = mysql_rep_admin.setup_mail(self.to_line, self.subj,
                                          self.frm_line)

        self.assertEqual((mail.to, mail.subj, mail.frm),
                         (self.to_line, self.subj, self.frm_line))

    def test_no_from_line(self):

        """Function:  test_no_from_line

        Description:  Test with no from line passed.

        Arguments:

        """

        mail = mysql_rep_admin.setup_mail(self.to_line)
        from_line = getpass.getuser() + "@" + socket.gethostname()

        self.assertEqual((mail.to, mail.subj, mail.frm),
                         (self.to_line, None, from_line))


if __name__ == "__main__":
    unittest.main()
