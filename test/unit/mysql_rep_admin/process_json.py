#!/usr/bin/python
# Classification (U)

"""Program:  process_json.py

    Description:  Unit testing of process_json in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/process_json.py

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


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__ -> Class initialization.
        add_2_msg -> Stub method holder for Mail.add_2_msg.
        send_mail -> Stub method holder for Mail.send_mail.

    """

    def __init__(self, lag_time=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        pass

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        return True

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_mail -> Test with mail option.
        test_stdout -> Test with standard out.
        test_no_stdout -> Test with standard out suppressed.
        test_file -> Test with sending to file.
        test_mongo -> Test with mongo connection.
        test_mongo_missing -> Test with mongo missing one option.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mail = Mail()
        self.outdata = {"key": "value"}

    def test_mail(self):

        """Function:  test_mail

        Description:  Test with mail option.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(
            self.outdata, mail=self.mail, sup_std=True))

    def test_stdout(self):

        """Function:  test_stdout

        Description:  Test with standard out.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin._process_json(self.outdata))

    def test_no_stdout(self):

        """Function:  test_no_stdout

        Description:  Test with standard out suppressed.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(self.outdata,
                                                       sup_std=True))

    @mock.patch("mysql_rep_admin.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_file(self):

        """Function:  test_file

        Description:  Test with sending to file.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(
            self.outdata, ofile="FileName", sup_std=True))

    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    def test_mongo(self):

        """Function:  test_mongo

        Description:  Test with mongo connection.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(
            self.outdata, mongo_cfg ="MongoInstance",
            db_tbl="database:collection", sup_std=True))

    def test_mongo_missing(self):

        """Function:  test_mongo_missing

        Description:  Test with mongo connection missing one argument.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(
            self.outdata, mongo_cfg ="MongoInstance", sup_std=True))


if __name__ == "__main__":
    unittest.main()
