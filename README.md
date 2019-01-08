# Python project for replication administration for MySQL replication.
# Classification (U)

# Description:
  This program is used for replication administration in a MySQL replication setup to include checking binary log status, slave status, master status, time lag between master and slave, errors detected within replication, binary log positions, and replication configuration status.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Check the slave(s) IO and SQL threads.
  * Compare master binlog position to the slaves.
  * Display the master and/or slave binlog filename and position.
  * Check time lag for the slave(s).
  * Check for errors on the slave(s).
  * Display server information for master and/or slave(s).

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - lib/errors
    - lib/machine
    - mysql_lib/mysql_libs
    - mysql_lib/mysql_class
    - mongo_lib/mongo_libs


# Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
```

Install/upgrade system modules.

```
cd mysql-rep-admin
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Descriptions:
### Program: mysql_rep_admin.py
##### Description: Replication administration program for a MySQL replication setup.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-rep-admin/mysql_rep_admin.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_rep_admin.py

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
            | -C | -S | -B | -D | -T | -R | -E | -A | -I | -O |
            -f {JSON|standard | -b db:coll | -m file} | -o dir_path/file]
            [-v | -h]

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
        -R => Replication check using the mysqlrplcheck program.
        -E => Check for errors on the slave(s).
        -I => Display server information for master and/or slave(s).
        -A => Does multiple checks which include the following options:
            (-C, -S, -T, -R, -E)
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
            # DO NOT USE 127.0.0.1 for the master/source, use actual IP.
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


# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_rep_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
```

Install/upgrade system modules.

```
cd mysql-rep-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for mysql_rep_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-rep-admin
```


### Unit:  help_message
```
test/unit/mysql_rep_admin/help_message.py
```

### Unit:  
```
test/unit/mysql_rep_admin/
```

### Unit:  
```
test/unit/mysql_rep_admin/
```

### Unit:  run_program
```
test/unit/mysql_rep_admin/run_program.py
```

### Unit:  main
```
test/unit/mysql_rep_admin/main.py
```

### All unit testing
```
test/unit/mysql_rep_admin/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_admin/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_rep_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
```

Install/upgrade system modules.

```
cd mysql-rep-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.

```
cd test/integration/mysql_rep_admin/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Integration test runs for mysql_rep_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-rep-admin
```


### Integration:  
```
test/integration/mysql_rep_admin/
```

### All integration testing
```
test/integration/mysql_rep_admin/integration_test_run.sh
```

### Code coverage program
```
test/integration/mysql_rep_admin/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_rep_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
```

Install/upgrade system modules.

```
cd mysql-rep-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.

```
cd test/blackbox/mysql_rep_admin/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

# Blackbox test run for mysql_rep_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-rep-admin
```


### Blackbox:  
```
test/blackbox/mysql_rep_admin/blackbox_test.sh
```

