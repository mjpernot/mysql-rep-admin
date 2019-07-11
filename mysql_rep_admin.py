#!/usr/bin/python
# Classification (U)

"""Program:  mysql_rep_admin.py

    Description:  Administration program for MySQL Replication system.  Has a
        number of functions to monitor the status of the replication
        between master and slaves (replicas).  The program can monitor
        and check on a number of different aspects in replication to
        include checking binary log status, slave status, master status,
        time lag between master and slave, errors detected within
        replication, binary log positions, and replication configuration
        status.  The program is setup to monitor between a master
        database and multiple slave (replica) databases.

    Usage:
        mysql_rep_admin.py -d path {-c file | -s path/file} [-p path
            | -C | -S | -B | -D | -T | -E | -A | -O | -o dir_path/file]
            -f {JSON|standard | -b db:coll | -m file} [-v | -h]

    Arguments:
        -d dir path => Directory path to the config files (-c and -s).
            Required arg.
        -c file => Master config file.  Is loaded as a python, do not
            include the .py extension with the name.
        -s file => Slave config file.  Will be a text file.  Include the
            file extension with the name.
        -C => Compare master binlog position to the slaves'.
        -S => Check the slave(s) IO and SQL threads.
        -B => Display the master binlog filename and position.
        -D => Display the slave(s) binlog filename and position.
        -T => Check time lag for the slave(s).
        -E => Check for errors on the slave(s).
        -A => Does multiple checks which include the following options:
            (-C, -S, -T, -E)
        -O => Other slave replication checks.
        -f JSON|standard => Output format as JSON or standard. (only
            used with option -T)
        -o path/file => Directory path and file name for output.
        -b database:collection => Name of database and collection.
            Delimited by colon (:).  Default: sysmon:mysql_rep_lag
        -m file => Mongo config file.  Is loaded as a python, do not
            include the .py extension with the name.
        -p dir_path => Directory path to the mysql binary programs.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  Will require -c and/or -s option to be included.
        NOTE 2:  -v or -h overrides the other options.
        NOTE 3:  -o and -f options is only available for -T option.
        NOTE 4:  -b option requires -m option to be included.

    Notes:
        Master configuration file format (filename.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            # WARNING:  Do not use the loopback IP or 'localhost' for the
            #    master database, use the actual IP.
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/my.cnf"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/myextra.cfg"

        NOTE 1:  Include the cfg_file even if running remotely as the
            file will be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the
            defaults-extra-file format.

        Slave(s) configuration file format (filename.txt)
            # Slave 1 configuration {Database Name/Server}
            user = root
            passwd = ROOT_PASSWORD
            host = IP_ADDRESS
            serv_os = Linux or Solaris
            name = HOSTNAME
            port = PORT_NUMBER
            cfg_file DIRECTORY_PATH/my.cnf
            sid = SERVER_ID
            # Slave N configuration {Database Name/Server}
               Repeat rest of above section for Slave 1.

        NOTE:  Include the cfg_file even if running remotely as the file
            will be used in future releases.

    Example:
        mysql_rep_admin.py -c master -d config  -s slaves.txt -A

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import time
import datetime
import os

# Third party
import json

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import lib.machine as machine
import mysql_lib.mysql_class as mysql_class
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


def rpt_mst_log(MASTER, SLAVE, **kwargs):

    """Function:  rpt_mst_log

    Description:  Returns the master log file name and position.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if MASTER:
        fname, log_pos = MASTER.get_log_info()
        name = MASTER.get_name()

        print("\nMaster: {0}".format(name))
        print("\tMaster Log:\t{0}".format(fname))
        print("\tLog Position:\t{0}".format(log_pos))

        if MASTER.gtid_mode:
            print("\tGTID Position:\t{0}".format(MASTER.exe_gtid))

    else:
        print("\nrpt_mst_log:  Warning:  No Master instance detected.")


