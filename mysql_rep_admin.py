#!/usr/bin/python
# Classification (U)

"""Program:  mysql_rep_admin.py

    Description:  Administration a MySQL Replication database system.  Has a
        number of functions to monitor the status of the replication
        between master and slaves (replicas).  The program can monitor
        and check on a number of different aspects in replication to
        include checking binary log status, slave status, master status,
        time lag between master and slave, errors detected within
        replication, binary log positions, and replication configuration
        status.  The program is setup to monitor between a master
        database and multiple slave databases.

    Usage:
        mysql_rep_admin.py
            {-B -c mysql_cfg -d path [-z] [-e] [-o /path/file [-a]]
                 [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -C -c mysql_cfg -s [/path/]slave.txt -d path [-z] [-e]
                 [-o /path/file [-a]] [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -D -c mysql_cfg -s [/path/]slave.txt -d path [-z] [-e]
                 [-o /path/file [-a]] [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -E -s [path/]slave.txt -d path [-z] [-e] [-o /path/file [-a]]
                 [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -O -s [/path/]slave.txt -d path [-z] [-e] [-o /path/file [-a]]
                 [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -S -s [/path/]slave.txt -d path [-z] [-e] [-o /path/file [-a]]
                 [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -T -c mysql_cfg -s [/path]/slave.txt -d path [-z] [-e] [-x]
                 [-o /path/file [-a]] [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]] |
             -A -c mysql_cfg -s [/path/]slave.txt -d path [-z] [-e]
                 [-o /path/file [-a]] [-i [db:coll] -m mongo_cfg]
                 [-t ToEmail [ToEmail2 ...] [-u SubjectLine] [-w]]}
            [-y flavor_id]
            [-p path]
            [-v | -h]

    Arguments:
        Major options:
        -B => Display the master binlog filename and position.
            -c mysql_cfg => Master config file.
            -d path => Directory path to the config file.

        -C => Compare master binlog position to the slaves' and return any
                differences detected if not the same positions.
            -c mysql_cfg => Master config file.
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        -D => Display the slave(s) binlog filename and position.
            -c mysql_cfg => Master config file.
            -s [/path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        -E => Check for any replication errors on the slave(s).
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        -O => Other slave replication checks and return any errors detected.
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        -S => Check the slave(s) IO and SQL threads and return any errors or
                warnings detected.
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        -T => Check time lag for the slave(s) and return any differences
                detected.
            -c mysql_cfg => Master config file.
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.
            -x => Returns none if no time lag is detected.  If this option is
                used, then none of the other options are allowed.
                Note:  Usually used for email purposes to only email out if a
                    time lag is detected.

        -A => Runs multiple checks which include the options:  -C, -S, -T, -E
            -c mysql_cfg => Master config file.
            -s [path/]slave.txt => Slave config file.
            -d path => Directory path to the config files.

        Options available to the major options above:
            -z => Suppress standard out.
            -e => Expand the JSON data structure.
            -o /path/file => Directory path and file name for output.
                -a => Append output to file.
            -i [database:collection] => Insert results of command into Mongo
                    database. List the name of database and collection.
                    Default: sysmon:mysql_rep_lag
                -m mongo_cfg => File is the Mongo configuration file for
                    inserting results into a Mongo database.  This is loaded as
                    a python module, do not include the .py extension with the
                    name.
            -t to_addresses => Enables emailing capability.  Sends output to
                one or more email addresses.
                -u subject_line => Subject line of email.
                -w => Override the default mail command and use mailx.

        General options:
        -p dir_path => Directory path to the mysql binary programs, if needed.
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE:  -v or -h overrides the other options.

    Notes:
        Master configuration file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for Database:
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOSTNAME"
            sid = SERVER_ID
            extra_def_file = "PYTHON_PROJECT/config/mysql.cfg"
            serv_os = "Linux"
            port = 3306
            cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

            # Set what TLS versions are allowed in the connection set up:
            tls_versions = []

        NOTE 1:  Include the cfg_file even if running remotely as the
            file will be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the
            defaults-extra-file format.
        NOTE 3:  For the -T option to determine if slaves are missing, the
            "report-host" and "report-port" must be added to the mysqld.cnf
            file on each of the slaves and the database restarted for it to
            take effect.
        NOTE 4:  Ignore the Replication user information entries.  They are
            not required for this program.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.


        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PSWORD"
            socket="DIRECTORY_PATH/mysqld.sock"

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.
        NOTE 3:  Socket use is only required to be set in certain conditions
            when connecting using localhost.


        Slave configuration file format (config/slave.txt.TEMPLATE)
        Make a copy of this section for each slave in the replica set.
            # Slave configuration:
            user = USER
            japd = PSWORD
            host = HOST_IP
            name = HOSTNAME
            sid = SERVER_ID
            cfg_file = None
            port = 3306
            serv_os = Linux
            extra_def_file = PYTHON_PROJECT/mysql.cfg

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

        NOTE 1:  Ignore the Replication user information entries.  They are
            not required for this program.


        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
            configuration file format for the Mongo connection used for
            inserting data into a database.
            There are two ways to connect:  single or replica set.

            Single database connection:

            # Single Configuration file for Mongo Database Server.
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOSTNAME"
            port = 27017
            conf_file = None
            auth = True
            auth_db = "admin"
            auth_mech = "SCRAM-SHA-1"
            use_arg = True
            use_uri = False

            Replica Set connection:  Same format as above, but with these
                additional entries at the end of the configuration file:

            repset = "REPLICA_SET_NAME"
            repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
            db_auth = "AUTHENTICATION_DATABASE"

            If Mongo is set to use TLS or SSL connections, then one or more of
                the following entries will need to be completed to connect
                using TLS or SSL protocols.
                Note:  Read the configuration file to determine which entries
                    will need to be set.

                SSL:
                    auth_type = None
                    ssl_client_ca = None
                    ssl_client_key = None
                    ssl_client_cert = None
                    ssl_client_phrase = None
                TLS:
                    auth_type = None
                    tls_ca_certs = None
                    tls_certkey = None
                    tls_certkey_phrase = None

            Note:  FIPS Environment for Mongo.
              If operating in a FIPS 104-2 environment, this package will
              require at least a minimum of pymongo==3.8.0 or better.  It will
              also require a manual change to the auth.py module in the pymongo
              package.  See below for changes to auth.py.

            - Locate the auth.py file python installed packages on the system
                in the pymongo package directory.
            - Edit the file and locate the "_password_digest" function.
            - In the "_password_digest" function there is an line that should
                match: "md5hash = hashlib.md5()".  Change it to
                "md5hash = hashlib.md5(usedforsecurity=False)".
            - Lastly, it will require the Mongo configuration file entry
                auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

    Known Bugs:
        Bug: The -T option may produce extra entries in the slaves list if the
            master's show slave hosts names do not match up with the host names
            in the slave.txt file.
        Workaround: Ensure the slave.txt's host name entries in the file are
            set to match the host names from the master.

    Example:
        mysql_rep_admin.py -c mysql_cfg -d config -s slave.txt -T -x

"""

