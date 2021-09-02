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
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self, lag_time=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.lag_time = lag_time
        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

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
        setUp
        test_mail
        test_stdout
        test_no_stdout
        test_file
        test_mongo_failed
        test_mongo_successful
        test_mongo_missing

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mail = Mail()
        self.outdata = {"key": "value"}
        self.status = (True, None)
        self.status2 = (False, "Error Message")

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

    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc")
    def test_mongo_failed(self, mock_ins):

        """Function:  test_mongo_failed

        Description:  Test with failed mongo connection.

        Arguments:

        """

        mock_ins.return_value = self.status2

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_rep_admin._process_json(
                    self.outdata, class_cfg="MongoInstance",
                    db_tbl="database:collection", sup_std=True))

    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc")
    def test_mongo_successful(self, mock_ins):

        """Function:  test_mongo_successful

        Description:  Test with successful mongo connection.

        Arguments:

        """

        mock_ins.return_value = self.status

        self.assertFalse(
            mysql_rep_admin._process_json(
                self.outdata, class_cfg="MongoInstance",
                db_tbl="database:collection", sup_std=True))

    def test_mongo_missing(self):

        """Function:  test_mongo_missing

        Description:  Test with mongo connection missing one argument.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin._process_json(
            self.outdata, class_cfg="MongoInstance", sup_std=True))


if __name__ == "__main__":
    unittest.main()
