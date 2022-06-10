#!/usr/bin/python
# Classification (U)

"""Program:  data_out.py

    Description:  Unit testing of data_out in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/data_out.py

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
import json
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def linecnt(fname):

    """Function:  linecnt

    Description:  Count number of lines in a file.

    Arguments:

    """

    return sum(1 for _ in open(fname))


class ArgParser(object):

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

        return True if arg in self.args_array else False

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class MailTest(object):

    """Class:  MailTest

    Description:  Class which is a representation of an email.

    Methods:
        __init__
        add_2_msg
        send_mail

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

    def send_mail(self, txt_ln=None):

        """Method:  send_mail

        Description:  Send email.

        Arguments:

        """

        pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_append
        test_mongo_error
        test_mongo3
        test_mongo2
        test_mongo
        test_mail_subj
        test_mail
        test_std_out_errors
        test_std_out

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.mail = MailTest("toaddr")
        self.data = {"Status": "ok"}
        self.args_array1 = {"-t": "toaddr"}
        self.args_array2 = {"-t": "toaddr", "-s": "SubjectLine"}
        self.args_array3 = {"-m": "mongo", "-d": "config", "-i": "DB:Table"}
        self.args_array4 = {"-m": "mongo", "-d": "config"}
        self.args_array5 = {"-d": "config", "-i": "DB:Table"}
        self.args_array6 = {"-a": True}

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    def test_append(self):

        """Function:  test_append

        Description:  Test with append option.

        Arguments:

        """

        self.args.args_array = self.args_array6

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_libs.load_module",
                mock.Mock(return_value="Cfg"))
    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "Error Message2")))
    def test_mongo_error(self):

        """Function:  test_mongo_error

        Description:  Test with mongo option with an error.

        Arguments:

        """

        self.args.args_array = self.args_array3

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_libs.load_module",
                mock.Mock(return_value="Cfg"))
    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    def test_mongo3(self):

        """Function:  test_mongo3

        Description:  Test with mongo option - missing one option.

        Arguments:

        """

        self.args.args_array = self.args_array5

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_libs.load_module",
                mock.Mock(return_value="Cfg"))
    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    def test_mongo2(self):

        """Function:  test_mongo2

        Description:  Test with mongo option - missing one option.

        Arguments:

        """

        self.args.args_array = self.args_array4

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_libs.load_module",
                mock.Mock(return_value="Cfg"))
    @mock.patch("mysql_rep_admin.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    def test_mongo(self):

        """Function:  test_mongo

        Description:  Test with mongo option.

        Arguments:

        """

        self.args.args_array = self.args_array3

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_class.setup_mail")
    def test_mail_subj(self, mock_mail):

        """Function:  test_mail_subj

        Description:  Test with mail option and subject line.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_mail.return_value = self.mail

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_class.setup_mail")
    def test_mail(self, mock_mail):

        """Function:  test_mail

        Description:  Test with mail option.

        Arguments:

        """

        self.args.args_array = self.args_array1

        mock_mail.return_value = self.mail

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(True, "Error Message")))
    def test_std_out_errors(self):

        """Function:  test_std_out_errors

        Description:  Test with errors detected.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.dict_out",
                mock.Mock(return_value=(False, None)))
    def test_std_out(self):

        """Function:  test_std_out

        Description:  Test with standard out.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))


if __name__ == "__main__":
    unittest.main()