# Libraries and Global Variables
from __future__ import print_function
from __future__ import absolute_import

# Standard
import sys
import time
import datetime

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .lib import machine
    from .mysql_lib import mysql_class
    from .mysql_lib import mysql_libs
    from .mongo_lib import mongo_libs
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs
    import lib.gen_class as gen_class
    import lib.machine as machine
    import mysql_lib.mysql_class as mysql_class
    import mysql_lib.mysql_libs as mysql_libs
    import mongo_lib.mongo_libs as mongo_libs
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def rpt_mst_log(**kwargs):

    """Function:  rpt_mst_log

    Description:  Returns the master log file name and position.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    master = kwargs.get("master", None)
    data = {"MasterLog": {}}

    if master:
        fname, log_pos = master.get_log_info()
        data["MasterLog"]["Master"] = master.get_name()
        data["MasterLog"]["MasterLog"] = fname
        data["MasterLog"]["LogPosition"] = log_pos

        if master.gtid_mode:
            data["MasterLog"]["GTIDPosition"] = master.exe_gtid

    else:
        print("rpt_mst_log:  Error:  No Master instance detected.")

    return data


def rpt_slv_log(**kwargs):

    """Function:  rpt_slv_log

    Description:  Returns the master and relay master log file names along with
        the read and exec master log positions from each of the slave nodes.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    slaves = list(kwargs.get("slaves", list()))
    data = {"SlaveLogs": []}

    if slaves:
        for slv in slaves:
            if slv.is_connected():
                mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
                tdata = {"Slave": slv.get_name(), "MasterFile": mst_file,
                         "MasterPosition": read_pos, "RelayFile": relay_file,
                         "ExecPosition": exec_pos}

                if slv.gtid_mode:
                    tdata["RetrievedGTID"] = slv.retrieved_gtid

            else:
                tdata = {"Slave": slv.get_name(), "MasterFile": "Unknown",
                         "MasterPosition": "Unknown", "RelayFile": "Unknown",
                         "ExecPosition": "Unknown"}

            data["SlaveLogs"].append(tdata)

    else:
        print("rpt_slv_log:  Error:  No Slave instances detected.")

    return data


