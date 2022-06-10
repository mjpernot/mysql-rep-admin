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
        mysql_rep_admin.py -d path
            {-C -c file -s [path/]slave.txt |
             -S -s [path/]slave.txt |
             -B -c file |
             -D -s [path/]slave.txt |
             -T -c file -s [path]/slave.txt [-j [-f]] [-o dir_path/file [-a]]
                [-i db:coll -m file]
                [-t ToEmail [ToEmail2 ...] [-u SubjectLine]] |
             -E -s [path/]slave.txt |
             -A -c file -s [path/]slave.txt [-j [-f]] [-o dir_path/file [-a]]
                [-i db:coll -m file]
                [-t ToEmail [ToEmail2 ...] [-u SubjectLine]] |
             -O -s [path/]slave.txt}
            [-y flavor_id] [-p path] [-z]
            [-v | -h]

    Arguments:
        -d dir path => Directory path to the config files. Required arg.

        -C => Compare master binlog position to the slaves' and return any
                differences detected if not the same positions.
            -c file => Master config file.
            -s [path/]slave.txt => Slave config file.

        -S => Check the slave(s) IO and SQL threads and return any errors or
                warnings detected.
            -s [path/]slave.txt => Slave config file.

        -B => Display the master binlog filename and position.
            -c file => Master config file.

        -D => Display the slave(s) binlog filename and position.
            -s [path/]slave.txt => Slave config file.

        -T => Check time lag for the slave(s) and return any differences
                detected.
            -c file => Master config file.
            -s [path/]slave.txt => Slave config file.
            -j => Return output in JSON format.
            -f => Flatten the JSON data structure to file and standard out.
            # -e => Expand the JSON data structure.
                # NOTE: This is replacing -f option.
            -o path/file => Directory path and file name for output.
            -a => Append output to output file.
            -i [database:collection] => Insert results of command into Mongo
                    database. List the name of database and collection.
                    Default: sysmon:mysql_rep_lag
                -m file => File is the Mongo configuration file for inserting
                    results into a Mongo database.  This is loaded as a python
                    module, do not include the .py extension with the name.
            -t to_email_addresses => Enables emailing capability for an option
                if the option allows it.  Sends output to one or more email
                addresses.
            -u subject_line => Subject line of email.  Will create own subject
                line if one is not provided.
            NOTE:  If returning as standard format and there is no time lag,
                nothing will be returned.  However, if -j option is selected,
                then a JSON doc will be returned even if no time lag.

        -E => Check for any replication errors on the slave(s).
            -s [path/]slave.txt => Slave config file.

        -A => Runs multiple checks which include the options:  -C, -S, -T, -E
            -c file => Master config file.
            -s [path/]slave.txt => Slave config file.
            -j => Return output in JSON format.
            -f => Flatten the JSON data structure to file and standard out.
            # -e => Expand the JSON data structure.
                # NOTE: This is replacing -f option.
            -o path/file => Directory path and file name for output.
            -a => Append output to output file.
            -i [database:collection] => Insert results of command into Mongo
                    database. List the name of database and collection.
                    Default: sysmon:mysql_rep_lag
                -m file => File is the Mongo configuration file for inserting
                    results into a Mongo database.  This is loaded as a python
                    module, do not include the .py extension with the name.
            -t to_email_addresses => Enables emailing capability for an option
                if the option allows it.  Sends output to one or more email
                addresses.
            -u subject_line => Subject line of email.  Will create own subject
                line if one is not provided.
            NOTE:  If returning as standard format and there is no time lag,
                nothing will be returned.  However, if -j option is selected,
                then a JSON doc will be returned even if no time lag.

        -O => Other slave replication checks and return any errors detected.
            -s [path/]slave.txt => Slave config file.

        -p dir_path => Directory path to the mysql binary programs.
        -y value => A flavor id for the program lock.  To create unique lock.
        -z => Suppress standard out.
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
            password="PASSWORD"
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

            Note:  If using SSL connections then set one or more of the
                following entries.  This will automatically enable SSL
                connections. Below are the configuration settings for SSL
                connections.  See configuration file for details on each entry:

            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None
            ssl_client_phrase = None

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

    Example:
        mysql_rep_admin.py -c master -d config  -s slave.txt -T

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import time
import datetime

# Third party
import json
import ast

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.machine as machine
import lib.gen_class as gen_class
import mysql_lib.mysql_class as mysql_class
import mysql_lib.mysql_libs as mysql_libs
import mongo_lib.mongo_libs as mongo_libs
import version

__version__ = version.__version__

