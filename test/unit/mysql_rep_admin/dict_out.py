#!/usr/bin/python
# Classification (U)

"""Program:  dict_out.py

    Description:  Unit testing of dict_out in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/dict_out.py

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


class Mail(object):

    """Class:  Mail

    Description:  Class which is a representation of the gen_class.Mail class.

    Methods:
        __init__
        add_2_msg

    """

    def __init__(self, toline, subj=None, frm=None, msg_type=None):

        """Method:  __init__

        Description:  Initialization of an instance of the Mail class.

        Arguments:

        """

        if isinstance(subj, list):
            subj = list(subj)

        if isinstance(toline, list):
            self.toline = list(toline)

        else:
            self.toline = toline

        self.subj = subj
        self.frm = frm
        self.msg_type = msg_type
        self.msg = ""

    def add_2_msg(self, txt_ln=None):

        """Method:  add_2_msg

        Description:  Add text to text string if data is present.

        Arguments:

        """

        if txt_ln:

            if isinstance(txt_ln, str):
                self.msg = self.msg + txt_ln

            else:
                self.msg = self.msg + json.dumps(txt_ln)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_mail_std2
        test_mail_std
        test_mail_expand2
        test_mail_expand
        test_non_dict
        test_ofile_expand
        test_set_nostd
        test_set_expand
        test_set_ofile
        test_set_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = {}
        self.data2 = {"key1": "value1"}
        self.ofile = "OutFile"
        self.json_fmt = True
        self.no_std = True
        self.mail = Mail("ToAddress")
        self.msg = '{\n    "key1": "value1"\n}'
        self.msg2 = '{"key1": "value1"}'
        self.err_msg = "Error: Is not a dictionary: [1, 2, 3]"

    def test_mail_std2(self):

        """Function:  test_mail_std2

        Description:  Test with mail with standard format.

        Arguments:

        """

        mysql_rep_admin.dict_out(self.data2, mail=self.mail, no_std=True)

        self.assertEqual(self.mail.msg, self.msg2)

    def test_mail_std(self):

        """Function:  test_mail_std

        Description:  Test with mail with standard format.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.dict_out(
                self.data, mail=self.mail, no_std=True), (False, None))

    def test_mail_expand2(self):

        """Function:  test_mail_expand2

        Description:  Test with mail with expand argument.

        Arguments:

        """

        mysql_rep_admin.dict_out(
            self.data2, mail=self.mail, no_std=True, expand=True)

        self.assertEqual(self.mail.msg, self.msg)

    def test_mail_expand(self):

        """Function:  test_mail_json

        Description:  Test with mail with expand argument.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.dict_out(
                self.data, mail=self.mail, no_std=True, expand=True),
            (False, None))

    def test_non_dict(self):

        """Function:  test_non_dict

        Description:  Test with non-dictionary object.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_admin.dict_out([1, 2, 3]), (True, self.err_msg))

    @mock.patch("mysql_rep_admin.gen_libs.print_data")
    def test_ofile_expand(self, mock_prt):

        """Function:  test_ofile_expand

        Description:  Test with ofile and expand arguments.

        Arguments:

        """

        mock_prt.return_value = True

        self.assertEqual(
            mysql_rep_admin.dict_out(self.data, ofile=self.ofile, expand=True),
            (False, None))

    @mock.patch("mysql_rep_admin.gen_libs.print_data")
    def test_set_nostd(self, mock_prt):

        """Function:  test_set_nostd

        Description:  Test with no_std argument.

        Arguments:

        """

        mock_prt.return_value = True

        self.assertEqual(
            mysql_rep_admin.dict_out(self.data, no_std=self.no_std),
            (False, None))

    @mock.patch("mysql_rep_admin.gen_libs.print_data")
    def test_set_expand(self, mock_prt):

        """Function:  test_set_expand

        Description:  Test with expand argument.

        Arguments:

        """

        mock_prt.return_value = True

        self.assertEqual(
            mysql_rep_admin.dict_out(self.data, expand=True), (False, None))

    @mock.patch("mysql_rep_admin.gen_libs.print_data")
    def test_set_ofile(self, mock_prt):

        """Function:  test_set_ofile

        Description:  Test with ofile argument.

        Arguments:

        """

        mock_prt.return_value = True

        self.assertEqual(mysql_rep_admin.dict_out(self.data, ofile=self.ofile),
                         (False, None))

    @mock.patch("mysql_rep_admin.gen_libs.print_data")
    def test_set_default(self, mock_prt):

        """Function:  test_set_default

        Description:  Test with default settings.

        Arguments:

        """

        mock_prt.return_value = True

        self.assertEqual(mysql_rep_admin.dict_out(self.data), (False, None))


if __name__ == "__main__":
    unittest.main()