def chk_slv(slave):

    """Function:  chk_slv

    Description:  Returns the Slave's read file and postition with the
        executed file and position.  Will also print GTID info, in pre-MySQL
        5.6 this will be NULL.  Include a status on whether the slave might
        be lagging behind the master database.

    Arguments:
        (input) slave -> Slave instance
        (output) data -> Slave log information and status in dictionary format

    """

    mst_file, relay_file, read_pos, exec_pos = slave.get_log_info()

    if slave.is_connected():
        data = {"Name": slave.get_name(), "Status": "OK"}

        # Slave's master info doesn't match slave's relay info.
        if mst_file != relay_file or read_pos != exec_pos:
            data["Status"] = \
                "Warning:  Slave might be lagging in execution of log"
            data["Info"] = {"ReadLog": mst_file, "ReadPosition": read_pos,
                            "ExecLog": relay_file, "ExecPosition": exec_pos}

            if slave.gtid_mode:
                data["Info"]["RetrievedGTID"] = slave.retrieved_gtid
                data["Info"]["ExecutedGTID"] = slave.exe_gtid

    else:
        data = {"Name": slave.get_name(), "Status": "DOWN"}

    return data


def chk_mst_log(**kwargs):

    """Function:  chk_mst_log

    Description:  Returns the binary log and position between the master and
        slave(s) and the read and execute positions of the log on the slave.
        Includes a status of whether the master and slaves are in sync.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    master = kwargs.get("master", None)
    slaves = list(kwargs.get("slaves", list()))
    data = {"CheckMasterLog": {"MasterLog": {}, "SlaveLogs": []}}

    if master and slaves:
        fname, log_pos = master.get_log_info()
        data["CheckMasterLog"]["MasterLog"]["Master"] = {
            "Name": master.name, "Log": fname, "Position": log_pos}
        data["CheckMasterLog"]["MasterLog"]["Slaves"] = list()

        for slv in slaves:
            if slv.is_connected():
                mst_file, _, read_pos, _ = slv.get_log_info()
                tdata = {"Name": slv.get_name(), "Status": "OK"}

                # Master's log file or position doesn't match slave's log info.
                if fname != mst_file or log_pos != read_pos:
                    tdata["Status"] = \
                        "Warning:  Slave lagging in reading master log"
                    tdata["Info"] = {"Log": mst_file, "Position": read_pos}

            else:
                tdata = {"Name": slv.get_name(), "Status": "DOWN"}

            data["CheckMasterLog"]["MasterLog"]["Slaves"].append(tdata)
            data["CheckMasterLog"]["SlaveLogs"].append(chk_slv(slv))

    elif slaves:
        print("chk_mst_log: Warning:  Missing Master instance.")

        for slv in slaves:
            data["CheckMasterLog"]["SlaveLogs"].append(chk_slv(slv))

    else:
        print("chk_mst_log:  Warning:  Missing Master and Slave instances.")

    return data


def chk_slv_thr(**kwargs):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    slaves = list(kwargs.get("slaves", list()))
    data = {"CheckSlaveThread": {"Slaves": []}}

    if slaves:
        for slv in slaves:
            tdata = {"Name": slv.get_name(), "IOThread": "Up",
                     "SQLThread": "Up"}
            thr, io_thr, sql_thr, run = slv.get_thr_stat()

            # Slave IO and run state.
            if not thr or not gen_libs.is_true(run):
                tdata["IOThread"] = "Down"
                tdata["SQLThread"] = "Down"

            # Slave IO thread.
            elif not gen_libs.is_true(io_thr):
                tdata["IOThread"] = "Down"

            # Slave SQL thread.
            elif not gen_libs.is_true(sql_thr):
                tdata["SQLThread"] = "Down"

            data["CheckSlaveThread"]["Slaves"].append(tdata)

    else:
        print("chk_slv_thr:  Warning:  No Slave instance detected.")

    return data


def chk_slv_err(**kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    slaves = list(kwargs.get("slaves", list()))
    data = {"CheckSlaveError": {"Slaves": []}}

    if slaves:
        for slv in slaves:
            if slv.is_connected():
                tdata = {"Name": slv.get_name(), "Connection": "Up",
                         "IO": {"Status": "Good"}, "SQL": {"Status": "Good"}}

                # Pre-MySQL 5.6 versions, will be NULL for these two entries
                iost, sql, io_msg, sql_msg, io_time, sql_time = \
                    slv.get_err_stat()

                # IO error
                if iost:
                    tdata["IO"]["Error"] = iost
                    tdata["IO"]["Message"] = io_msg
                    tdata["IO"]["Timestamp"] = io_time
                    tdata["IO"]["Status"] = "Bad"

                # SQL error
                if sql:
                    tdata["SQL"]["Error"] = sql
                    tdata["SQL"]["Message"] = sql_msg
                    tdata["SQL"]["Timestamp"] = sql_time
                    tdata["SQL"]["Status"] = "Bad"

            else:
                tdata = {"Name": slv.get_name(), "Connection": "DOWN",
                         "IO": {"Status": "Unknown"},
                         "SQL": {"Status": "Unknown"}}

            data["CheckSlaveError"]["Slaves"].append(tdata)

    else:
        print("chk_slv_err:  Warning:  No Slave instance detected.")

    return data


def add_miss_slaves(master, data):

    """Function:  add_miss_slaves

    Description:  Returns a list of missing slaves.

    Arguments:
        (input) master -> Master instance
        (input) data -> JSON document of Check Slave Time output
        (output) miss_slv -> List of missing slaves

    """

    data = dict(data)
    all_list = list()
    slv_list = list()
    miss_slv = list()

    for slv in master.slaves:
        all_list.append(slv["Replica_UUID"])

    for slv in data["CheckSlaveTime"]["Slaves"]:
        slv_list.append(slv["Slave_UUID"])

    # Add slaves from the master slave list that are not in the slave list.
    for uuid in [val for val in all_list if val not in slv_list]:
        miss_slv.append({"Slave_UUID": uuid, "LagTime": "UNK"})

    return miss_slv


def chk_slv_time(**kwargs):

    """Function:  chk_slv_time

    Description:  Checks for time delays on the slave(s).

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    master = kwargs.get("master", None)
    slaves = list(kwargs.get("slaves", list()))
    data = {"CheckSlaveTime": {"Slaves": []}}

    if slaves:
        for slv in slaves:
            if slv.is_connected():
                data["CheckSlaveTime"]["Slaves"].append(
                    {"Name": slv.get_name(),
                     "Slave_UUID": slv.slave_uuid,
                     "LagTime": _process_time_lag(slv, slv.get_time())})
            else:
                data["CheckSlaveTime"]["Slaves"].append(
                    {"Name": slv.get_name(),
                     "Slave_UUID": "Unknown",
                     "LagTime": "DOWN"})

    data["CheckSlaveTime"]["Slaves"] = \
        data["CheckSlaveTime"]["Slaves"] + add_miss_slaves(master, data)

    return data


