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
        mysql_rep_admin.py -d path [-p path]
            {-C -c file -s [path]/slave.txt} |
            {-S -s [path]/slave.txt} |
            {-B -c file} |
            {-D -s [path]/slave.txt} |
            {-T -c file -s [path]/slave.txt [-j [-f]] [-o dir_path/file [-a]]
                [-b db:coll | -m file]
                [-t ToEmail {ToEmail2 ...} {-u SubjectLine}]} |
            {-E -s [path]/slave.txt} |
            {-A -s [path]/slave.txt} |
            {-O -s [path]/slave.txt}
            [-y flavor_id] [-z]
            [-v | -h]

    Arguments:
        -d dir path => Directory path to the config files (-c). Required arg.
        -c file => Master config file.
            For use with the -C, -B, and -T options.
        -s [path]/slave.txt => Slave config file.
        -C => Compare master binlog position to the slaves' and return any
            differences detected if not the same positions.
        -S => Check the slave(s) IO and SQL threads and return any errors or
            warnings detected.
        -B => Display the master binlog filename and position.
        -D => Display the slave(s) binlog filename and position.
        -T => Check time lag for the slave(s) and return any differences
            detected.
        -E => Check for any replication errors on the slave(s).
        -A => Does multiple checks which include the following options:
            (-C, -S, -T, -E)
        -O => Other slave replication checks and return any errors detected.
        -j => Return output in JSON format, if available.
            For use with the -T option.
        -f => Flatten the JSON data structure to file and standard out.
            For use with the -j option.
        -o path/file => Directory path and file name for output.
            Use the -a option to append to an existing file.
            For use with the -T option.
        -a => Append output to output file.
        -b database:collection => Name of database and collection.
            Default: sysmon:mysql_rep_lag
        -m file => Insert results into a Mongo database.  File is the Mongo
            config file.
            For use with the -T option.
        -p dir_path => Directory path to the mysql binary programs.
        -t to_email_addresses => Enables emailing capability for an option if
            the option allows it.  Sends output to one or more email addresses.
            For use with the -T option.
        -u subject_line => Subject line of email.  Optional, will create own
            subject line if one is not provided.
        -y value => A flavor id for the program lock.  To create unique lock.
        -z => Suppress standard out.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE:  -v or -h overrides the other options.

    Notes:
        Master configuration file format (config/mysql_cfg.py.TEMPLATE):
        NOTE:  Do not use the loopback IP or 'localhost' for the "host"
        variable, use the actual IP.
            # Configuration file for {Database Name/Server}
            user = "USER"
            passwd = "PASSWORD"
            host = "IP_ADDRESS"
            name = "HOSTNAME"
            sid = SERVER_ID
            extra_def_file = "DIRECTORY_PATH/config/mysql.cfg"
            serv_os = "Linux"
            port = 3306
            cfg_file = "DIRECTORY_PATH/my.cnf"

        NOTE 1:  Include the cfg_file even if running remotely as the
            file will be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the
            defaults-extra-file format.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.

        Slave configuration file format (config/slave.txt.TEMPLATE)
        Make a copy of this section for each slave in the replica set.
            # Slave 1 configuration {Database Name/Server}
            user = USER
            passwd = PASSWORD
            host = IP_ADDRESS
            name = HOSTNAME
            sid = SERVER_ID
            cfg_file = None
            port = 3306
            serv_os = Linux

        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
            configuration file format for the Mongo connection used for
            inserting data into a database.
            There are two ways to connect:  single or replica set.

            1.)  Single database connection:

            # Single Configuration file for Mongo Database Server.
            user = "USER"
            passwd = "PASSWORD"
            host = "IP_ADDRESS"
            name = "HOSTNAME"
            port = 27017
            conf_file = None
            auth = True

            2.)  Replica Set connection:  Same format as above, but with these
                additional entries at the end of the configuration file:

            repset = "REPLICA_SET_NAME"
            repset_hosts = "HOST1:PORT, HOST2:PORT, HOST3:PORT, [...]"
            db_auth = "AUTHENTICATION_DATABASE"

    Example:
        mysql_rep_admin.py -c master -d config  -s slave.txt -A

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

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
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
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            # Master's log file or position doesn't match slave's log info.
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print("Master: {0}".format(master.name))
                print("\tMaster Log: {0}".format(fname))
                print("\t\tMaster Pos: {0}".format(log_pos))
                print("Slave: {0}".format(name))
                print("\tSlave Log: {0}".format(mst_file))
                print("\t\tSlave Pos: {0}".format(read_pos))

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
                print("Error:  Slave IO/SQL Threads are down.")

            # Slave IO thread.
            elif not gen_libs.is_true(io_thr):
                print(PRT_TEMPLATE.format(name))
                print("Error:  Slave IO Thread is down.")

            # Slave SQL thread.
            elif not gen_libs.is_true(sql_thr):
                print(PRT_TEMPLATE.format(name))
                print("Error:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_slv_err(master, slaves, **kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    slaves = list(slaves)

    if slaves:

        for slv in slaves:

            # For pre-MySQL 5.6 versions, will be NULL for these two entries.
            io, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # IO error
            if io:
                print("\nSlave:\t{0}".format(name))
                print("IO Error Detected:\t{0}".format(io))
                print("\tIO Message:\t{0}".format(io_msg))

                print("\tIO Timestamp:\t{0}".format(io_time))

            # SQL error
            if sql:
                print("\nSlave:\t{0}".format(name))
                print("SQL Error Detected:\t{0}".format(sql))
                print("\tSQL Message:\t{0}".format(sql_msg))

                print("\tSQL Timestamp:\t{0}".format(sql_time))

    else:
        print("\nchk_slv_err:  Warning:  No Slave instance detected.")


def add_miss_slaves(master, outdata, **kwargs):

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

    for x in master.show_slv_hosts():
        all_list.append(x["Host"])

    for y in outdata["Slaves"]:
        slv_list.append(y["Name"])

    # Add slaves from the slave list that are not in the master's slave list.
    for x in [val for val in all_list if val not in slv_list]:
        outdata["Slaves"].append({"Name": x, "LagTime": None})

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

    """

    jdata = json.dumps(outdata, indent=4)
    mongo_cfg = kwargs.get("class_cfg", None)
    db_tbl = kwargs.get("db_tbl", None)
    ofile = kwargs.get("ofile", None)
    mail = kwargs.get("mail", None)
    mode = kwargs.get("mode", "w")

    if mongo_cfg and db_tbl:
        db, tbl = db_tbl.split(":")
        mongo_libs.ins_doc(mongo_cfg, db, tbl, outdata)

    if ofile:
        gen_libs.write_file(ofile, mode, jdata)

    if mail:
        mail.add_2_msg(jdata)
        mail.send_mail()

    if not kwargs.get("sup_std", False):
        gen_libs.print_data(jdata)


def _process_time_lag(slv, time_lag, name, json_fmt, **kwargs):

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

    if time_lag:
        time.sleep(5)
        slv.upd_slv_time()
        time_lag = slv.get_time()

        if time_lag and not json_fmt:
            print("\nSlave:  {0}".format(name))
            print("\tTime Lag:  {0}".format(time_lag))

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
            _chk_other(skip, tmp_tbl, retry, name)

    else:
        print("\nchk_slv_other:  Warning:  No Slave instance detected.")


def _chk_other(skip, tmp_tbl, retry, name, **kwargs):

    """Function:  _chk_other

    Description:  Private function for chk_slv_other().  Print any possible
        problems found.

    Arguments:
        (input) skip -> Mysql's skip count.
        (input) tmp_tbl -> Mysql's temp tables created count.
        (input) retry -> Mysql's retry count.
        (input) name -> Name of Mysql server.

    """

    global PRT_TEMPLATE

    if skip > 0 or int(tmp_tbl) > 5 or int(retry) > 0:
        print(PRT_TEMPLATE.format(name))

        if skip > 0:
            print("Skip Count:  {0}".format(skip))

        if int(tmp_tbl) > 5:
            print("Temp Table Count:  {0}".format(tmp_tbl))

        if int(retry) > 0:
            print("Retried Transaction Count:  {0}".format(retry))


def call_run_chk(args_array, func_dict, master, slaves, **kwargs):

    """Function:  call_run_chk

    Description:  Calls the specified option function calls based on what
        instances are available.  Both the master and slaves
        instances are passed to the functions, the functions will
        determine what instances to be used.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) master -> Master instance.
        (input) slaves -> Slave instances.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    slaves = list(slaves)
    json_fmt = args_array.get("-j", False)
    outfile = args_array.get("-o", None)
    db_tbl = args_array.get("-b", None)
    sup_std = args_array.get("-z", False)
    mongo_cfg = None
    mail = None
    mode = "w"
    indent = 4

    if args_array.get("-a", False):
        mode = "a"

    if args_array.get("-f", False):
        indent = None

    if args_array.get("-m", None):
        mongo_cfg = gen_libs.load_module(args_array["-m"], args_array["-d"])

    if args_array.get("-t", None):
        mail = gen_class.setup_mail(args_array.get("-t"),
                                    subj=args_array.get("-u", None))

    if "-A" in args_array:

        for x in func_dict["-A"]:
            func_dict[x](
                master, slaves, json_fmt=json_fmt, ofile=outfile,
                db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail, sup_std=sup_std,
                mode=mode, indent=indent)

        for y in args_array:

            # The option is in func_dict but not under the ALL option and is
            #   not the ALL option itself.
            if y in func_dict and y not in func_dict["-A"] and y != "-A":
                func_dict[y](
                    master, slaves, json_fmt=json_fmt, ofile=outfile,
                    db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail,
                    sup_std=sup_std, mode=mode, indent=indent)

    else:

        # Intersect args_array & func_dict to find which functions to call.
        for opt in set(args_array.keys()) & set(func_dict.keys()):
            func_dict[opt](
                master, slaves, json_fmt=json_fmt, ofile=outfile,
                db_tbl=db_tbl, class_cfg=mongo_cfg, mail=mail, sup_std=sup_std,
                mode=mode, indent=indent)


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    master = None

    if "-c" in args_array:
        mst_cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

        master = mysql_class.MasterRep(mst_cfg.name, mst_cfg.sid,
                                       mst_cfg.user, mst_cfg.passwd,
                                       getattr(machine, mst_cfg.serv_os)(),
                                       mst_cfg.host, mst_cfg.port,
                                       mst_cfg.cfg_file)
        master.connect()

    slaves = []

    if "-s" in args_array:
        slv_cfg = cmds_gen.create_cfg_array(args_array["-s"],
                                            cfg_path=args_array["-d"])
        slaves = mysql_libs.create_slv_array(slv_cfg)

    call_run_chk(args_array, func_dict, master, slaves)

    if master:
        cmds_gen.disconnect(master, slaves)

    else:
        cmds_gen.disconnect(slaves)


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

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d", "-p"]
    file_chk_list = ["-o"]
    file_crt_list = ["-o"]
    func_dict = {"-A": ["-C", "-S", "-E", "-T", "-O"], "-B": rpt_mst_log,
                 "-D": rpt_slv_log, "-C": chk_mst_log, "-S": chk_slv_thr,
                 "-E": chk_slv_err, "-T": chk_slv_time, "-O": chk_slv_other}
    opt_con_req_list = {"-b": ["-m"], "-u": ["-t"], "-A": ["-s"], "-B": ["-c"],
                        "-C": ["-c", "-s"], "-D": ["-s"], "-E": ["-s"],
                        "-O": ["-s"], "-T": ["-c", "-s"]}
    opt_def_dict = {"-b": "sysmon:mysql_rep_lag"}
    opt_multi_list = ["-u", "-t"]
    opt_or_dict_list = {"-c": ["-s"]}
    opt_req_list = ["-d"]
    opt_val_list = ["-d", "-c", "-p", "-s", "-o", "-b", "-m", "-u", "-t", "-y"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list,
                                       opt_def_dict, multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_req_or_lst(args_array, opt_or_dict_list) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and not arg_parser.arg_file_chk(args_array, file_chk_list,
                                       file_crt_list):

        try:
            proglock = gen_class.ProgramLock(cmdline.argv,
                                             args_array.get("-y", ""))
            run_program(args_array, func_dict)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_admin with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