def rpt_slv_log(MASTER, SLAVE, **kwargs):

    """Function:  rpt_slv_log

    Description:  Returns the master and relay master log file names along with
        the read and exec master log positions.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            print("\nSlave: {0}".format(name))
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


def chk_slv(SLAVE, **kwargs):

    """Function:  chk_slv

    Description:  Compares the Slave's read file and postition with the
        executed file and position.  Will also print GTID info, in pre-MySQL
        5.6 this will be NULL.

    Arguments:
        (input) SLAVE -> Slave class instance.

    """

    mst_file, relay_file, read_pos, exec_pos = SLAVE.get_log_info()
    name = SLAVE.get_name()

    # If slave's master info does not equal slave's relay info.
    if mst_file != relay_file or read_pos != exec_pos:
        print("\nSlave: {0}".format(name))
        print("Warning:  Slave might be lagging in execution of log.")
        print("\tRead Log:\t{0}".format(mst_file))
        print("\tRead Pos:\t{0}".format(read_pos))

        if SLAVE.gtid_mode:
            print("\tRetrieved GTID:\t{0}".format(SLAVE.retrieved_gtid))

        print("\tExec Log:\t{0}".format(relay_file))
        print("\tExec Pos:\t{0}".format(exec_pos))

        if SLAVE.gtid_mode:
            print("\tExecuted GTID:\t{0}".format(SLAVE.exe_gtid))


def chk_mst_log(MASTER, SLAVE, **kwargs):

    """Function:  chk_mst_log

    Description:  Compares the binary log and position between the master and
        slave(s) and also compares the read and execute positions of
        the log on the slave itself.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if MASTER and SLAVE:
        fname, log_pos = MASTER.get_log_info()

        for slv in SLAVE:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            # If master's log file or position doesn't match slave's log info.
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print("Master: {0}".format(MASTER.name))
                print("\tMaster Log: {0}".format(fname))
                print("\t\tMaster Pos: {0}".format(log_pos))
                print("Slave: {0}".format(name))
                print("\tSlave Log: {0}".format(mst_file))
                print("\t\tSlave Pos: {0}".format(read_pos))

            chk_slv(slv, **kwargs)

    elif SLAVE:
        print("\nchk_mst_log:  Warning:  Missing Master instance.")

        for slv in SLAVE:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            chk_slv(slv, **kwargs)

    else:
        print("\nchk_mst_log:  Warning:  Missing Master and Slave instances.")