def _process_time_lag(slv, time_lag):

    """Function:  _process_time_lag

    Description:  Check to see if the time lag still exists.

    Arguments:
        (input) slv -> Slave instance
        (input) time_lag -> Current time lag between master and slave
        (output) time_lag -> Updated time lag between master and slave

    """

    if  time_lag == "null" or time_lag > 0:
        time.sleep(5)

        if slv.conn:
            slv.upd_slv_time()
            time_lag = slv.get_time()

    return time_lag


def chk_slv_other(**kwargs):

    """Function:  chk_slv_other

    Description:  Returns a number of other status variables that might
        indicate a problem on the slaves.

    Arguments:
        (input) kwargs:
            master -> Master instance
            slaves -> Slave instances
        (output) data -> Results of the command in dictionary format

    """

    slaves = list(kwargs.get("slaves", list()))
    data = {"CheckSlaveOther": {"Slaves": list()}}

    if slaves:
        for slv in slaves:
            if slv.is_connected():
                skip, tmp_tbl, retry = slv.get_others()
                data["CheckSlaveOther"]["Slaves"].append(
                    _chk_other(
                        skip, tmp_tbl, retry, slv.get_name(), slv.version))

            else:
                data["CheckSlaveOther"]["Slaves"].append(
                    {"Name": slv.get_name(), "Status": "DOWN"})

    else:
        print("chk_slv_other:  Warning:  No Slave instance detected.")

    return data