# Global
PRT_TEMPLATE = "\nSlave: {0}"


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def rpt_mst_log(master, slaves, **kwargs):

    """Function:  rpt_mst_log

    Description:  Returns the master log file name and position.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    slaves = list(slaves)

    if master:
        fname, log_pos = master.get_log_info()
        name = master.get_name()

        print("\nMaster: {0}".format(name))
        print("\tMaster Log:\t{0}".format(fname))
        print("\tLog Position:\t{0}".format(log_pos))

        if master.gtid_mode:
            print("\tGTID Position:\t{0}".format(master.exe_gtid))

    else:
        print("\nrpt_mst_log:  Warning:  No Master instance detected.")


def rpt_slv_log(master, slaves, **kwargs):

    """Function:  rpt_slv_log

    Description:  Returns the master and relay master log file names along with
        the read and exec master log positions.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    global PRT_TEMPLATE

    slaves = list(slaves)

    if slaves:

        for slv in slaves:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            print(PRT_TEMPLATE.format(name))
            print("\tMaster File:\t\t{0}".format(mst_file))
            print("\tMaster Position:\t{0}".format(read_pos))

            if slv.gtid_mode:
                print("\tRetrieved GTID:\t\t{0}".format(slv.retrieved_gtid))

            print("\tRelay File:\t\t{0}".format(relay_file))
            print("\tExec Position:\t\t{0}".format(exec_pos))

            if slv.gtid_mode:
                print("\tExecuted GTID:\t\t{0}".format(slv.exe_gtid))

    else:
        print("\nrpt_slv_log:  Warning:  No Slave instance detected.")


def chk_slv(slave, **kwargs):

    """Function:  chk_slv

    Description:  Compares the Slave's read file and postition with the
        executed file and position.  Will also print GTID info, in pre-MySQL
        5.6 this will be NULL.

    Arguments:
        (input) slave -> Slave instance.

    """

    global PRT_TEMPLATE

    mst_file, relay_file, read_pos, exec_pos = slave.get_log_info()
    name = slave.get_name()

    # Slave's master info doesn't match slave's relay info.
    if mst_file != relay_file or read_pos != exec_pos:
        print(PRT_TEMPLATE.format(name))
        print("Warning:  Slave might be lagging in execution of log.")
        print("\tRead Log:\t{0}".format(mst_file))
        print("\tRead Pos:\t{0}".format(read_pos))

        if slave.gtid_mode:
            print("\tRetrieved GTID:\t{0}".format(slave.retrieved_gtid))

        print("\tExec Log:\t{0}".format(relay_file))
        print("\tExec Pos:\t{0}".format(exec_pos))

        if slave.gtid_mode:
            print("\tExecuted GTID:\t{0}".format(slave.exe_gtid))