def chk_slv_thr(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:
            thr, io_thr, sql_thr, run = slv.get_thr_stat()
            name = slv.get_name()

            # Check slave IO state and slave running attributes.
            if not thr or not gen_libs.is_true(run):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave IO/SQL Threads are down.")

            # Check slave IO running attribute.
            elif not gen_libs.is_true(io_thr):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave IO Thread is down.")

            # Check slave SQL running attribute.
            elif not gen_libs.is_true(sql_thr):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_slv_err(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:

            # For pre-MySQL 5.6 versions, will be NULL for these two entries.
            io, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # Is there a IO error
            if io:
                print("\nSlave:\t{0}".format(name))
                print("IO Error Detected:\t{0}".format(io))
                print("\tIO Message:\t{0}".format(io_msg))

                print("\tIO Timestamp:\t{0}".format(io_time))

            # Is there a SQL error
            if sql:
                print("\nSlave:\t{0}".format(name))
                print("SQL Error Detected:\t{0}".format(sql))
                print("\tSQL Message:\t{0}".format(sql_msg))

                print("\tSQL Timestamp:\t{0}".format(sql_time))

    else:
        print("\nchk_slv_err:  Warning:  No Slave instance detected.")


def add_miss_slaves(MASTER, outdata, **kwargs):

    """Function:  add_miss_slaves

    Description:  Adds any down slave hosts to the JSON's slave list.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) outdata -> JSON document of Check Slave Time output.
        (output) outdata -> JSON document of Check Slave Time output.

    """

    all_list = []
    slv_list = []

    for x in MASTER.show_slv_hosts():
        all_list.append(x["Host"])

    for y in outdata["Slaves"]:
        slv_list.append(y["Name"])

    # Loop on slaves that are in master slave list, but not in all slave list.
    for x in [val for val in all_list if val not in slv_list]:
        # Add missing slave to all slave list.
        outdata["Slaves"].append({"Name": x, "Lag_Time": None})

    return outdata


def chk_slv_time(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_time

    Description:  Checks for time delays on the slave(s).

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).
        (input) **kwargs:
            form -> JSON|standard - JSON format or standard output.
            ofile -> file name - Name of output file.
            db_tbl -> database:collection - Name of db and collection.
            class_cfg -> Server class configuration settings.

    """

    frmt = kwargs.get("form", "standard")

    if frmt == "JSON":
        outdata = {"Application": "MySQL Replication",
                   "Master": MASTER.name,
                   "Asof": datetime.datetime.strftime(datetime.datetime.now(),
                                                      "%Y-%m-%d %H:%M:%S"),
                   "Slaves": []}

    if SLAVE:

        for slv in SLAVE:
            time_lag = slv.get_time()
            name = slv.get_name()

            if time_lag:
                time.sleep(5)
                slv.upd_slv_time()
                time_lag = slv.get_time()

                if time_lag and frmt == "standard":
                    print("\nSlave:  {0}".format(name))
                    print("\tTime Lag:  {0}".format(time_lag))

            if frmt == "JSON":
                outdata["Slaves"].append({"Name": slv.name,
                                          "Lag_Time": time_lag})

    elif frmt == "standard":
        print("\nchk_slv_time:  Warning:  No Slave instance detected.")

    if frmt == "JSON":
        outdata = add_miss_slaves(MASTER, outdata)
        mongo_libs.json_prt_ins_2_db(outdata, **kwargs)


def chk_slv_other(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_other

    Description:  Checks a number of other status variables that might indicate
        a problem on the slave(s).

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:
            skip, tmp_tbl, retry = slv.get_others()
            name = slv.get_name()

            if skip > 0 or int(tmp_tbl) > 5 or int(retry) > 0:
                print("\nSlave: {0}".format(name))

                if skip > 0:
                    print("Skip Count:  {0}".format(skip))

                if int(tmp_tbl) > 5:
                    print("Temp Table Count:  {0}".format(tmp_tbl))

                if int(retry) > 0:
                    print("Retried Transaction Count:  {0}".format(retry))

    else:
        print("\nchk_slv_other:  Warning:  No Slave instance detected.")


def call_run_chk(args_array, func_dict, MASTER, SLAVE):

    """Function:  call_run_chk

    Description:  Calls the specified option function calls based on what
        instances are available.  Both the MASTER and SLAVE(s)
        instances are passed to the functions, the functions will
        determine what instances to be used.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    frmt = args_array.get("-f", "standard")
    outfile = args_array.get("-o", None)

    db_tbl = args_array.get("-b", None)
    Mongo_Cfg = None

    if args_array.get("-m", None):
        Mongo_Cfg = gen_libs.load_module(args_array["-m"], args_array["-d"])

    if "-A" in args_array:

        for x in func_dict["-A"]:
            func_dict[x](MASTER, SLAVE, form=frmt, ofile=outfile,
                         db_tbl=db_tbl, class_cfg=Mongo_Cfg)

        for y in args_array:

            # If argument is in func_dict dictionary and not under the ALL
            #   option and is not the ALL option itself.
            if y in func_dict and y not in func_dict["-A"] and y != "-A":
                func_dict[y](MASTER, SLAVE, form=frmt, ofile=outfile,
                             db_tbl=db_tbl, class_cfg=Mongo_Cfg)

    # Else run each option in argument list.
    else:

        for w in args_array:

            if w in func_dict:
                func_dict[w](MASTER, SLAVE, form=frmt, ofile=outfile,
                             db_tbl=db_tbl, class_cfg=Mongo_Cfg)


def run_program(args_array, func_dict):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    MASTER = None

    if "-c" in args_array:
        mst_cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

        MASTER = mysql_class.MasterRep(mst_cfg.name, mst_cfg.sid,
                                       mst_cfg.user, mst_cfg.passwd,
                                       getattr(machine, mst_cfg.serv_os)(),
                                       mst_cfg.host, mst_cfg.port,
                                       mst_cfg.cfg_file)
        MASTER.connect()

    SLAVE = []

    if "-s" in args_array:
        slv_cfg = cmds_gen.create_cfg_array(args_array["-s"],
                                            cfg_path=args_array["-d"])

        for slv in slv_cfg:
            slv_inst = mysql_class.SlaveRep(slv["name"], slv["sid"],
                                            slv["user"], slv["passwd"],
                                            getattr(machine,
                                                    slv["serv_os"])(),
                                            slv["host"], int(slv["port"]),
                                            slv["cfg_file"])
            slv_inst.connect()

            if slv_inst.conn:
                SLAVE.append(slv_inst)

    call_run_chk(args_array, func_dict, MASTER, SLAVE)

    cmds_gen.disconnect(MASTER, SLAVE)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
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

    dir_chk_list = ["-d", "-p"]
    file_chk_list = ["-o"]
    file_crt_list = ["-o"]
    func_dict = {"-A": ["-C", "-S", "-E", "-T", "-O"], "-B": rpt_mst_log,
                 "-D": rpt_slv_log, "-C": chk_mst_log, "-S": chk_slv_thr,
                 "-E": chk_slv_err, "-T": chk_slv_time, "-O": chk_slv_other}
    opt_con_req_list = {"-b": ["-m"]}
    opt_def_dict = {"-f": "standard", "-b": "sysmon:mysql_rep_lag"}
    opt_or_dict_list = {"-c": ["-s"]}
    opt_req_list = ["-d"]
    opt_val_list = ["-d", "-c", "-p", "-s", "-f", "-o", "-b", "-m"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list, opt_def_dict)

    if not gen_libs.help_func(args_array, __version__, help_message):
        if arg_parser.arg_req_or_lst(args_array, opt_or_dict_list) \
           and not arg_parser.arg_require(args_array, opt_req_list) \
           and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
           and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
           and not arg_parser.arg_file_chk(args_array, file_chk_list,
                                           file_crt_list):
            run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