def _chk_other(skip, tmp_tbl, retry, name, sql_ver):

    """Function:  _chk_other

    Description:  Private function for chk_slv_other().  Print any possible
        problems found.

    Arguments:
        (input) skip -> Skip count
        (input) tmp_tbl -> Temp tables create count
        (input) retry -> Retry count
        (input) name -> Name of Mysql server
        (input) sql_ver -> Slave's MySQL version
        (output) data -> Dictionary of problems detected in slave

    """

    data = {"Name": name, "Status": "Good"}

    if skip is None or skip > 0:
        data["SkipCount"] = skip
        data["Status"] = "Bad"

    if not tmp_tbl or int(tmp_tbl) > 5:
        data["TempTableCount"] = tmp_tbl
        data["Status"] = "Bad"

    if (sql_ver[0] < 8 and (not retry or int(retry) > 0)) \
       or (sql_ver[0] >= 8 and retry > 0):
        data["RetryTransactionCount"] = retry
        data["Status"] = "Bad"

    return data


def data_out(data, args, **kwargs):

    """Function:  data_out

    Description:  Outputs the data in a variety of formats and media.

    Arguments:
        (input) data -> Data output results
        (input) args -> ArgParser class instance
        (input) kwargs:
            def_subj -> Default subject line for email

    """

    data = dict(data)
    def_subj = kwargs.get("def_subj", "MySQLRepAdminCheck")
    mail = None

    if args.get_val("-t", def_val=False):
        mail = gen_class.setup_mail(
            args.get_val("-t"), subj=args.get_val("-u", def_val=def_subj))

    status = gen_libs.dict_out(
        data, ofile=args.get_val("-o", def_val=None),
        mode="a" if args.get_val("-a", def_val=False) else "w",
        expand=args.get_val("-e", def_val=False),
        no_std=args.get_val("-z", def_val=False), mail=mail)

    if status[0]:
        print("data_out 1:  Error detected: %s" % (status[1]))

    elif args.arg_exist("-i") and args.arg_exist("-m"):
        cfg = gen_libs.load_module(args.get_val("-m"), args.get_val("-d"))
        dbs, tbl = args.get_val("-i").split(":")
        status2 = mongo_libs.ins_doc(cfg, dbs, tbl, data)

        if not status2[0]:
            print("data_out 2:  Error Detected:  %s" % (status2[1]))

    if mail and not status[0]:
        mail.send_mail(use_mailx=args.get_val("-w", def_val=False))


def is_time_lag(data):

    """Function:  is_time_lag

    Description:  Checks to see if there is a time lag.

    Note:  This should only be called when only the -T option is selected and
        no other options as the list should only contain one item in the list.

    Arguments:
        (input) data -> Data output results
        (output) status -> True|False - If there is a time lag detected

    """

    status = False
    data = dict(data)

    # The first list should only contain the -T option results
    for slv in data["Checks"][0]["CheckSlaveTime"]["Slaves"]:

        if slv["LagTime"] != 0:
            status = True
            break

    return status


def call_run_chk(args, func_dict, master, slaves):

    """Function:  call_run_chk

    Description:  Calls the specified option function calls based on what
        instances are available.  Both the master and slaves
        instances are passed to the functions, the functions will
        determine what instances to be used.  The data results will be
        consolidated and then processed.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options
        (input) master -> Master instance
        (input) slaves -> List of slave instances

    """

    func_dict = dict(func_dict)
    slaves = list(slaves)
    data = {"Application": "MySQLReplication",
            "Master": master.name,
            "AsOf": datetime.datetime.strftime(datetime.datetime.now(),
                                               "%Y-%m-%d %H:%M:%S"),
            "Checks": []}

    if args.arg_exist("-A"):
        for opt in func_dict["-A"]:
            tdata = func_dict[opt](master=master, slaves=slaves)
            data["Checks"].append(tdata)

        # The option is in func_dict but not under the ALL option and is not
        #   the ALL option itself
        for item in (opt for opt in args.get_args() if opt in func_dict and
                     opt not in func_dict["-A"] and opt != "-A"):

            tdata = func_dict[item](master=master, slaves=slaves)
            data["Checks"].append(tdata)

    else:

        # Intersect args & func_dict to find which functions to call.
        for opt in set(args.get_args_keys()) & set(func_dict.keys()):
            tdata = func_dict[opt](master=master, slaves=slaves)
            data["Checks"].append(tdata)

    if args.arg_exist("-x") and not is_time_lag(data):
        data = None

    if data:
        data_out(data, args)