def chk_mst_log(master, slaves, **kwargs):

    """Function:  chk_mst_log

    Description:  Compares the binary log and position between the master and
        slave(s) and also compares the read and execute positions of
        the log on the slave itself.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    slaves = list(slaves)

    if master and slaves:
        fname, log_pos = master.get_log_info()

        for slv in slaves:
            mst_file, _, read_pos, _ = slv.get_log_info()
            name = slv.get_name()

            # Master's log file or position doesn't match slave's log info.
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print("Master: {0}".format(master.name))
                print("\tMaster Log: {0}".format(fname))
                print("\tMaster Pos: {0}".format(log_pos))
                print("Slave: {0}".format(name))
                print("\tSlave Log: {0}".format(mst_file))
                print("\tSlave Pos: {0}".format(read_pos))

            chk_slv(slv, **kwargs)

    elif slaves:
        print("\nchk_mst_log:  Warning:  Missing Master instance.")

        for slv in slaves:
            chk_slv(slv, **kwargs)

    else:
        print("\nchk_mst_log:  Warning:  Missing Master and Slave instances.")


def chk_slv_thr(master, slaves, **kwargs):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    global PRT_TEMPLATE

    slaves = list(slaves)

    if slaves:

        for slv in slaves:
            thr, io_thr, sql_thr, run = slv.get_thr_stat()
            name = slv.get_name()

            # Slave IO and run state.
            if not thr or not gen_libs.is_true(run):
                print(PRT_TEMPLATE.format(name))
                print("\tError:  Slave IO/SQL Threads are down.")

            # Slave IO thread.
            elif not gen_libs.is_true(io_thr):
                print(PRT_TEMPLATE.format(name))
                print("\tError:  Slave IO Thread is down.")

            # Slave SQL thread.
            elif not gen_libs.is_true(sql_thr):
                print(PRT_TEMPLATE.format(name))
                print("\tError:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_slv_err(master, slaves, **kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    print_template = "\nSlave:\t{0}"
    slaves = list(slaves)

    if slaves:

        for slv in slaves:

            # For pre-MySQL 5.6 versions, will be NULL for these two entries.
            iost, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # Connection status
            if not slv.conn:
                print(print_template.format(name))
                print("\tConnection Error:  No connection detected")

            # IO error
            if iost:
                print(print_template.format(name))
                print("\tIO Error Detected:\t{0}".format(iost))
                print("\tIO Message:\t{0}".format(io_msg))

                print("\tIO Timestamp:\t{0}".format(io_time))

            # SQL error
            if sql:
                print(print_template.format(name))
                print("\tSQL Error Detected:\t{0}".format(sql))
                print("\tSQL Message:\t{0}".format(sql_msg))

                print("\tSQL Timestamp:\t{0}".format(sql_time))

    else:
        print("\nchk_slv_err:  Warning:  No Slave instance detected.")


def add_miss_slaves(master, outdata):

    """Function:  add_miss_slaves

    Description:  Adds any down slave hosts to the JSON's slave list.

    Arguments:
        (input) master -> Master instance.
        (input) outdata -> JSON document of Check Slave Time output.
        (output) outdata -> JSON document of Check Slave Time output.

    """

    outdata = dict(outdata)
    all_list = []
    slv_list = []

    for slv in master.show_slv_hosts():
        all_list.append(slv["Host"])

    for slv in outdata["Slaves"]:
        slv_list.append(slv["Name"])

    # Add slaves from the slave list that are not in the master's slave list.
    for item in [val for val in all_list if val not in slv_list]:
        outdata["Slaves"].append({"Name": item, "LagTime": None})

    return outdata


def chk_slv_time(master, slaves, **kwargs):

    """Function:  chk_slv_time

    Description:  Checks for time delays on the slave(s).

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.
        (input) **kwargs:
            ofile -> file name - Name of output file.
            db_tbl -> database:collection - Name of db and collection.
            class_cfg -> Server class configuration settings.
            mail -> Mail instance.
            sup_std -> Suppress standard out.
            json_fmt -> True|False - convert output to JSON format.
            indent -> Indentation level for JSON document.

    """

    slaves = list(slaves)
    json_fmt = kwargs.get("json_fmt", False)

    if json_fmt:
        outdata = {"Application": "MySQL Replication",
                   "Server": master.name,
                   "AsOf": datetime.datetime.strftime(datetime.datetime.now(),
                                                      "%Y-%m-%d %H:%M:%S"),
                   "Slaves": []}

    if slaves:

        for slv in slaves:
            time_lag = slv.get_time()
            name = slv.get_name()
            time_lag = _process_time_lag(slv, time_lag, name, json_fmt)

            if json_fmt:
                outdata["Slaves"].append({"Name": slv.name,
                                          "LagTime": time_lag})

    elif not json_fmt:
        print("\nchk_slv_time:  Warning:  No Slave instance detected.")

    if json_fmt:
        outdata = add_miss_slaves(master, outdata)
        _process_json(outdata, **kwargs)


def _process_json(outdata, **kwargs):

    """Function:  _process_json

    Description:  Private function for chk_slv_time().  Process JSON data.

    Arguments:
        (input) outdata -> JSON document of Check Slave Time output.
        (input) **kwargs:
            ofile -> file name - Name of output file.
            db_tbl -> database:collection - Name of db and collection.
            class_cfg -> Server class configuration settings.
            mail -> Mail instance.
            sup_std -> Suppress standard out.
            mode -> File write mode.
            indent -> Indentation level for JSON document.

    """

    indent = kwargs.get("indent", None)
    jdata = json.dumps(outdata, indent=indent)
    mongo_cfg = kwargs.get("class_cfg", None)
    db_tbl = kwargs.get("db_tbl", None)
    ofile = kwargs.get("ofile", None)
    mail = kwargs.get("mail", None)
    mode = kwargs.get("mode", "w")

    if mongo_cfg and db_tbl:
        dbn, tbl = db_tbl.split(":")
        status = mongo_libs.ins_doc(mongo_cfg, dbn, tbl, outdata)

        if not status[0]:
            print("\n_process_json:  Error Detected:  %s" % (status[1]))

    if ofile:
        gen_libs.write_file(ofile, mode, jdata)

    if mail:
        mail.add_2_msg(jdata)
        mail.send_mail()

    if not kwargs.get("sup_std", False):
        gen_libs.print_data(jdata)


def _process_time_lag(slv, time_lag, name, json_fmt):

    """Function:  _process_time_lag

    Description:  Private function for chk_slv_time().  Process time lag for
        slave.

    Arguments:
        (input) slv -> Slave instance.
        (input) time_lag -> Time lag between master and slave.
        (input) name -> Name of slave.
        (input) json_fmt -> True|False - output to JSON format.
        (output) time_lag -> Time lag between master and slave.

    """

    if time_lag > 0 or time_lag is None:
        time.sleep(5)

        if slv.conn:
            slv.upd_slv_time()

        time_lag = slv.get_time()

        if (time_lag > 0 or time_lag is None) and not json_fmt:
            print("\nSlave:  {0}".format(name))
            print("\tTime Lag:  {0}".format(time_lag or "No Time Detected"))

    return time_lag


def chk_slv_other(master, slaves, **kwargs):

    """Function:  chk_slv_other

    Description:  Checks a number of other status variables that might indicate
        a problem on the slave(s).

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    slaves = list(slaves)

    if slaves:

        for slv in slaves:
            skip, tmp_tbl, retry = slv.get_others()
            name = slv.get_name()
            _chk_other(skip, tmp_tbl, retry, name, slv.version)

    else:
        print("\nchk_slv_other:  Warning:  No Slave instance detected.")


