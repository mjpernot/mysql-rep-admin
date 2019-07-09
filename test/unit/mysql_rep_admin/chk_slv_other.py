#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_other.py

    Description:  Unit testing of chk_slv_other in mysql_rep_admin.py.

    Usage:
        test/unit/mysql_rep_admin/chk_slv_other.py

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
import lib.gen_libs as gen_libs
import mysql_rep_admin
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.name = "Master_Name"


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Super-Class:  None

    Sub-Classes:  None

    Methods:
        __init__ -> Class initialization.
        get_name -> Stub method holder for SlaveRep.get_name.
        get_others -> Stub method holder for SlaveRep.get_others.

    """

    def __init__(self, skip=1, tmp_tbl=6, retry=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            None

        """

        self.name = "Slave_Name"
        self.skip = skip
        self.tmp_tbl = tmp_tbl
        self.retry = retry
        

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for SlaveRep.get_name.

        Arguments:

        """

        return self.name

    def get_others(self):

        """Method:  get_others

        Description:  Stub method holder for SlaveRep.get_others.

        Arguments:

        """

        return self.skip, self.tmp_tbl, self.retry


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:

    Methods:
        setUp -> Initialize testing environment.
        test_no_slv -> Test with no slaves present.
        test_chk_slv_other -> Test chk_slv_other method.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()

    def test_no_slv(self):

        """Function:  test_no_slv

        Description:  Test with no slaves present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_other(self.master, []))

    def test_chk_slv_other(self):

        """Function:  test_chk_slv_other

        Description:  Test chk_slv_other method.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_admin.chk_slv_other(self.master,
                                                          [self.slave]))


if __name__ == "__main__":
    unittest.main()
