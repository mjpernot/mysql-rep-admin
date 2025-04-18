# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/run_program.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_admin                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def rpt_slv_log(                                        # pylint:disable=R0913
        master, slaves, form, ofile, db_tbl, class_cfg):

    """Method:  rpt_slv_log

    Description:  Function stub holder for mysql_rep_admin.rpt_slv_log.

    Arguments:

    """

    status = True

    if master and slaves and form:
        status = True

    if ofile and db_tbl and class_cfg:
        status = True

    return status


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

        self.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-s": "slaves.txt"}

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


class SlaveRep():                                       # pylint:disable=R0903

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__

    """

    def __init__(                                       # pylint:disable=R0913
            self, name=None, sid=None, user=None, japd=None, serv_os=None,
            **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Instance name.
            (input) sid -> Server id.
            (input) user -> User name.
            (input) japd -> User pswd.
            (input) serv_os -> Machine class instance.
            (input) **kwargs:
                port -> MySQL port number.
                cfg_file -> MySQL configuration file.
                host -> Host name.

        """

        self.name = name
        self.sid = sid
        self.user = user
        self.japd = japd
        self.serv_os = serv_os
        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", None)
        self.cfg_file = kwargs.get("cfg_file", None)
        self.conn = "Connection Handler"


class MasterRep():                                      # pylint:disable=R0903

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__
        connect

    """

    def __init__(                                       # pylint:disable=R0913
            self, name=None, sid=None, user=None, japd=None, serv_os=None,
            **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Instance name.
            (input) sid -> Server id.
            (input) user -> User name.
            (input) japd -> User pswd.
            (input) serv_os -> Machine class instance.
            (input) **kwargs:
                port -> MySQL port number.
                cfg_file -> MySQL configuration file.
                host -> Host name.

        """

        self.name = name
        self.sid = sid
        self.user = user
        self.japd = japd
        self.serv_os = serv_os
        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", None)
        self.cfg_file = kwargs.get("cfg_file", None)
        self.conn = "Connection Handler"
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  Stub method holder for MasterRep.connect.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class MstCfg():                                         # pylint:disable=R0903

    """Class:  MstCfg

    Description:  Class stub holder for gen_libs.load_module class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "MasterName"
        self.sid = 11
        self.user = "UserName"
        self.japd = None
        self.serv_os = "Linux"
        self.host = "HostName"
        self.port = 3306
        self.cfg_file = "CfgFile"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_master_connect_fail
        test_master_connect_good
        test_master_down
        test_all_slaves_down
        test_one_slave_down
        test_no_master
        test_no_slaves
        test_single_func

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mstcfg = MstCfg()
        self.master = MasterRep()
        self.slave1 = SlaveRep()
        self.slave2 = SlaveRep()
        self.slv_array = [self.slave1, self.slave2]
        self.func_list = {"-D": rpt_slv_log}
        self.args = ArgParser()
        self.cfg_array = [{"name": "HOST_NAME", "japd": "japd",
                           "cfg_file": "None", "host": "SERVER",
                           "user": "root", "serv_os": "Linux", "sid": "11",
                           "port": "3306"},
                          {"name": "HOST_NAME2", "japd": "japd",
                           "cfg_file": "None", "host": "SERVER2",
                           "user": "root", "serv_os": "Linux", "sid": "21",
                           "port": "3306"}]
        self.cfg_array2 = [{"name": "HOST_NAME", "japd": "japd",
                            "cfg_file": "None", "host": "SERVER",
                            "user": "root", "serv_os": "Linux", "sid": 11,
                            "port": 3306},
                           {"name": "HOST_NAME2", "japd": "japd",
                            "cfg_file": "None", "host": "SERVER2",
                            "user": "root", "serv_os": "Linux", "sid": 21,
                            "port": 3306}]

    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_master_conn_fail(self, mock_cfg, mock_rep):

        """Function:  test_master_connect_fail

        Description:  Test with master connection failed.

        Arguments:

        """

        self.master.conn_msg = "Error message"

        mock_cfg.return_value = self.mstcfg
        mock_rep.return_value = self.master

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_master_conn_good(                          # pylint:disable=R0913
            self, mock_cfg, mock_array, mock_rep, mock_slv, mock_transpose):

        """Function:  test_master_connect_good

        Description:  Test with master connection is successful.

        Arguments:

        """

        mock_transpose.return_value = self.cfg_array2
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_master_down(                               # pylint:disable=R0913
            self, mock_cfg, mock_array, mock_rep, mock_slv, mock_transpose):

        """Function:  test_master_down

        Description:  Test with master is down.

        Arguments:

        """

        self.master.conn = None
        mock_transpose.return_value = self.cfg_array2
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_all_slaves_down(                           # pylint:disable=R0913
            self, mock_cfg, mock_array, mock_rep, mock_slv, mock_transpose):

        """Function:  test_all_slaves_down

        Description:  Test with all slaves are down.

        Arguments:

        """

        self.slave1.conn = None
        self.slave2.conn = None
        mock_transpose.return_value = self.cfg_array2
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_one_slave_down(                            # pylint:disable=R0913
            self, mock_cfg, mock_array, mock_rep, mock_slv, mock_transpose):

        """Function:  test_one_slave_down

        Description:  Test with one of the slaves is down.

        Arguments:

        """

        self.slave1.conn = None
        mock_transpose.return_value = self.cfg_array2
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    def test_no_master(self, mock_array, mock_slv, mock_transpose):

        """Function:  test_no_master

        Description:  Test with no -c option in args_array.

        Arguments:

        """

        del self.args.args_array["-c"]

        mock_transpose.return_value = self.cfg_array2
        mock_array.return_value = self.cfg_array
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.mysql_libs.disconnect")
    @mock.patch("mysql_rep_admin.call_run_chk")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_no_slaves(self, mock_cfg, mock_call, mock_dis, mock_rep):

        """Function:  test_no_slaves

        Description:  Test with no -s option in args_array.

        Arguments:

        """

        del self.args.args_array["-s"]

        mock_cfg.return_value = self.mstcfg
        mock_call.return_value = True
        mock_dis.return_value = True
        mock_rep.return_value = self.master

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))

    @mock.patch("mysql_rep_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.gen_libs.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_single_func(                               # pylint:disable=R0913
            self, mock_cfg, mock_array, mock_rep, mock_slv, mock_transpose):

        """Function:  test_single_func

        Description:  Test with single function call.

        Arguments:

        """

        mock_transpose.return_value = self.cfg_array2
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(
            mysql_rep_admin.run_program(self.args, self.func_list))


if __name__ == "__main__":
    unittest.main()