def _chk_other(skip, tmp_tbl, retry, name, sql_ver):

    """Function:  _chk_other

    Description:  Private function for chk_slv_other().  Print any possible
        problems found.

    Arguments:
        (input) skip -> Mysql's skip count.
        (input) tmp_tbl -> Mysql's temp tables created count.
        (input) retry -> Mysql's retry count.
        (input) name -> Name of Mysql server.
        (input) sql_ver -> Slave's MySQL version.

    """

    global PRT_TEMPLATE

    if skip is None or skip > 0:
        print(PRT_TEMPLATE.format(name))
        print("\tSkip Count:  {0}".format(skip))

    if not tmp_tbl or int(tmp_tbl) > 5:
        print(PRT_TEMPLATE.format(name))
        print("\tTemp Table Count:  {0}".format(tmp_tbl))

    if (sql_ver[0] < 8 and (not retry or int(retry) > 0)) \
       or (sql_ver[0] >= 8 and retry > 0):
        print(PRT_TEMPLATE.format(name))
        print("\tRetried Transaction Count:  {0}".format(retry))


def dict_out(data, **kwargs):

    """Function:  dict_out

    Description:  Print dictionary to a file, standard out, and/or an email
        instance either in expanded or flatten JSON format.

    Arguments:
        (input) data -> Dictionary document
        (input) kwargs:
            expand -> True|False - Expand JSON format
            mail -> Mail instance
            ofile -> Name of output file name
            mode -> w|a => Write or append mode for file
            no_std -> True|False - Do not print to standard out
        (output) err_flag -> True|False - If error has occurred
        (output) err_msg -> Error message

    """

    err_flag = False
    err_msg = None
    mail = kwargs.get("mail", None)
    indent = 4 if kwargs.get("expand", False) else None
    mode = kwargs.get("mode", "w")
    ofile = kwargs.get("ofile", None)
    no_std = kwargs.get("mail", False)

    if isinstance(data, dict):
        if ofile:
            gen_libs.print_data(
                json.dumps(data, indent=indent), ofile=ofile, mode=mode)

        if not no_std:
            gen_libs.print_data(json.dumps(data, indent=indent))

        if mail:
            mail.add_2_msg(json.dumps(data, indent=indent))

    else:
        err_flag = True
        err_msg = "Error: Is not a dictionary: %s" % (data)

    return err_flag, err_msg


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
    def_subj = kwargs.get("def_subj", "NoSubjectLine")
    mail = None

    if args.get_val("-t", def_val=False):
        mail = gen_class.setup_mail(
            args.get_val("-t"), subj=args.get_val("-s", def_val=def_subj))

    status = dict_out(
        data, ofile=args.get_val("-o", def_val=None),
        mode="a" if args.get_val("-a", def_val=False) else "w",
        expand=args.get_val("-e", def_val=False),
        no_std=args.get_val("-z", def_val=False), mail=mail)

    if not status[0]:
        print("data_out 1:  Error detected: %s" % (status[1]))

    elif args.arg_exist("-i") and args.arg_exist("-m"):
        cfg = gen_libs.load_module(args.get_val("-m"), args.get_val("-d"))
        dbs, tbl = args.get_val("-i").split(":")
        status2 = mongo_libs.ins_doc(cfg, dbs, tbl, data)

        if not status2[0]:
            print("data_out 2:  Error Detected:  %s" % (status2[1]))

    if mail and not status[0]:
        mail.send_mail()


