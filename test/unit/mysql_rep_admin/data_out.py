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
import unittest
import json
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def linecnt(fname):

    """Function:  linecnt

    Description:  Count number of lines in a file.

    Arguments:

    """

    return sum(1 for _ in open(fname, encoding="UTF-8"))


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


class Mail2():

    """Class:  Mail2

    Description:  Class which is a representation of the gen_class.Mail2 class.

    Methods:
        __init__
        add_attachment
        send_email

    """

    def __init__(self, subject, toaddrs, fromaddr=None):

        """Method:  __init__

        Description:  Initialization of an instance of the Mail2 class.

        Arguments:

        """

        # Dictionary of file types/extensions and their associated MIME types
        self.ftypes = {
            "plain": "plain", "text": "plain", "sh": "x-sh", "x-sh": "x-sh",
            "tar": "x-tar", "x-tar": "x-tar", "pdf": "pdf", "json": "json",
            "gz": "gzip", "gzip": "gzip"}
        self.subj = " ".join(subject) if isinstance(subject, list) else subject
        self.toaddrs = ",".join(
            toaddrs) if isinstance(toaddrs, list) else toaddrs
        self.fromaddr = fromaddr if fromaddr else "UserName" + "@" + "HostName"

        self.msg = {}
        self.msg["From"] = self.fromaddr
        self.msg["To"] = self.toaddrs
        self.msg["Subject"] = self.subj
        self.fname = None
        self.data = None
        self.host = None

    def add_attachment(self, fname, ftype, data):

        """Method:  add_attachment

        Description:  Converts the file data into base64 format and attaches
            the data and filename to the email.

        Arguments:

        """

        ftype = self.ftypes[ftype] if ftype in self.ftypes else None

        if ftype:
            self.fname = fname
            self.data = data

    def send_email(self, host="localhost"):

        """Method:  send_email

        Description:  Converts the mail content to a string and mails out the
            message using SMTP.sendmail.

        Arguments:

        """

        if host:
            self.host = host


class Mail():

    """Class:  Mail

    Description:  Class which is a representation of the gen_class.Mail class.

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

    def send_mail(self, use_mailx=False):

        """Method:  send_mail

        Description:  Send email.

        Arguments:

        """

        status = True

        if use_mailx:
            status = True

        return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_mail2
        test_append
        test_mail_subj
        test_mail_mailx
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
        self.mail = Mail("toaddr")
        self.mail2 = Mail2("subject", "toaddr")
        self.data = {"Status": "ok"}
        self.args_array1 = {"-t": "toaddr"}
        self.args_array2 = {"-t": "toaddr", "-u": "SubjectLine"}
        self.args_array3 = {"-t": "toaddr", "-r": True, "-f": "FileName"}
        self.args_array4 = {
            "-t": "toaddr", "-u": "SubjectLine", "-r": True, "-f": "FileName"}
        self.args_array6 = {"-a": True}
        self.args_array7 = {"-t": "toaddr", "-w": True}

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_class.Mail2")
    def test_mail2_subj(self, mock_mail):

        """Function:  test_mail2_subj

        Description:  Test with Mail2 attachment option and subject line.

        Arguments:

        """

        self.args.args_array = self.args_array4

        mock_mail.return_value = self.mail2

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_class.Mail2")
    def test_mail2(self, mock_mail):

        """Function:  test_mail2

        Description:  Test with Mail2 attachment option.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_mail.return_value = self.mail2

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(False, None)))
    def test_append(self):

        """Function:  test_append

        Description:  Test with append option.

        Arguments:

        """

        self.args.args_array = self.args_array6

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
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

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_admin.gen_class.setup_mail")
    def test_mail_mailx(self, mock_mail):

        """Function:  test_mail_mailx

        Description:  Test with mail option with the mailx override option.

        Arguments:

        """

        self.args.args_array = self.args_array7

        mock_mail.return_value = self.mail

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
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

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(True, "Error Message")))
    def test_std_out_errors(self):

        """Function:  test_std_out_errors

        Description:  Test with errors detected.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))

    @mock.patch("mysql_rep_admin.gen_libs.dict_out",
                mock.Mock(return_value=(False, None)))
    def test_std_out(self):

        """Function:  test_std_out

        Description:  Test with standard out.

        Arguments:

        """

        self.assertFalse(mysql_rep_admin.data_out(self.data, self.args))


if __name__ == "__main__":
    unittest.main()