def run_program(args, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options
        (input) kwargs:
            slv_key -> Dictionary of keys and data types

    """

    func_dict = dict(func_dict)
    master = None

    if args.arg_exist("-c"):
        mst_cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))

        master = mysql_class.MasterRep(
            mst_cfg.name, mst_cfg.sid, mst_cfg.user, mst_cfg.japd,
            os_type=getattr(machine, mst_cfg.serv_os)(), host=mst_cfg.host,
            port=mst_cfg.port, defaults_file=mst_cfg.cfg_file)
        master.connect(silent=True)

    if master and master.conn_msg:
        print("run_program:  Error encountered on server(%s): %s" %
              (master.name, master.conn_msg))

    else:
        slaves = []

        if args.arg_exist("-s"):
            slv_cfg = gen_libs.create_cfg_array(
                args.get_val("-s"), cfg_path=args.get_val("-d"))
            slv_cfg = gen_libs.transpose_dict(
                slv_cfg, kwargs.get("slv_key", {}))
            slaves = mysql_libs.create_slv_array(slv_cfg)

        call_run_chk(args, func_dict, master, slaves)
        conn_list = [slv for slv in slaves if slv.conn]

        if master and master.conn:
            conn_list.append(master)

        mysql_libs.disconnect(conn_list)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains options which will be directories and the
            octal permission settings
        file_crt_list -> contains options which require files to be created
        file_perm -> file check options with their perms in octal
        func_dict -> dictionary list for the function calls or other options
        opt_con_req_list -> contains the options that require other options
        opt_def_dict -> contains options with their default values
        opt_multi_list -> list of options that will have multiple values
        opt_or_dict_list -> contains list of options that are OR and required
        opt_req_list -> contains the options that are required for the program
        opt_val_list -> contains options which require values
        opt_xor_val -> dictionary with key and values that will be xor
        slv_key -> dictionary that contains keys and data types

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_perms_chk = {"-d": 5, "-p": 5}
    file_crt_list = ["-o"]
    file_perm = {"-o": 6}
    func_dict = {
        "-A": ["-C", "-S", "-E", "-T", "-O"], "-B": rpt_mst_log,
        "-D": rpt_slv_log, "-C": chk_mst_log, "-S": chk_slv_thr,
        "-E": chk_slv_err, "-T": chk_slv_time, "-O": chk_slv_other}
    opt_con_req_list = {
        "-i": ["-m"], "-u": ["-t"], "-w": ["-t"], "-A": ["-s"], "-B": ["-c"],
        "-C": ["-c", "-s"], "-D": ["-s"], "-E": ["-s"], "-O": ["-s"],
        "-T": ["-c", "-s"], "-x": ["-T"]}
    opt_def_dict = {"-i": "sysmon:mysql_rep_lag"}
    opt_multi_list = ["-u", "-t"]
    opt_or_dict_list = {"-c": ["-s"]}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-d", "-c", "-p", "-s", "-o", "-i", "-m", "-u", "-t", "-y"]
    opt_xor_val = {"-x": ["-A", "-B", "-C", "-S", "-E", "-D", "-O"]}
    slv_key = {"sid": "int", "port": "int", "cfg_file": "None",
               "ssl_client_ca": "None", "ssl_ca_path": "None",
               "ssl_client_key": "None", "ssl_client_cert": "None",
               "ssl_client_flag": "int", "ssl_disabled": "bool",
               "ssl_verify_id": "bool", "ssl_verify_cert": "bool"}

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=opt_multi_list,
        opt_def=opt_def_dict, do_parse=True)

    if not gen_libs.help_func(args, __version__, help_message)                \
       and args.arg_req_or_lst(opt_or=opt_or_dict_list)                       \
       and args.arg_require(opt_req=opt_req_list)                             \
       and args.arg_cond_req(opt_con_req=opt_con_req_list)                    \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)                      \
       and args.arg_file_chk(file_perm_chk=file_perm, file_crt=file_crt_list) \
       and args.arg_xor_dict(opt_xor_val=opt_xor_val):

        try:
            proglock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict, slv_key=slv_key)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_admin with id of: %s"
                  % (args.get_val("-y", def_val="")))


if __name__ == "__main__":
    sys.exit(main())