def call_run_chk(args, func_dict, master, slaves):

    """Function:  call_run_chk

    Description:  Calls the specified option function calls based on what
        instances are available.  Both the master and slaves
        instances are passed to the functions, the functions will
        determine what instances to be used.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options
        (input) master -> Master instance
        (input) slaves -> Slave instances

    """

    func_dict = dict(func_dict)
    slaves = list(slaves)
    mail = None
    mongo_cfg = None
    json_fmt = args.arg_exist("-j")
    outfile = args.get_val("-o", def_val=None)
    db_tbl = args.get_val("-i", def_val=None)
    sup_std = args.arg_exist("-z")
    mode = "a" if args.arg_exist("-a") else "w"
    indent = 4 if args.arg_exist("-f") else None

    if args.arg_exist("-m"):
        mongo_cfg = gen_libs.load_module(
            args.get_val("-m"), args.get_val("-d"))

    if args.arg_exist("-t"):
        mail = gen_class.setup_mail(
            args.get_val("-t"), subj=args.get_val("-u", def_val=None))

    if args.arg_exist("-A"):
        for opt in func_dict["-A"]:
            func_dict[opt](
                master, slaves, json_fmt=json_fmt, ofile=outfile,
                db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail, sup_std=sup_std,
                mode=mode, indent=indent)

        # The option is in func_dict but not under the ALL option and is not
        #   the ALL option itself.
        for item in (opt for opt in args.get_args() if opt in func_dict and
                     opt not in func_dict["-A"] and opt != "-A"):

            func_dict[item](
                master, slaves, json_fmt=json_fmt, ofile=outfile,
                db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail,
                sup_std=sup_std, mode=mode, indent=indent)

    else:

        # Intersect args & func_dict to find which functions to call.
        for opt in set(args.get_args_keys()) & set(func_dict.keys()):
            func_dict[opt](
                master, slaves, json_fmt=json_fmt, ofile=outfile,
                db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail, sup_std=sup_std,
                mode=mode, indent=indent)


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
            octal permission settings.
        file_chk_list -> contains the options which will have files included.
        file_crt_list -> contains options which require files to be created.
        func_dict -> dictionary list for the function calls or other options.
        opt_con_req_list -> contains the options that require other options.
        opt_def_dict -> contains options with their default values.
        opt_or_dict_list -> contains list of options that are OR and required.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_perms_chk = {"-d": 5, "-p": 5}
    file_chk_list = ["-o"]
    file_crt_list = ["-o"]
    func_dict = {"-A": ["-C", "-S", "-E", "-T", "-O"], "-B": rpt_mst_log,
                 "-D": rpt_slv_log, "-C": chk_mst_log, "-S": chk_slv_thr,
                 "-E": chk_slv_err, "-T": chk_slv_time, "-O": chk_slv_other}
    opt_con_req_list = {"-i": ["-m"], "-u": ["-t"], "-A": ["-s"], "-B": ["-c"],
                        "-C": ["-c", "-s"], "-D": ["-s"], "-E": ["-s"],
                        "-O": ["-s"], "-T": ["-c", "-s"]}
    opt_def_dict = {"-i": "sysmon:mysql_rep_lag"}
    opt_multi_list = ["-u", "-t"]
    opt_or_dict_list = {"-c": ["-s"]}
    opt_req_list = ["-d"]
    opt_val_list = ["-d", "-c", "-p", "-s", "-o", "-i", "-m", "-u", "-t", "-y"]
    slv_key = {"sid": "int", "port": "int", "cfg_file": "None",
               "ssl_client_ca": "None", "ssl_ca_path": "None",
               "ssl_client_key": "None", "ssl_client_cert": "None",
               "ssl_client_flag": "int", "ssl_disabled": "bool",
               "ssl_verify_id": "bool", "ssl_verify_cert": "bool"}

    # Process argument list from command line.
    args = gen_class.ArgParser(
        cmdline.argv, opt_val=opt_val_list, multi_val=opt_multi_list,
        opt_def=opt_def_dict, do_parse=True)

    if not gen_libs.help_func(args.get_args(), __version__, help_message) \
       and args.arg_req_or_lst(opt_or=opt_or_dict_list) \
       and args.arg_require(opt_req=opt_req_list) \
       and args.arg_cond_req(opt_con_req=opt_con_req_list) \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)\
       and args.arg_file_chk(file_chk=file_chk_list, file_crt=file_crt_list):

        try:
            proglock = gen_class.ProgramLock(
                cmdline.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict, slv_key=slv_key)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_admin with id of: %s"
                  % (args.get_val("-y", def_val="")))


if __name__ == "__main__":
    sys.exit(main())
