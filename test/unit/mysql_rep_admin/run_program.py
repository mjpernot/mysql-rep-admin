#!/usr/bin/python
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


def rpt_slv_log(master, slaves, form, ofile, db_tbl, class_cfg):

    """Method:  rpt_slv_log

    Description:  Function stub holder for mysql_rep_admin.rpt_slv_log.

    Arguments:
        master -> Stub holder
        slaves -> Stub holder
        form -> Stub holder
        ofile -> Stub holder
        db_tbl -> Stub holder
        class_cfg -> Stub holder

    """

    status = True

    if master and slaves and form and ofile and db_tbl and class_cfg:
        status = True

    return status


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, name=None, sid=None, user=None, japd=None,
                 serv_os=None, **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Stub holder.
            (input) sid -> Stub holder.
            (input) user -> Stub holder.
            (input) japd -> Stub holder.
            (input) serv_os -> Stub holder.
            (input) **kwargs:
                port -> Stub holder.
                cfg_file -> Stub holder.
                host -> Stub holder.

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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__ -> Class initialization.
        connect -> Stub method holder for MasterRep.connect.

    """

    def __init__(self, name=None, sid=None, user=None, japd=None,
                 serv_os=None, **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Stub holder.
            (input) sid -> Stub holder.
            (input) user -> Stub holder.
            (input) japd -> Stub holder.
            (input) serv_os -> Stub holder.
            (input) **kwargs:
                port -> Stub holder.
                cfg_file -> Stub holder.
                host -> Stub holder.

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

    def connect(self):

        """Method:  connect

        Description:  Stub method holder for MasterRep.connect.

        Arguments:

        """

        return True


class MstCfg(object):

    """Class:  MstCfg

    Description:  Class stub holder for gen_libs.load_module class.

    Methods:
        __init__ -> Class initialization.

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
        setUp -> Initialize testing environment.
        test_master_down -> Test with master is down.
        test_all_slaves_down -> Test with all slaves are down.
        test_one_slave_down -> Test with one of the slaves is down.
        test_no_master -> Test with no -c option in args_array.
        test_no_slaves -> Test with no -s option in args_array.
        test_single_func -> Test with single function call.

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
        self.func_dict = {"-D": rpt_slv_log}
        self.args_array = {"-D": True, "-m": "Mongo", "-d": "cfg",
                           "-c": "configfile", "-s": "slavefile"}
        self.args_array2 = {"-D": True, "-m": "Mongo", "-d": "cfg",
                            "-c": "configfile"}
        self.args_array3 = {"-D": True, "-m": "Mongo", "-d": "cfg"}
        self.cfg_array = [{"name": "HOST_NAME", "japd": "japd",
                           "cfg_file": "None", "host": "SERVER",
                           "user": "root", "serv_os": "Linux", "sid": "11",
                           "port": "3306"},
                          {"name": "HOST_NAME2", "japd": "japd",
                           "cfg_file": "None", "host": "SERVER2",
                           "user": "root", "serv_os": "Linux", "sid": "21",
                           "port": "3306"}]

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.cmds_gen.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_master_down(self, mock_cfg, mock_array, mock_rep, mock_slv):

        """Function:  test_master_down

        Description:  Test with master is down.

        Arguments:

        """

        self.master.conn = None
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(mysql_rep_admin.run_program(self.args_array,
                                                     self.func_dict))

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.cmds_gen.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_all_slaves_down(self, mock_cfg, mock_array, mock_rep, mock_slv):

        """Function:  test_all_slaves_down

        Description:  Test with all slaves are down.

        Arguments:

        """

        self.slave1.conn = None
        self.slave2.conn = None
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(mysql_rep_admin.run_program(self.args_array,
                                                     self.func_dict))

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.cmds_gen.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_one_slave_down(self, mock_cfg, mock_array, mock_rep, mock_slv):

        """Function:  test_one_slave_down

        Description:  Test with one of the slaves is down.

        Arguments:

        """

        self.slave1.conn = None
        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(mysql_rep_admin.run_program(self.args_array,
                                                     self.func_dict))

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect")
    @mock.patch("mysql_rep_admin.call_run_chk")
    def test_no_master(self, mock_call, mock_dis):

        """Function:  test_no_master

        Description:  Test with no -c option in args_array.

        Arguments:

        """

        mock_call.return_value = True
        mock_dis.return_value = True

        self.assertFalse(mysql_rep_admin.run_program(self.args_array3,
                                                     self.func_dict))

    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.cmds_gen.disconnect")
    @mock.patch("mysql_rep_admin.call_run_chk")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_no_slaves(self, mock_cfg, mock_call, mock_dis, mock_rep):

        """Function:  test_no_slaves

        Description:  Test with no -s option in args_array.

        Arguments:

        """

        mock_cfg.return_value = self.mstcfg
        mock_call.return_value = True
        mock_dis.return_value = True
        mock_rep.return_value = self.master

        self.assertFalse(mysql_rep_admin.run_program(self.args_array2,
                                                     self.func_dict))

    @mock.patch("mysql_rep_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.call_run_chk", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_admin.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_admin.mysql_class.MasterRep")
    @mock.patch("mysql_rep_admin.cmds_gen.create_cfg_array")
    @mock.patch("mysql_rep_admin.gen_libs.load_module")
    def test_single_func(self, mock_cfg, mock_array, mock_rep, mock_slv):

        """Function:  test_single_func

        Description:  Test with single function call.

        Arguments:

        """

        mock_cfg.return_value = self.mstcfg
        mock_array.return_value = self.cfg_array
        mock_rep.return_value = self.master
        mock_slv.return_value = self.slv_array

        self.assertFalse(mysql_rep_admin.run_program(self.args_array,
                                                     self.func_dict))


if __name__ == "__main__":
    unittest.main()
