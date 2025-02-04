# Python project for replication administration for MySQL replication.
# Classification (U)

# Description:
  Used for replication administration in a MySQL replication setup to include checking binary log status, slave status, master status, time lag between master and slave, errors detected within replication, binary log positions, and replication configuration status.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Check the slave(s) IO and SQL threads.
  * Compare master binlog position to the slaves.
  * Display the master and/or slave binlog filename and position.
  * Check time lag for the slave(s).
  * Check for errors on the slave(s).
  * Display server information for master and/or slave(s).

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python3-pip
    - python3-devel
    - gcc


# Installation:

Install this project using git.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create MySQL configuration file and make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "**PYTHON_PROJECT**/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

  * Change these entries only if required:
    - serv_os = "Linux"
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * TLS version: Set what TLS versions are allowed in the connection set up.
    - tls_versions = []

```
cp config/mysql_cfg.py.TEMPLATE config/mysql_cfg.py
vim config/mysql_cfg.py
chmod 600 config/mysql_cfg.py
```

Create MySQL definition file and make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
  * Note:  socket use is only required to be set in certain conditions when connecting using localhost.
    - password="PASSWORD"
    - socket=DIRECTORY_PATH/mysqld.sock

```
cp config/mysql.cfg.TEMPLATE config/mysql.cfg
vim config/mysql.cfg
chmod 600 config/mysql.cfg
```

Create Slave definition file and make the appropriate change for a slave connection.
  * Change these entries in the MySQL slave setup:
    - user = USER
    - japd = PSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID
    - extra_def_file = **PYTHON_PROJECT**/config/mysql.cfg

  * Change these entries only if required:
    - cfg_file = None
    - serv_os = Linux
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * NOTE:  Create a new set of entries for each slave in the MySQL replica set.

```
cp config/slave.txt.TEMPLATE config/slave.txt
vim config/slave.txt
chmod 600 config/slave.txt
```

### Database Configuration

For some options to work correctly the report-host and report-port options must be added to each of the slaves mysqld.cnf file and the database restarted.
It is recommended to add these entries to all slaves including the master database.

Add the following lines to the mysqld.cnf file under the [mysqld] section.
  * report-host and report-port must match up with "name" and "port" entries respectively from the mysql_cfg.py/slave.txt file.

report-host = HOSTNAME
report-port = PORT

Restart each of the database instances for the changes to take effect.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
mysql_rep_admin.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/unit/mysql_rep_admin/unit_test_run.sh
test/unit/mysql_rep_admin/code_coverage.sh
```

